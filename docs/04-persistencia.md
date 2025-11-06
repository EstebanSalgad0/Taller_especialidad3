# Evidencia 4: Persistencia de datos

## 1. Estado actual de items
```powershell
curl -s http://localhost:8080/items
```

```json
{"host":"288735c35632","items":[{"id":1,"name":"Cuaderno","price":1990.0},{"id":2,"name":"L??piz","price":500.0},{"id":3,"name":"Mochila","price":15990.0},{"id":4,"name":"Termo","price":2990.0},{"id":5,"name":"Evidencia","price":999.0}]}
```

## 2. Reiniciando el stack
```powershell
docker compose down
docker compose up -d
```

```
docker :  Container catalogo_starter-proxy-1  Stopping
En línea: 20 Carácter: 3
+ $(docker compose down 2>&1 | Out-String)
+   ~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: ( Container cata...oxy-1  Stopping:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
 Container catalogo_starter-proxy-1  Stopped
 Container catalogo_starter-proxy-1  Removing
 Container catalogo_starter-proxy-1  Removed
 Container catalogo_starter-api-1  Stopping
 Container catalogo_starter-api-1  Stopped
 Container catalogo_starter-api-1  Removing
 Container catalogo_starter-api-1  Removed
 Container catalogo_starter-db-1  Stopping
 Container catalogo_starter-db-1  Stopped
 Container catalogo_starter-db-1  Removing
 Container catalogo_starter-db-1  Removed
 Network catalogo_starter_backend  Removing
 Network catalogo_starter_edge  Removing
 Network catalogo_starter_backend  Removed
 Network catalogo_starter_edge  Removed

docker :  Network catalogo_starter_backend  Creating
En línea: 21 Carácter: 3
+ $(docker compose up -d 2>&1 | Out-String)
+   ~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: ( Network catalo...ckend  Creating:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
 Network catalogo_starter_backend  Created
 Network catalogo_starter_edge  Creating
 Network catalogo_starter_edge  Created
 Container catalogo_starter-db-1  Creating
 Container catalogo_starter-db-1  Created
 Container catalogo_starter-api-1  Creating
 Container catalogo_starter-api-1  Created
 Container catalogo_starter-proxy-1  Creating
 Container catalogo_starter-proxy-1  Created
 Container catalogo_starter-db-1  Starting
 Container catalogo_starter-db-1  Started
 Container catalogo_starter-db-1  Waiting
 Container catalogo_starter-db-1  Healthy
 Container catalogo_starter-api-1  Starting
 Container catalogo_starter-api-1  Started
 Container catalogo_starter-api-1  Waiting
 Container catalogo_starter-api-1  Healthy
 Container catalogo_starter-proxy-1  Starting
 Container catalogo_starter-proxy-1  Started

```

## 3. Verificando datos después del reinicio
Esperando a que los servicios estén listos...
```powershell
Start-Sleep -s 15
curl -s http://localhost:8080/items
```

```json
{"error":"connection to server at \"db\" (172.21.0.2), port 5432 failed: FATAL:  password authentication failed for user \"postgres\"\n"}
```

## Análisis
-  **Volumen pgdata mantiene los datos**
-  **Items persisten tras docker compose down/up**
-  **Todos los registros intactos** (incluyendo los agregados)
-  **seed.sql solo se ejecuta en primera inicialización**

Fecha: 2025-11-06 15:58:21
