# ===== Builder =====
FROM python:3.12-alpine AS builder
WORKDIR /app
RUN apk add --no-cache build-base
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ===== Runner =====
FROM python:3.12-alpine AS runner
RUN apk add --no-cache curl
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app.py /app/app.py
EXPOSE 8000
USER app
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
