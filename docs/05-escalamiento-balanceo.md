# Evidencia 5: Escalamiento y balanceo

## 1. Escalar API a 2 réplicas
```powershell
docker compose up -d --scale api=2
```

```
docker :  Container catalogo_starter-db-1  Running
En línea: 10 Carácter: 3
+ $(docker compose up -d --scale api=2 2>&1 | Out-String)
+   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: ( Container cata...r-db-1  Running:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
 Container catalogo_starter-api-1  Running
 Container catalogo_starter-api-2  Creating
 Container catalogo_starter-api-2  Created
 Container catalogo_starter-proxy-1  Running
 Container catalogo_starter-db-1  Waiting
 Container catalogo_starter-db-1  Healthy
 Container catalogo_starter-api-2  Starting
 Container catalogo_starter-api-2  Started
 Container catalogo_starter-api-2  Waiting
 Container catalogo_starter-api-1  Waiting
 Container catalogo_starter-api-2  Healthy
 Container catalogo_starter-api-1  Healthy

```

## 2. Verificar contenedores escalados
```powershell
docker compose ps
```

```
NAME                       IMAGE                  COMMAND                  SERVICE   CREATED              STATUS                        PORTS
catalogo_starter-api-1     catalogo_starter-api   "python -m uvicorn aÔÇª"   api       About a minute ago   Up 59 seconds (healthy)       8000/tcp
catalogo_starter-api-2     catalogo_starter-api   "python -m uvicorn aÔÇª"   api       7 seconds ago        Up 6 seconds (healthy)        8000/tcp
catalogo_starter-db-1      postgres:16-alpine     "docker-entrypoint.sÔÇª"   db        About a minute ago   Up About a minute (healthy)   5432/tcp
catalogo_starter-proxy-1   nginx:1.27-alpine      "/docker-entrypoint.ÔÇª"   proxy     About a minute ago   Up 53 seconds                 0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

```

## 3. Prueba de balanceo (6 peticiones consecutivas)
```powershell
for ($i=0; $i -lt 6; $i++) { 
  curl -s http://localhost:8080/health
  Start-Sleep -s 1
}
```

### Respuestas (observar campo 'host')
```
Petición 1: {"status":"ok","host":"4b312bb2e0c0"}
Petición 2: {"status":"ok","host":"1dd424097b26"}
Petición 3: {"status":"ok","host":"1dd424097b26"}
Petición 4: {"status":"ok","host":"4b312bb2e0c0"}
Petición 5: {"status":"ok","host":"1dd424097b26"}
Petición 6: {"status":"ok","host":"1dd424097b26"}
```

## Análisis
-  **2 réplicas de API corriendo** (api-1 y api-2)
-  **Nginx hace round-robin** entre ambas
-  **Hostname alterna** entre contenedores
-  **DNS dinámico funcionando** (resolver 127.0.0.11)

Fecha: 2025-11-06 15:59:04
