````markdown
# Catálogo de Productos - API REST con Docker

Proyecto de catálogo de productos usando FastAPI, PostgreSQL y Nginx como reverse proxy, todo orquestado con Docker Compose.

## 🚀 Requisitos previos
- Docker Engine / Docker Desktop (Compose v2)
- Git

## ⚙️ Configuración inicial

### 1. Variables de entorno
Primero copio el archivo de ejemplo y configuro las variables:
```bash
cp .env.example .env
```
Dentro de `.env` tengo configurado:
- `DB_NAME=catalogo`
- `DB_USER=postgres`

### 2. Secret de la base de datos
Para la contraseña de PostgreSQL uso Docker secrets. Creo el archivo localmente:
```bash
echo "changeme" > db_password.txt
```
**Importante**: Este archivo está en `.gitignore` y NO debe subirse al repositorio. En producción usaría Docker Swarm secrets o algún gestor de secretos como HashiCorp Vault.

## 🐳 Levantar el stack

Uso el Makefile que creé para simplificar los comandos:
```bash
make up
make ps
```

O directamente con Docker Compose:
```bash
docker compose up -d --build
docker compose ps
```

El stack levanta en este orden gracias a los healthchecks:
1. **PostgreSQL** (db) - espera hasta que `pg_isready` responda OK
2. **FastAPI** (api) - espera a que DB esté healthy
3. **Nginx** (proxy) - espera a que API esté healthy

## 🧪 Probar los endpoints

### Health check
```bash
curl -s http://localhost:8080/health
```
Respuesta esperada:
```json
{"status":"ok","host":"<container_id>"}
```

### Listar items
```bash
curl -s http://localhost:8080/items
```
Respuesta esperada (3 items del seed.sql):
```json
{
  "host":"<container_id>",
  "items":[
    {"id":1,"name":"Cuaderno","price":1990.0},
    {"id":2,"name":"Lápiz","price":500.0},
    {"id":3,"name":"Mochila","price":15990.0}
  ]
}
```

### Agregar un nuevo item
```bash
curl -X POST http://localhost:8080/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Regla","price":890}'
```

## 📊 Tamaño de la imagen optimizada

Implementé un **Dockerfile multi-stage** para reducir el tamaño de la imagen final:

### Etapa 1: Builder
- Instala herramientas de compilación (`build-base`)
- Compila dependencias Python (psycopg2 requiere compilación)
- Instala paquetes en `/install`

### Etapa 2: Runner
- Imagen limpia sin herramientas de build
- Solo copia los artefactos necesarios de `/install`
- Agrega `curl` para healthcheck
- Usuario no-root (`app`)

### Resultado
```bash
docker image ls catalogo_starter-api
```
- **Tamaño final**: ~113 MB (Alpine + FastAPI + psycopg2 + curl)
- **Comparación**: Sin multi-stage serían ~300+ MB con todas las herramientas de compilación

## 📈 Escalamiento y balanceo

Configuré Nginx para hacer round-robin entre réplicas de la API. Puedo escalar fácilmente:

```bash
make scale
```

O con Docker Compose directamente:
```bash
docker compose up -d --scale api=2
```

Para verificar el balanceo, hago varias peticiones y veo cómo alterna el hostname:
```bash
curl -s http://localhost:8080/health
curl -s http://localhost:8080/health
curl -s http://localhost:8080/health
```

Cada respuesta muestra un `host` diferente, confirmando que Nginx está distribuyendo las peticiones entre las dos réplicas.

**¿Cómo funciona?**
- Configuré el `resolver 127.0.0.11` en Nginx (DNS interno de Docker)
- Esto permite que Nginx re-resuelva el nombre `api` dinámicamente
- Docker DNS devuelve las IPs de todas las réplicas en round-robin

## 💾 Persistencia de datos

Los datos de PostgreSQL se guardan en un volumen nombrado (`pgdata`), por lo que persisten aunque baje los contenedores.

### Prueba de persistencia
```bash
# 1. Agrego un item nuevo
curl -X POST http://localhost:8080/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Prueba","price":100}'

# 2. Bajo completamente el stack
docker compose down

# 3. Vuelvo a levantar
docker compose up -d

# 4. Verifico que el item sigue ahí
curl -s http://localhost:8080/items
```

El item "Prueba" debería seguir en la lista porque los datos están en el volumen, no en el contenedor.

## 🔄 Backup y Restore

Implementé comandos en el Makefile para hacer backup y restore de la base de datos.

### Crear backup
```bash
make backup
```

Esto ejecuta:
```bash
docker compose exec -T db pg_dump -U postgres -d catalogo > backup.sql
```

### Restaurar desde backup
```bash
make restore
```

Esto ejecuta:
```bash
docker compose exec -T db psql -U postgres -d catalogo < backup.sql
```

### Prueba completa de backup/restore
```bash
# 1. Creo el backup
make backup

# 2. Borro la tabla (simulando pérdida de datos)
docker compose exec db psql -U postgres -d catalogo -c "DROP TABLE items;"

# 3. Verifico que ya no hay datos
curl -s http://localhost:8080/items
# Respuesta: error "relation items does not exist"

# 4. Restauro desde el backup
make restore

# 5. Verifico que los datos volvieron
curl -s http://localhost:8080/items
# Respuesta: todos los items restaurados
```

## 🏗️ Decisiones de diseño e implementación

### Seguridad

**Usuario no-root en contenedores**
- Creé un usuario `app` sin privilegios en el Dockerfile
- La API corre con este usuario, no como root
- Esto limita el daño si hay una vulnerabilidad

**Gestión de secretos**
- Uso Docker Compose secrets para la contraseña de PostgreSQL
- El secret se monta en `/run/secrets/db_password`
- Mi código lee desde este archivo usando `DB_PASSWORD_FILE`
- No hay credenciales hardcodeadas en el código ni en las imágenes

**Cabeceras de seguridad en Nginx**
Configuré estas cabeceras para protección básica:
- `X-Content-Type-Options: nosniff` - previene MIME sniffing
- `X-Frame-Options: DENY` - previene clickjacking
- `Referrer-Policy: no-referrer` - no envía el referrer

**`.dockerignore` completo**
Excluyo archivos innecesarios de la imagen:
- Secretos (`.env`, `db_password.txt`)
- Python artifacts (`__pycache__`, `.venv`)
- Git (`.git/`, `.gitignore`)
- Documentación (`*.md`, `docs/`)
- OS files (`.DS_Store`, `Thumbs.db`)

### Arquitectura de red

**Dos redes separadas**
```
Host (:8080)
    ↓
[edge] → Nginx (proxy)
    ↓
[edge] → FastAPI (api)
    ↓
[backend] → PostgreSQL (db)
```

- **Red `edge`**: Proxy ↔ API (capa pública)
- **Red `backend`**: API ↔ DB (capa interna)
- Solo el proxy expone puerto al host (8080:80)
- La DB no es accesible desde fuera, solo desde la API

**Ventajas de este diseño**:
- DB completamente aislada del exterior
- Puedo escalar la API sin exponer puertos adicionales
- Fácil agregar más servicios en backend sin tocar edge

### Healthchecks y arranque ordenado

**PostgreSQL**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres -d catalogo"]
  interval: 5s
  timeout: 3s
  retries: 20
```

**FastAPI**
```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -fsS http://localhost:8000/health || exit 1"]
  interval: 5s
  timeout: 3s
  retries: 20
```

**Dependencias con `service_healthy`**
- API espera a que DB esté healthy antes de iniciar
- Proxy espera a que API esté healthy
- Esto evita errores de conexión durante el arranque

### Optimizaciones

**Dockerfile multi-stage**
- Separo construcción de runtime
- Builder: instala herramientas de compilación pesadas
- Runner: solo copia artefactos finales
- Resultado: imagen 60% más pequeña

**DNS dinámico en Nginx**
```nginx
resolver 127.0.0.11 valid=30s;
set $backend "api:8000";
proxy_pass http://$backend;
```
- Nginx re-resuelve el nombre `api` cada 30 segundos
- Permite round-robin real cuando escalo réplicas
- Sin esto, Nginx solo resolvería al arrancar

**Volumen nombrado para PostgreSQL**
- Uso `pgdata` en lugar de bind mount
- Docker gestiona el volumen automáticamente
- Mejor performance que bind mounts en Windows/Mac

## 📝 Comandos útiles (Makefile)

Creé estos comandos para facilitar el uso diario:

```bash
make up          # Levanta el stack en background
make down        # Baja todo y limpia volúmenes
make ps          # Estado de contenedores
make logs        # Ver logs en tiempo real
make build       # Reconstruir imágenes
make scale       # Escala API a 2 réplicas
make backup      # Crea backup.sql de la DB
make restore     # Restaura desde backup.sql
make image-size  # Muestra tamaño de imagen API
```

## 🎯 Tecnologías utilizadas

- **FastAPI** (Python 3.12): Framework web moderno y rápido
- **PostgreSQL 16**: Base de datos relacional
- **Nginx 1.27**: Reverse proxy y load balancer
- **Docker Compose**: Orquestación de contenedores
- **Alpine Linux**: Imágenes base ligeras

## 📸 Evidencias de funcionamiento

Todas las evidencias están documentadas en la carpeta [`/docs`](docs/):

1. **[docker compose ps](docs/01-docker-compose-ps.md)** - Estado de contenedores (todos healthy)
2. **[Healthchecks](docs/02-healthchecks.md)** - Logs mostrando healthchecks OK
3. **[Endpoints funcionando](docs/03-endpoints-funcionando.md)** - GET y POST /items
4. **[Persistencia](docs/04-persistencia.md)** - Datos manteniéndose tras reinicio
5. **[Escalamiento y balanceo](docs/05-escalamiento-balanceo.md)** - 2 réplicas con round-robin

Ver el índice completo en [docs/README.md](docs/README.md)

````
