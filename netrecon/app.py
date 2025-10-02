from flask import Flask, render_template, request
from modules.port_scanner import scan_tcp_connect
from modules.service_detector import detect
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

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

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        host = request.form["host"].strip()
        ports = parse_ports(request.form.get("ports","1-1024"))
        timeout = float(request.form.get("timeout","1.0"))
        workers = int(request.form.get("workers","200"))
        scan = scan_tcp_connect(host, ports, workers=workers, timeout=timeout)
        details = []
        for p, st in scan.items():
            if st == "open":
                details.append(detect(host, p))
        return render_template("result.html", host=host, scan=scan, details=details)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)