import socket, ssl, sys, json, threading
from message_encryption import MessageEncryption, decode64, encode64

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8443

TLS_CERT = "certs/client/client.crt"
TLS_KEY  = "certs/client/client.key"
CA_CERT  = "certs/ca/ca.crt"

def recv_loop(sock: ssl.SSLSocket, enc: MessageEncryption):
    while True:
        data = sock.recv(8192)
        if not data:
            print("Disconnected")
            break
        try:
            # Expect "[name] " prefix then base64 blob
            if data.startswith(b"["):
                prefix, rest = data.split(b"] ",1)
                # rest is encrypted blob in base64 from peers
                try:
                    blob = rest.strip()
                    print(f"{prefix.decode()}] {blob.decode()}")
                except Exception:
                    print(data.decode(errors="ignore"), end="")
            else:
                print(data.decode(errors="ignore"), end="")
        except Exception as e:
            print(f"[recv error] {e}")

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "client"
    room = sys.argv[2] if len(sys.argv) > 2 else "lobby"
    passphrase = sys.argv[3] if len(sys.argv) > 3 else "secret"

    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
    ctx.load_cert_chain(certfile=TLS_CERT, keyfile=TLS_KEY)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2

    enc = MessageEncryption(passphrase)

    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        with ctx.wrap_socket(sock, server_hostname="localhost") as ssock:
            hello = json.dumps({"name": name, "room": room, "passphrase": passphrase}).encode()
            ssock.sendall(hello)

            t = threading.Thread(target=recv_loop, args=(ssock, enc), daemon=True)
            t.start()

            print("Type messages. Ctrl+C to exit.")
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                blob = enc.encrypt(line.encode())
                b64 = encode64(blob).encode()
                ssock.sendall(b64 + b"\n")

if __name__ == "__main__":
    main()