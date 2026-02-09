## Port Knocking Starter Template

This directory is a starter template for the port knocking portion of the assignment.

### What you need to implement
- Pick a protected service/port (default is 2222).
- Define a knock sequence (e.g., 1234, 5678, 9012).
- Implement a server that listens for knocks and validates the sequence.
- Open the protected port only after a valid sequence.
- Add timing constraints and reset on incorrect sequences.
- Implement a client to send the knock sequence.

### Getting started
1. Implement your server logic in `knock_server.py`.
2. Implement your client logic in `knock_client.py`.
3. Update `demo.sh` to demonstrate your flow.
4. Run from the repo root with `docker compose up port_knocking`.

### Example usage
```bash
python3 knock_client.py --target 172.20.0.40 --sequence 1234,5678,9012
```

# Port Knocking Security Fix

## Overview
This project implements **port knocking** to protect a hidden service running on port **2222**.  
The service remains inaccessible until a client sends a predefined sequence of connection attempts (knocks) to specific ports in the correct order.

**Knock sequence used:**


1234 → 5678 → 9012


Once the correct sequence is received within a limited time window, the server dynamically updates firewall rules to allow the client’s IP address to access the protected port.

---

## How It Works

### Server (`knock_server.py`)
- Listens for incoming TCP connection attempts on the knock ports.
- Tracks knock progress **per source IP**.
- Enforces a timing window to prevent slow or brute-force attempts.
- On successful sequence:
  - Uses `iptables` to allow the client IP access to port `2222`.
- On incorrect sequence or timeout:
  - Resets the client’s progress.

### Client (`knock_client.py`)
- Sends connection attempts to each port in the knock sequence.
- Optional verification step checks if the protected port becomes reachable after knocking.

---

## Dockerized Setup

The server is containerized and runs with elevated privileges to manage firewall rules.

### Build
```bash
docker build -t knock-server .



Run:

docker run --rm -it --privileged \
  -p 3333:2222 \
  -p 1234:1234 \
  -p 5678:5678 \
  -p 9012:9012 \
  knock-server

Port 3333 on the host maps to protected port 2222 inside the container.

Running the Client
python3 knock_client.py --target <target-ip> --sequence 1234,5678,9012 --check

Security Benefit

Port knocking reduces the attack surface by hiding services from unauthorized users.
Only clients that know the correct knock sequence can access the protected service, preventing automated scans and unauthorized connection attempts.