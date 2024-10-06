# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto en el que Uvicorn correrá
EXPOSE 8000

# Comando para ejecutar tanto FastAPI con Uvicorn como la parte de CMD
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & python main.py"]
