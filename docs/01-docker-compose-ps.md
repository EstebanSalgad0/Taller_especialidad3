# Evidencia 1: Estado de contenedores (docker compose ps)

## Comando ejecutado
```powershell
docker compose ps
```

## Resultado
```
NAME                       IMAGE                  COMMAND                  SERVICE   CREATED          STATUS                    PORTS
catalogo_starter-api-1     catalogo_starter-api   "python -m uvicorn aÔÇª"   api       14 minutes ago   Up 14 minutes (healthy)   8000/tcp
catalogo_starter-db-1      postgres:16-alpine     "docker-entrypoint.sÔÇª"   db        14 minutes ago   Up 14 minutes (healthy)   5432/tcp
catalogo_starter-proxy-1   nginx:1.27-alpine      "/docker-entrypoint.ÔÇª"   proxy     14 minutes ago   Up 14 minutes             0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

```

## Análisis
-  **3 contenedores corriendo**
-  **Todos en estado HEALTHY**
-  **Solo proxy expone puerto** (8080:80)
-  **API y DB en red interna**

Fecha: 2025-11-06 15:54:56
