import socket, ssl, threading, json
from connection_manager import ConnectionManager
from room_manager import RoomManager
from message_encryption import MessageEncryption, encode64

HOST = "0.0.0.0"
PORT = 8443

TLS_CERT = "certs/server/server.crt"
TLS_KEY  = "certs/server/server.key"
CA_CERT  = "certs/ca/ca.crt"

# Require client cert
ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ctx.load_cert_chain(certfile=TLS_CERT, keyfile=TLS_KEY)
ctx.load_verify_locations(CA_CERT)
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.minimum_version = ssl.TLSVersion.TLSv1_2

cm = ConnectionManager()
rm = RoomManager()

def handle_client(conn: ssl.SSLSocket, addr):
    try:
        # First message must be JSON: {"name": "...", "room": "...", "passphrase": "..."}
        raw = conn.recv(4096)
        meta = json.loads(raw.decode())
        name = meta.get("name","anon")
        room = meta.get("room","lobby")
        pwd  = meta.get("passphrase","secret")
        enc  = MessageEncryption(pwd)

        cm.register(conn, name, room)
        rm.join(conn, room)

        conn.sendall(b"WELCOME\n")
        while True:
            data = conn.recv(8192)
            if not data:
                break
            # broadcast encrypted frame as base64 string with sender name prefix
            frame = f"[{name}] ".encode() + data
            # already encrypted blob expected from client; forward as-is to peers
            cm.broadcast(conn, frame)
    except Exception as e:
        try:
            conn.sendall(f"ERR: {e}\n".encode())
        except Exception:
            pass
    finally:
        try:
            # ensure leaving room
            for r in list(rm.rooms.keys()):
                rm.leave(conn, r)
            cm.unregister(conn)
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(50)
        with ctx.wrap_socket(s, server_side=True) as ss:
            print(f"SecureChatServer listening on {HOST}:{PORT}")
            while True:
                client, addr = ss.accept()
                t = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
                t.start()

if __name__ == "__main__":
    main()
