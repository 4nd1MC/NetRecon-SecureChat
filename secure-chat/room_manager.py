import threading
from collections import defaultdict

class RoomManager:
    def __init__(self):
        self.lock = threading.RLock()
        self.rooms = defaultdict(set)  # room -> set(sock)

    def join(self, sock, room: str):
        with self.lock:
            self.rooms[room].add(sock)

    def leave(self, sock, room: str):
        with self.lock:
            if sock in self.rooms.get(room, set()):
                self.rooms[room].remove(sock)
                if not self.rooms[room]:
                    self.rooms.pop(room, None)

    def members(self, room: str):
        with self.lock:
            return list(self.rooms.get(room, set()))