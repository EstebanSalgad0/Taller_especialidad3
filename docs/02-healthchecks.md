# Evidencia 2: Logs de healthchecks

## Comando ejecutado
```powershell
docker compose logs --tail=30 | Select-String -Pattern "health"
```

## Logs de DB (PostgreSQL)
```
db-1  | 
db-1  | PostgreSQL Database directory appears to contain a database; Skipping initialization
db-1  | 
db-1  | 2025-11-06 18:40:13.461 UTC [1] LOG:  starting PostgreSQL 16.10 on x86_64-pc-linux-musl, compiled by gcc (Alpine 14.2.0) 14.2.0, 64-bit
db-1  | 2025-11-06 18:40:13.462 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db-1  | 2025-11-06 18:40:13.462 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db-1  | 2025-11-06 18:40:13.467 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2025-11-06 18:40:13.474 UTC [29] LOG:  database system was shut down at 2025-11-06 18:40:11 UTC
db-1  | 2025-11-06 18:40:13.483 UTC [1] LOG:  database system is ready to accept connections
db-1  | 2025-11-06 18:40:49.915 UTC [99] ERROR:  relation "items" does not exist at character 29
db-1  | 2025-11-06 18:40:49.915 UTC [99] STATEMENT:  SELECT id, name, price FROM items ORDER BY id;
db-1  | 2025-11-06 18:45:13.555 UTC [27] LOG:  checkpoint starting: time
db-1  | 2025-11-06 18:45:18.120 UTC [27] LOG:  checkpoint complete: wrote 48 buffers (0.3%); 0 WAL file(s) added, 0 removed, 0 recycled; write=4.530 s, sync=0.024 s, total=4.566 s; sync files=37, longest=0.008 s, average=0.001 s; distance=203 kB, estimate=203 kB; lsn=0/1998040, redo lsn=0/1997FF0

```

## Logs de API (FastAPI)
```
api-1  | INFO:     127.0.0.1:45706 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:52838 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:52852 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:42462 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:42476 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:43326 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:43342 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:55848 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:55862 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:42496 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:42498 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:49288 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:38274 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:38284 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:34642 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:34644 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:56830 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:56834 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:48728 - "GET /health HTTP/1.1" 200 OK
api-1  | INFO:     127.0.0.1:48732 - "GET /health HTTP/1.1" 200 OK

```

## Verificación de healthchecks
```powershell
docker inspect catalogo_starter-db-1 --format='{{.State.Health.Status}}'
docker inspect catalogo_starter-api-1 --format='{{.State.Health.Status}}'
```

```
DB Health: healthy
API Health: healthy
```

## Análisis
-  **DB healthcheck**: pg_isready responde OK
-  **API healthcheck**: /health endpoint respondiendo
-  **Arranque ordenado**: DB  API  Proxy

Fecha: 2025-11-06 15:56:01
