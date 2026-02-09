FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir paramiko

# Copy your scripts
COPY honeypot.py .
COPY logger.py . 

# Create logs directory
RUN mkdir -p /app/logs

EXPOSE 22

CMD ["python", "-u", "honeypot.py"]