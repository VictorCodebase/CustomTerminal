import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# HexParser class assumes the input hex stream fully validified
class HexParser:
    END_OF_FILE = 0xFF
    
    def __init__(self, hex_stream):
        self.hex_stream = hex_stream

    def hex(self):
        commands = []
        index = 0

        while index < len(self.hex_stream):
            if self.hex_stream[index] == self.END_OF_FILE:
                return commands 

            length = self.hex_stream[index + 1] #byte storing the length of the command
            command = self.hex_stream[index:index + 2 + length]
            command.append(self.END_OF_FILE)
            commands.append(command)

            index = (index + 1) + (length + 1) #index pointer hops to where length pointer was (index + 1), then hops past the value of length (legth + 1)


        return commands
