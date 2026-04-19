from Enum import Vehicle

# Can be used to implement the serial port manager for other radio modules

class CommandInterface:
    # FORMAT_STRING = # More information here: https://docs.python.org/3/library/struct.html
    PACKET_ID = 0

    def __init__(self):
        self.PacketID = CommandInterface.GeneratePacketID()
        self.Vehicle = Vehicle.UNKNOWN

    def EncodePacket(self) -> bytes:
        """Encode data packet

        Args:
          data: Data passed into given command

        Returns:
          Encoded data string
        """
        pass

    @staticmethod
    def DecodePacket(encoded_string):
        """Decodes data packet
        
        Args:
          Encoded data packet

        Returns:
          Data from encoded data packet
        """
        pass
    
    @staticmethod
    def GeneratePacketID():
        CurrentPacketID = CommandInterface.PACKET_ID

        CommandInterface.PACKET_ID += 1

        return CurrentPacketID