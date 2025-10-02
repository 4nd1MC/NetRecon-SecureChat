import socket

def grab_banner(host: str, port: int, timeout: float = 2.0) -> str:
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            try:
                data = s.recv(1024)
                if data:
                    return data.decode(errors="ignore").strip()
            except Exception:
                pass
            # Try simple probes for common services
            for probe in [b"\r\n", b"HEAD / HTTP/1.0\r\n\r\n", b"QUIT\r\n"]:
                try:
                    s.sendall(probe)
                    data = s.recv(1024)
                    if data:
                        return data.decode(errors="ignore").strip()
                except Exception:
                    continue
    except Exception:
        return ""
    return ""