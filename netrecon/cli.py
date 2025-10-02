#!/usr/bin/env python3
import argparse, json
from modules.port_scanner import scan_tcp_connect
from modules.service_detector import detect
from modules.banner_grabber import grab_banner

def parse_ports(s: str):
    out = set()
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a,b = part.split("-",1)
            out.update(range(int(a), int(b)+1))
        else:
            out.add(int(part))
    return sorted(out)

def main():
    ap = argparse.ArgumentParser(description="NetRecon CLI (Linux)")
    ap.add_argument("host")
    ap.add_argument("-p","--ports", default="1-1024")
    ap.add_argument("--timeout", type=float, default=1.0)
    ap.add_argument("--workers", type=int, default=200)
    args = ap.parse_args()

    ports = parse_ports(args.ports)
    scan = scan_tcp_connect(args.host, ports, workers=args.workers, timeout=args.timeout)
    details = []
    for p, st in scan.items():
        if st == "open":
            details.append(detect(args.host, p))
    result = {"host": args.host, "scan": scan, "details": details}
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()