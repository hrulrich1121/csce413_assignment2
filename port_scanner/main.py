#!/usr/bin/env python3
"""
Port Scanner - Starter Template for Students
Assignment 2: Network Security

This is a STARTER TEMPLATE to help you get started.
You should expand and improve upon this basic implementation.

TODO for students:
1. Implement multi-threading for faster scans
2. Add banner grabbing to detect services
3. Add support for CIDR notation (e.g., 192.168.1.0/24)
4. Add different scan types (SYN scan, UDP scan, etc.)
5. Add output formatting (JSON, CSV, etc.)
6. Implement timeout and error handling
7. Add progress indicators
8. Add service fingerprinting
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import sys
import argparse


def scan_port(target, port, timeout=1.0):
    """
    Scan a single port on the target host

    Args:
        target (str): IP address or hostname to scan
        port (int): Port number to scan
        timeout (float): Connection timeout in seconds

    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        # TODO: Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: Set timeout
        s.settimeout(timeout)
        # TODO: Try to connect to target:port
        result = s.connect_ex((target,port))
        # TODO: Close the socket
        # TODO: Return True if connection successful
        if result == 0:
            try:
                s.send(b"\r\n")
                banner = s.recv(1024).decode(errors="ignore").strip()
                print(banner)
            except:
                banner = ""
            return True
        else:
            pass
        
        s.close()
        return False

    except (socket.timeout, OSError):
        return False


def scan_range(target, start_port, end_port, max_threads=100, timeout=1.0):
    """
    Scan a range of ports on the target host

    Args:
        target (str): IP address or hostname to scan
        start_port (int): Starting port number
        end_port (int): Ending port number

    Returns:
        list: List of open ports
    """
    open_ports = []

    print(f"[*] Scanning {target} from port {start_port} to {end_port}")
    print(f"[*] This may take a while...")

    # TODO: Implement the scanning logic
    # Hint: Loop through port range and call scan_port()
    # Hint: Consider using threading for better performance

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all port scan tasks
        future_to_port = {
            executor.submit(scan_port, target, port, timeout): port
            for port in range(start_port, end_port + 1)
        }

        # Process results as they complete
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    print(f"[+] Port {port} is open")
                    open_ports.append(port)
            except Exception:
                pass

    return sorted(open_ports)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Simple Multi-threaded TCP Port Scanner"
    )

    parser.add_argument(
        "target",
        help="Target IP address or hostname"
    )

    parser.add_argument(
        "-p", "--ports",
        help="Port range (format: start-end). Default: 1-1024",
        default="1-1024"
    )

    parser.add_argument(
        "-t", "--threads",
        help="Number of threads (default: 100)",
        type=int,
        default=100
    )

    parser.add_argument(
        "--timeout",
        help="Socket timeout in seconds (default: 1.0)",
        type=float,
        default=1.0
    )

    args = parser.parse_args()

    # Validate and parse port range
    try:
        start_port, end_port = map(int, args.ports.split("-"))
        if not (0 < start_port <= end_port <= 65535):
            raise ValueError
    except ValueError:
        print("[-] Invalid port range. Use format start-end (e.g., 20-80)")
        sys.exit(1)

    # Validate thread count
    if args.threads <= 0 or args.threads > 1000:
        print("[-] Thread count must be between 1 and 1000")
        sys.exit(1)

    # Validate target resolution
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("[-] Could not resolve hostname.")
        sys.exit(1)


    print(f"[*] Starting port scan on {target_ip}")

    open_ports = scan_range(
    target_ip,
    start_port,
    end_port,
    max_threads=args.threads,
    timeout=args.timeout
)


    print(f"\n[+] Scan complete!")
    print(f"[+] Found {len(open_ports)} open ports:")
    for port in open_ports:
        print(f"    Port {port}: open")


if __name__ == "__main__":
    main()
