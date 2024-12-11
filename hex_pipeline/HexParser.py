import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HexParser:
    END_OF_FILE = 0xFF
    
    def __init__(self, hexStream):
        self.hexStream = hexStream

    def hex(self):
        commands = []
        index = 0

        while index < len(self.hexStream):
            if self.hexStream[index] == 255:
                print("commands parsed successfully")
                # print("export commands: ", self.commands)
                return commands 

            length = self.hexStream[index + 1] #byte storing the length of the command

            try:
                command = self.hexStream[index:index + 2 + length]
                command.append(self.END_OF_FILE)
                index = (index + 1) + (length + 1) #index pointer hops to where length pointer was (index + 1), then hops past the value of length (legth + 1)
                # print("Added: ", command)
                commands.append(command)
            except:
                logging.error("Parsing error")
                return False
        return commands
