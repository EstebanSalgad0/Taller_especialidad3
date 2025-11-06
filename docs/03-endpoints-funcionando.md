# Evidencia 3: Endpoints funcionando (/items)

## GET /items - Estado inicial
```powershell
curl -s http://localhost:8080/items
```

### Respuesta
```json
{"host":"288735c35632","items":[{"id":1,"name":"Cuaderno","price":1990.0},{"id":2,"name":"L??piz","price":500.0},{"id":3,"name":"Mochila","price":15990.0},{"id":4,"name":"Termo","price":2990.0}]}
```

## POST /items - Agregar nuevo item
```powershell
curl -X POST http://localhost:8080/items -H 'Content-Type: application/json' -d '{\"name\":\"Evidencia\",\"price\":999}'
```

### Respuesta
```json
{"id":5,"name":"Evidencia","price":999.0}
```

## GET /items - Después del POST
```json
{"host":"288735c35632","items":[{"id":1,"name":"Cuaderno","price":1990.0},{"id":2,"name":"L??piz","price":500.0},{"id":3,"name":"Mochila","price":15990.0},{"id":4,"name":"Termo","price":2990.0},{"id":5,"name":"Evidencia","price":999.0}]}
```

## Análisis
-  **GET /items** funciona correctamente
-  **POST /items** crea nuevos registros
-  **Respuestas incluyen hostname** para verificar balanceo
-  **Datos persisten** en PostgreSQL

Fecha: 2025-11-06 15:57:39
