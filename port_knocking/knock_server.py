#!/usr/bin/env python3
"""Starter template for the port knocking server."""

import argparse
import logging
import select
import socket
import subprocess
import time

DEFAULT_KNOCK_SEQUENCE = [1234, 5678, 9012]
DEFAULT_PROTECTED_PORT = 2222
DEFAULT_SEQUENCE_WINDOW = 10.0

knock_progress = {}

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def open_protected_port(ip, protected_port):
    """Open the protected port using firewall rules."""
    # TODO: Use iptables/nftables to allow access to protected_port.
    subprocess.run([
        "iptables", "-I", "INPUT",
        "-p", "tcp",
        "-s", ip,
        "--dport", str(protected_port),
        "-j", "ACCEPT"
    ])
    logging.info("Opened port %s for %s", protected_port, ip)



def close_protected_port(ip, protected_port):
    """Close the protected port using firewall rules."""
    subprocess.run([
        "iptables", "-D", "INPUT",
        "-p", "tcp",
        "-s", ip,
        "--dport", str(protected_port),
        "-j", "ACCEPT"
    ])
    logging.info("Closed port %s for %s", protected_port, ip)


def listen_for_knocks(sequence, window_seconds, protected_port):
    """Listen for knock sequence and open the protected port."""
    logger = logging.getLogger("KnockServer")
    logger.info("Listening for knocks: %s", sequence)
    logger.info("Protected port: %s", protected_port)

    # TODO: Create UDP or TCP listeners for each knock port.
    # TODO: Track each source IP and its progress through the sequence.
    # TODO: Enforce timing window per sequence.
    # TODO: On correct sequence, call open_protected_port().
    # TODO: On incorrect sequence, reset progress.
    sockets = {}

    # Create TCP listeners for each knock port
    for port in sequence:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen(5)
        sockets[s] = port

    while True:
        readable, _, _ = select.select(list(sockets.keys()), [], [], 1)

        for sock in readable:
            conn, addr = sock.accept()
            conn.close()

            ip = addr[0]
            port = sockets[sock]
            now = time.time()

            progress, start_time = knock_progress.get(ip, (0, now))

            # Reset if window expired
            if now - start_time > window_seconds:
                progress = 0
                start_time = now

            # Correct next knock
            if port == sequence[progress]:
                progress += 1
                logger.info("%s correct knock %s/%s", ip, progress, len(sequence))

                if progress == len(sequence):
                    open_protected_port(ip, protected_port)
                    progress = 0
                    start_time = now
            else:
                progress = 0
                start_time = now

            knock_progress[ip] = (progress, start_time)


def parse_args():
    parser = argparse.ArgumentParser(description="Port knocking server starter")
    parser.add_argument(
        "--sequence",
        default=",".join(str(port) for port in DEFAULT_KNOCK_SEQUENCE),
        help="Comma-separated knock ports",
    )
    parser.add_argument(
        "--protected-port",
        type=int,
        default=DEFAULT_PROTECTED_PORT,
        help="Protected service port",
    )
    parser.add_argument(
        "--window",
        type=float,
        default=DEFAULT_SEQUENCE_WINDOW,
        help="Seconds allowed to complete the sequence",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging()

    try:
        sequence = [int(port) for port in args.sequence.split(",")]
    except ValueError:
        raise SystemExit("Invalid sequence. Use comma-separated integers.")

    listen_for_knocks(sequence, args.window, args.protected_port)


if __name__ == "__main__":
    main()
