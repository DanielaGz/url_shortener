# ---------------------------
# 1️⃣ Imagen base liviana
# ---------------------------
FROM python:3.10-slim

# ---------------------------
# 2️⃣ Establecer directorio de trabajo
# ---------------------------
WORKDIR /app

# ---------------------------
# 3️⃣ Copiar dependencias primero para aprovechar cache
# ---------------------------
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------
# 4️⃣ Copiar el resto del código
# ---------------------------
COPY . .

# ---------------------------
# 5️⃣ Configurar variables de entorno
# ---------------------------
# Puerto que usará Cloud Run
ENV PORT=8080
# Evitar bytecode y mejorar logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ---------------------------
# 6️⃣ Comando de arranque
# ---------------------------
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8080"]
