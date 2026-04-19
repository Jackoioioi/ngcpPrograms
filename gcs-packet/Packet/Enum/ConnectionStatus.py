from enum import Enum

class ConnectionStatus(Enum):
    Connected = 0
    Unstable = 1
    Disconnected = 2