from Command.CommandInterface import CommandInterface

import json
import struct

class SearchArea(CommandInterface):
    FORMAT_STRING = "=BI"
    COMMAND_ID = 6

    def __init__(self, Coordinates: list):
        super().__init__()

        self.Coordinates = Coordinates

    def EncodePacket(self) -> bytes:
        """Encode data packet

        Args:
            coordinates: List of (x, y) tuples to encode as doubles

        Returns:
            Encoded data bytes
        """
        # Start with Command ID and Packet IDs
        Header = struct.pack(self.FORMAT_STRING, SearchArea.COMMAND_ID, self.PacketID)

        # Flatten the list of tuples into a single list of floats
        FlattenedCoordinates = [Item for Coordinate in self.Coordinates for Item in Coordinate]

        # Build the format string: two bytes for header, then 2 doubles per coordinate
        FormatString = f"{len(FlattenedCoordinates)}d"

        if FlattenedCoordinates:
            CoordinateBytes = struct.pack(FormatString, *FlattenedCoordinates)
            EncodedString = Header + CoordinateBytes
        else:
            EncodedString = Header

        return EncodedString

    @staticmethod
    def DecodePacket(EncodedString) -> int:
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet

        Returns:
            Data from encoded data packet
        """
        CoordinateCount = (len(EncodedString) - 2) // 16

        if CoordinateCount > 6:
            print("Too many coordinates")

        FormatString = SearchArea.FORMAT_STRING + "dd" * int(CoordinateCount)

        ExpectedLength = struct.calcsize(FormatString)

        if len(EncodedString) != ExpectedLength:
            raise ValueError(f"Encoded string length {len(EncodedString)} does not match expected {ExpectedLength} for format '{FormatString}'")

        UnpackedData = struct.unpack(FormatString, EncodedString)

        Coordinates = []

        for i in range(0, (CoordinateCount * 2), 2):
            Coordinates.append((UnpackedData[(i + 2)], UnpackedData[(i + 3)]))

        JSONData = {
            "Command ID": UnpackedData[0],
            "Packet ID": UnpackedData[1],
            "Coordinates": Coordinates
        }

        return json.dumps(JSONData)