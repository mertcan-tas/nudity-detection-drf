FROM python:3.12.7-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh && \  
    mkdir -p /app/staticfiles && \
    chmod -R 755 /app/staticfiles

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]