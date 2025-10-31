#!/usr/bin/env python3
import argparse
import socket
import sys

def parse_ports(s):
    out = []
    for part in s.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            p = int(part)
        except ValueError:
            raise ValueError(f"Invalid port: {part}")
        if p < 1 or p > 65535:
            raise ValueError(f"Port out of range: {p}")
        out.append(p)
    return out

def is_valid_host(host):
    # Accept hostname or IP. For IP check:
    try:
        socket.inet_pton(socket.AF_INET, host)
        return True
    except OSError:
        pass
    try:
        socket.inet_pton(socket.AF_INET6, host)
        return True
    except OSError:
        pass
    # fallback: don't strictly validate hostnames here (DNS will fail later)
    return True

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("host", help="target host (IP or hostname)")
    p.add_argument("--ports", default="11,8,1993,32,2025", help="comma-separated knock ports")
    p.add_argument("--timeout", type=int, default=10, help="sequence timeout seconds")
    p.add_argument("--use-hmac", action="store_true", help="enable HMAC tokens")
    args = p.parse_args(argv)

    host = args.host.strip()
    if not is_valid_host(host):
        print("Invalid host:", host); sys.exit(2)

    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print("Ports error:", e); sys.exit(2)

    if args.timeout <= 0:
        print("Timeout must be > 0"); sys.exit(2)

    print("Parsed values:")
    print(" host =", host)
    print(" ports =", ports)
    print(" timeout =", args.timeout)
    print(" use_hmac =", args.use_hmac)

if __name__ == "__main__":
    main()
