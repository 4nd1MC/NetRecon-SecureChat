import threading

class ConnectionManager:
    def __init__(self):
        self.lock = threading.RLock()
        self.clients = {}   # sock -> {"name": str, "room": str}

    def register(self, sock, name: str, room: str = "lobby"):
        with self.lock:
            self.clients[sock] = {"name": name, "room": room}

    def unregister(self, sock):
        with self.lock:
            self.clients.pop(sock, None)

    def set_room(self, sock, room: str):
        with self.lock:
            if sock in self.clients:
                self.clients[sock]["room"] = room

    def broadcast(self, from_sock, data: bytes):
        # send to everyone in same room
        with self.lock:
            if from_sock not in self.clients:
                return
            room = self.clients[from_sock]["room"]
            targets = [s for s, info in self.clients.items() if info["room"] == room and s is not from_sock]
        for s in targets:
            try:
                s.sendall(data)
            except Exception:
                pass

    def list_in_room(self, room: str):
        with self.lock:
            return [(s, info["name"]) for s, info in self.clients.items() if info["room"] == room]