import re, subprocess, shutil
from .banner_grabber import grab_banner

SIGS = [
    (r"SSH", "OpenSSH"),
    (r"HTTP/1\.[01]", "HTTP"),
    (r"SMTP", "SMTP"),
    (r"IMAP", "IMAP"),
    (r"POP3", "POP3"),
    (r"FTP", "FTP"),
    (r"Redis", "Redis"),
    (r"MongoDB", "MongoDB"),
]

def detect(host: str, port: int) -> dict:
    banner = grab_banner(host, port)
    svc = "unknown"
    for pat, name in SIGS:
        if re.search(pat, banner, re.I):
            svc = name
            break
    version = None
    if shutil.which("nmap"):
        try:
            out = subprocess.check_output(["nmap","-sV","-p",str(port), host], text=True)
            m = re.search(rf"{port}/tcp\s+open\s+(\S+)(?:\s+([\w\.\-]+))?", out)
            if m:
                svc = m.group(1)
                version = m.group(2)
        except Exception:
            pass
    return {"port": port, "service": svc, "version": version, "banner": banner[:256]}