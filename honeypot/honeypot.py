#!/usr/bin/env python3
"""SSH Honeypot implementation"""

import socket
import threading
import time
import paramiko # type: ignore
from logger import get_logger

HOST_KEY = paramiko.RSAKey.generate(2048)
SSH_PORT = 22

class HoneypotServer(paramiko.ServerInterface):
    def __init__(self, client_ip, logger):
        self.client_ip = client_ip
        self.logger = logger
        self.event = threading.Event()
        self.username = None
        self.password = None

    def check_auth_password(self, username, password):
        self.username = username
        self.password = password
        self.logger.info(
            f"AUTH ATTEMPT from {self.client_ip} | username={username} password={password}"
        )
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


def handle_client(client, addr, logger):
    start_time = time.time()
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)

    server = HoneypotServer(addr[0], logger)

    try:
        transport.start_server(server=server)
        channel = transport.accept(20)
        if channel is None:
            return

        server.event.wait(10)
        channel.send(b"Welcome to Ubuntu 22.04 LTS\n$ ")

        while True:
            data = channel.recv(1024)
            if not data:
                break

            command = data.decode(errors="ignore").strip()
            logger.info(f"COMMAND from {addr[0]}: {command}")

            if command in ("exit", "logout"):
                channel.send(b"logout\n")
                break

            channel.send(b"bash: command not found\n$ ")

    except Exception as e:
        logger.error(f"Error handling client {addr[0]}: {e}")
    finally:
        duration = round(time.time() - start_time, 2)
        logger.info(f"DISCONNECT {addr[0]} session_duration={duration}s")
        transport.close()
        client.close()


def run_honeypot():
    logger = get_logger()
    logger.info("SSH Honeypot listening on port 22")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", SSH_PORT))
    sock.listen(100)

    while True:
        client, addr = sock.accept()
        logger.info(f"CONNECTION from {addr[0]}:{addr[1]}")
        threading.Thread(
            target=handle_client, args=(client, addr, logger), daemon=True
        ).start()


if __name__ == "__main__":
    run_honeypot()
