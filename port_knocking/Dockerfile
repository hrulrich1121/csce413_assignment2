FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends iptables iproute2 netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY knock_server.py knock_client.py demo.sh ./

EXPOSE 1234 5678 9012 2222

CMD ["python3", "knock_server.py", "--sequence", "1234,5678,9012", "--protected-port", "2222"]
