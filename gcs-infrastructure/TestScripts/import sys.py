# import sys
# import os
# from pathlib import Path
# import json

# # 1. Rooting logic
# root = Path(__file__).resolve().parent.parent.parent

# # 2. Add paths to sys.path
# sys.path.append(str(root))
# sys.path.append(str(root / "gcs-infrastructure"))
# sys.path.append(str(root / "gcs-infrastructure" / "Application"))
# sys.path.append(str(root / "gcs-packet"))
# # Adding the 'Packet' folder specifically allows us to import PacketLibrary directly
# sys.path.append(str(root / "gcs-packet" / "Packet"))

# # 3. Imports
# from Command import *
# from Enum import *
# from Application.Infrastructure.InfrastructureInterface import *
# from Telemetry.Telemetry import Telemetry

# # FIX: Import the CLASS from the MODULE
# # Since you added the 'Packet' folder to sys.path, you import from the filename
# from PacketLibrary import PacketLibrary

# # 4. Configuration
# PORT = "COM8"
# GCS_MAC = "0013A20042B3A0EC"

# # Set the MAC Address
# # If this still gives an AttributeError, it means the class name isn't 'PacketLibrary' 
# # inside the file, but based on your previous logs, this is the correct path.
# PacketLibrary.SetGCSMACAddress(GCS_MAC)

# # 5. Launch Hardware
# try:
#     LaunchVehicleXBee(PORT)
#     print(f"Hardware initialized on {PORT}")
# except Exception as e:
#     print(f"Failed to launch XBee: {e}")
#     sys.exit(1)

# # 6. Receive Data
# print("Waiting for data1...")
# Command1 = ReceiveCommand()
# print(f"Rcv 1: {Command1}")

# print("Waiting for data2...")
# Command2 = ReceiveCommand()
# print(f"Rcv 2: {Command2}")

# print("Waiting for data3...")
# Command3 = ReceiveCommand()
# print(f"Rcv 3: {Command3}")


# # 7. Process and Send Telemetry
# commands = [Command1, Command2, Command3]
# for cmd in commands:
#     if cmd:
#         try:
#             data = json.loads(cmd)
#             # Create telemetry using IDs from the received JSON
#             t = Telemetry(
#                 data["Command ID"], 
#                 data["Packet ID"], 
#                 100, 0, 0, 0, 45, 0.5, 0, (1, 2), 0, 0, 1.0, 1.0, 0
#             )
#             SendTelemetry(t)
#             print(f"Telemetry sent for Packet ID: {data['Packet ID']}")
#         except (json.JSONDecodeError, KeyError) as e:
#             print(f"Processing Error: {e}")
#     else:
#         print("Skipping empty command.")

import sys
import os
from pathlib import Path
import json

# 1. Rooting logic
root = Path(__file__).resolve().parent.parent.parent

# 2. Setup paths
sys.path.append(str(root))
sys.path.append(str(root / "gcs-infrastructure"))
sys.path.append(str(root / "gcs-infrastructure" / "Application"))
sys.path.append(str(root / "gcs-infrastructure" / "lib" / "gcs-packet"))
sys.path.append(str(root / "gcs-infrastructure" / "lib" / "gcs-packet" / "Packet"))
sys.path.append(str(root / "gcs-infrastructure" / "lib" / "xbee-python" / "src"))

# 3. Imports
from Command import *
from Enum import *
from Application.Infrastructure.InfrastructureInterface import *
from PacketLibrary.PacketLibrary import PacketLibrary
from Telemetry.Telemetry import Telemetry

# 4. Configuration
PORT = "COM8"
GCS_MAC = "0013A20042B3A0EC"

PacketLibrary.SetGCSMACAddress(GCS_MAC)
print(f"GCS MAC Address set to: {PacketLibrary.GetGCSMACAddress()}")

# 5. Launch Hardware
try:
    LaunchVehicleXBee(PORT)
    print(f"Hardware initialized on {PORT}")
except Exception as e:
    print(f"Hardware Launch Error: {e}")
    sys.exit(1)

# 6. Receive and Process Loop
print("\n--- Listening for Radio Data (Press Ctrl+C to stop) ---")

def fetch_data(name):
    print(f"Waiting for {name}...")
    result = ReceiveCommand()
    print(f"Rcv {name}: {result}")
    return result

cmd1 = fetch_data("Data 1")
cmd2 = fetch_data("Data 2")
cmd3 = fetch_data("Data 3")

# 7. Telemetry Loop
for idx, raw in enumerate([cmd1, cmd2, cmd3], 1):
    if raw:
        try:
            data = json.loads(raw)
            t = Telemetry(
                data.get("Command ID", 0),
                data.get("Packet ID", 0),
                100, 0, 0, 0, 45, 0.5, 0, (1, 2), 0, 0, 1.0, 1.0, 0
            )
            SendTelemetry(t)
            print(f"Telemetry {idx} sent for Packet ID: {data.get('Packet ID')}")
        except Exception as e:
            print(f"Error processing Packet {idx}: {e}")

print("\nDone.")