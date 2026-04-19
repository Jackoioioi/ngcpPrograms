# import sys
# import os
# from pathlib import Path

# # rooting
# root = Path(__file__).resolve().parent.parent.parent

# # possible paths for py libs
# sys.path.append(str(root))
# sys.path.append(str(root / "gcs-infrastructure"))
# sys.path.append(str(root / "gcs-infrastructure" / "Application"))
# sys.path.append(str(root / "gcs-infrastructure" / "lib" / "gcs-packet"))
# sys.path.append(str(root / "gcs-infrastructure" / "lib" / "gcs-packet" / "Packet"))
# sys.path.append(str(root / "gcs-infrastructure" / "lib" / "xbee-python" / "src"))

# # from Command import *
# # from Enum import *
# # from Infrastructure.InfrastructureInterface import *
# # from PacketLibrary.PacketLibrary import PacketLibrary
# # from Telemetry.Telemetry import Telemetry
# from Command import *
# from Enum import *
# from Application.Infrastructure.InfrastructureInterface import *
# from PacketLibrary.PacketLibrary import PacketLibrary
# from Telemetry.Telemetry import Telemetry

# PORT = "COM8"

# #Read gcs-infrastructure documentation to understand the implications of the following function calls

# PacketLibrary.SetVehicleMACAddress(Vehicle.MRA, "0013A20040F8063C")

# LaunchGCSXBee(PORT)

# command1 = Heartbeat(ConnectionStatus.Connected)
# command2 = EmergencyStop(0)
# command3 = Heartbeat(ConnectionStatus.Disconnected)

# SendCommand(command1, Vehicle.MRA)
# SendCommand(command2, Vehicle.MRA)
# SendCommand(command3, Vehicle.MRA)

# telemetry1 = ReceiveTelemetry()
# telemetry2 = ReceiveTelemetry()
# telemetry3 = ReceiveTelemetry()

# print(f"({telemetry1.Vehicle}, {telemetry1.MACAddress})")

# print(telemetry1)
# print(telemetry2)
# print(telemetry3)


import sys
import os
import signal
from pathlib import Path
import threading


# rooting
root = Path(__file__).resolve().parent.parent.parent

# possible paths for py libs
sys.path.append(str(root))
sys.path.append(str(root / "gcs-infrastructure"))
sys.path.append(str(root / "gcs-infrastructure" / "Application"))
sys.path.append(str(root / "gcs-infrastructure" / "lib" / "gcs-packet"))
sys.path.append(str(root / "gcs-infrastructure" / "lib" / "gcs-packet" / "Packet"))
sys.path.append(str(root / "gcs-infrastructure" / "lib" / "xbee-python" / "src"))

from Command import *
from Enum import *
from Application.Infrastructure.InfrastructureInterface import *
from PacketLibrary.PacketLibrary import PacketLibrary
from Telemetry.Telemetry import Telemetry

# Ctrl+C handler
def handle_exit(sig, frame):
    print("\nCtrl+C detected. Shutting down GCS...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# Telemetry fetch with timeout
def fetch_telemetry(name, timeout=5):
    print(f"Waiting for {name}...")
    result = [None]

    def _fetch():
        try:
            result[0] = ReceiveTelemetry()
        except Exception:
            pass

    thread = threading.Thread(target=_fetch)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if result[0]:
        print(f"Received {name}: {result[0]}")
    else:
        print(f"No telemetry received for {name} (timed out after {timeout}s)")
    
    return result[0]

# Configuration
PORT = "COM8"
TIMEOUT = 5  # seconds to wait for telemetry

PacketLibrary.SetVehicleMACAddress(Vehicle.MRA, "0013A20040F8063C")

LaunchGCSXBee(PORT)
print(f"GCS XBee launched on {PORT}")

# Send Commands
print("\n--- Sending Commands ---")
command1 = Heartbeat(ConnectionStatus.Connected)
command2 = EmergencyStop(0)
command3 = Heartbeat(ConnectionStatus.Disconnected)

SendCommand(command1, Vehicle.MRA)
print("Command 1 sent: Heartbeat (Connected)")

SendCommand(command2, Vehicle.MRA)
print("Command 2 sent: EmergencyStop")

SendCommand(command3, Vehicle.MRA)
print("Command 3 sent: Heartbeat (Disconnected)")

# Receive Telemetry
print("\n--- Waiting for Telemetry (Press Ctrl+C to stop) ---")
telemetry1 = fetch_telemetry("Telemetry 1", TIMEOUT)
telemetry2 = fetch_telemetry("Telemetry 2", TIMEOUT)
telemetry3 = fetch_telemetry("Telemetry 3", TIMEOUT)

# Print results
print("\n--- Telemetry Results ---")
for i, t in enumerate([telemetry1, telemetry2, telemetry3], 1):
    if t:
        print(f"Telemetry {i}: {t}")
    else:
        print(f"Telemetry {i}: No data received")

print("\nDone.")