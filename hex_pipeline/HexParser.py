import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# HexParser class assumes the input hex stream fully validified
class HexParser:
    END_OF_FILE = 0xFF
    
    def __init__(self, hexStream):
        self.hexStream = hexStream

    def hex(self):
        commands = []
        index = 0

        while index < len(self.hexStream):
            if self.hexStream[index] == 255:
                return commands 

            length = self.hexStream[index + 1] #byte storing the length of the command
            command = self.hexStream[index:index + 2 + length]
            command.append(self.END_OF_FILE)
            commands.append(command)

            index = (index + 1) + (length + 1) #index pointer hops to where length pointer was (index + 1), then hops past the value of length (legth + 1)


        return commands
