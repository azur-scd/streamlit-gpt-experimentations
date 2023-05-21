# syntax=docker/dockerfile:1
FROM python:3.10.8-slim-buster
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8051

#CMD ["streamlit", "run", "About.py", "--server.sslCertFile=ssl/localhost.crt","--server.sslKeyFile=ssl/localhost.key","--server.port=8051", "--server.address=0.0.0.0"]
CMD ["streamlit", "run", "About.py"]