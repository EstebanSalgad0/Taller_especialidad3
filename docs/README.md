# 📁 Evidencias del Proyecto

Esta carpeta contiene las evidencias de funcionamiento del stack Docker Compose.

## 📋 Índice de evidencias

1. **[01-docker-compose-ps.md](01-docker-compose-ps.md)**
   - Estado de todos los contenedores
   - Verificación de health status
   - Puertos expuestos

2. **[02-healthchecks.md](02-healthchecks.md)**
   - Logs de healthchecks de DB y API
   - Verificación de arranque ordenado
   - Estado de salud de cada servicio

3. **[03-endpoints-funcionando.md](03-endpoints-funcionando.md)**
   - GET /items (listado inicial)
   - POST /items (crear nuevo item)
   - Verificación de respuestas JSON

4. **[04-persistencia.md](04-persistencia.md)**
   - Datos antes del reinicio
   - Proceso de down/up del stack
   - Verificación de persistencia en volumen

5. **[05-escalamiento-balanceo.md](05-escalamiento-balanceo.md)**
   - Escalamiento a 2 réplicas
   - 6 peticiones consecutivas
   - Evidencia de round-robin (hostnames alternando)

## 🎯 Cómo generar nuevas evidencias

Si necesitas regenerar las evidencias, ejecuta:

```powershell
# Desde la raíz del proyecto
cd catalogo_starter

# Las evidencias se generan automáticamente con los comandos del README
# O ejecuta cada archivo de evidencia manualmente
```

## 📅 Información

- **Fecha de generación**: Noviembre 6, 2025
- **Ambiente**: Docker Desktop en Windows
- **Stack**: FastAPI + PostgreSQL + Nginx
