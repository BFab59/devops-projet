FROM python:3.11-slim

WORKDIR /app

# Dépendances d'abord (layer cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code ensuite
COPY . .

EXPOSE 5000

# Gunicorn en prod, plus robuste que le serveur Flask natif
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app:app"]
