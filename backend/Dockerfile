FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

# 2 workers; meshing a scan takes a few seconds, so allow more than gunicorn's 30 s default.
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
