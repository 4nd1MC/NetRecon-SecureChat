import subprocess, shutil

def ping_sweep(cidr: str) -> list[str]:
    # Use nmap -sn if available, else fallback to fping if present, else empty.
    if shutil.which("nmap"):
        out = subprocess.check_output(["nmap","-sn",cidr], text=True, stderr=subprocess.DEVNULL)
        hosts = []
        for line in out.splitlines():
            if line.startswith("Nmap scan report for "):
                host = line.split("for ",1)[1].strip()
                hosts.append(host)
        return hosts
    return []