# Dockerfile
FROM python:3.8
ENV PYTHONUNBUFFERED 1

# Kodu kopyalamak için /app dizinini oluştur
RUN mkdir /app

# Çalışma dizinini /app olarak ayarla
WORKDIR /app

# requirements.txt dosyasını önce kopyala
COPY requirements.txt /app/

# Gereksinimleri kur
RUN pip install -r requirements.txt

# Geri kalan dosyaları kopyala
COPY . /app/
