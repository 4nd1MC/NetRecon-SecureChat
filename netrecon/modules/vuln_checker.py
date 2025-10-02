# Very lightweight heuristic. Expand per needs.
KNOWN = {
    ("http", "Apache", "2.4.49"): "Path traversal RCE (CVE-2021-41773)",
    ("http", "Apache", "2.4.50"): "Path traversal RCE (CVE-2021-42013)",
    ("http", "OpenSSL", "1.0.1"): "Heartbleed (CVE-2014-0160)",
}

def basic_check(service: str | None, version: str | None) -> list[str]:
    hits = []
    if not service or not version:
        return hits
    for (_, name, ver), note in KNOWN.items():
        if name.lower() in service.lower() and version.startswith(ver):
            hits.append(note)
    return hits