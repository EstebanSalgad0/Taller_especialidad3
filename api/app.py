import os
import socket
import psycopg2
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


def read_secret(path_env_key: str, fallback_env_key: str = None):
    """Lee una secret desde ruta (si existe), o desde env fallback."""
    path = os.getenv(path_env_key)
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    if fallback_env_key:
        return os.getenv(fallback_env_key)
    return None


DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_NAME = os.getenv("DB_NAME", "catalogo")
DB_PASSWORD = read_secret("DB_PASSWORD_FILE", "DB_PASSWORD")


def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        dbname=DB_NAME,
        password=DB_PASSWORD,
    )


@app.get("/health")
def health():
    return {"status": "ok", "host": socket.gethostname()}


@app.get("/items")
def items():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, price FROM items ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"host": socket.gethostname(), "items": [
            {"id": r[0], "name": r[1], "price": float(r[2])} for r in rows
        ]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


class ItemIn(BaseModel):
    name: str
    price: float


@app.post("/items")
def create_item(item: ItemIn):
    """Inserta un nuevo item en la base de datos y devuelve el registro creado."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id;",
            (item.name, item.price),
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"id": new_id, "name": item.name, "price": item.price}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
