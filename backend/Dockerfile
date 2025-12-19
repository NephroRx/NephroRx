FROM python:3.11-slim

WORKDIR /app

# (Optional) system deps if you need them (e.g., psycopg2, pillow, etc.)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

# If your Flask app is app.py with "app = Flask(__name__)"
# gunicorn needs "module:variable"
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
