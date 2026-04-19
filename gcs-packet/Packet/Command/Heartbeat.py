from Command.CommandInterface import CommandInterface
from Enum.ConnectionStatus import ConnectionStatus

import json
import struct

class Heartbeat(CommandInterface):
    FORMAT_STRING = "BIH"
    COMMAND_ID = 1

    def __init__(self, CurrentConnectionStatus: ConnectionStatus):
        super().__init__()

        self.CurrentConnectionStatus = CurrentConnectionStatus

    def EncodePacket(self) -> bytes:
        """Encode data packet

        Args:
            connection_status: Status for emergency stop: 0 = Enable Emergency Stop, 1 = Disable Emergency Stop

        Returns:
            Encoded data bytes
        """
        EncodedString = struct.pack(Heartbeat.FORMAT_STRING, Heartbeat.COMMAND_ID, self.PacketID, self.CurrentConnectionStatus.value)

        return EncodedString

    @staticmethod
    def DecodePacket(EncodedString) -> int:
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet

        Returns:
            Data from encoded data packet
        """
        ExpectedSize = 10

        if len(EncodedString) != ExpectedSize:

            print("Invalid String Size in hb")

        UnpackedData = struct.unpack(Heartbeat.FORMAT_STRING, EncodedString)

        JSONData = {
            "Command ID": UnpackedData[0],
            "Packet ID": UnpackedData[1],
            "Connection Status": UnpackedData[2]
        }

        return json.dumps(JSONData)
