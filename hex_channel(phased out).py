import executor

class Parse:
    def __init__(self, hexStream):
        self.hexStream = hexStream
        self.commands = []

        self.COMMANDLENGTHS = {
            0x01: 3,
            0x02: 4,
            0x03: 6,
            0x04: 3,
            0x05: 2,
            0x06: 2,
            0x07: 1,
        }

    def hex(self):
        index = 0
        if self.hexStream[len(self.hexStream) - 1] != 255:
            print("Invalid command stream, missing 0xFF")
            return self.commands
        
        if self.hexStream[0] > 7:
            print("Invalid command stream, must start with a command or command not recognized")
            return self.commands

        received_length = len(self.hexStream)
        calculated_length = 0
        while index < len(self.hexStream):
            if self.hexStream[index] == 255:
                print("command complete")
                return self.commands

            command = self.hexStream[index]
            length = self.hexStream[index + 1] #byte storing the length of the command




            #check if command length is valid
            if command not in self.COMMANDLENGTHS:
                print(f"Invalid command {command}")
                return self.commands
            calculated_length += self.COMMANDLENGTHS[command]

            print(f"Command: {command}, Length: {length}, Expected length: {self.COMMANDLENGTHS[command]}")
            if length < self.COMMANDLENGTHS[command]:
                print(f"Invalid length {length} for command {command} index {index}, execution was aborted, please recheck the parameters")
                return []
            self.commands.append(self.hexStream[index:index + 2 + length])
            index = (index + 1) + (length + 1) #index pointer hops to where length pointer was (index + 1), then hops past the value of length (legth + 1)
        
        if received_length < calculated_length:
            print("The input stream is too short for the commands given, execution was aborted")
            return False
        
        #special case
        if command != 0x04 and received_length != calculated_length:
            print("Input stream mismatch for the commands given, execution was aborted")
            return[]




        return PassCommands().toExecutor(self.commands)

    
    def print_hex_commands(self, commands):
        for command in commands:
            hex_str = ', '.join([f"0x{hex(val)[2:].upper().zfill(2)}" for val in command])
            print(f"[{hex_str}]")

class PassCommands:
    session = executor.CommandSwitch()
    #TODO: Fix the readme
    # Bug reports:
    #   Breaks on very long inputs
    #   adds uneeded 0xFF in last byte

    render = [0x08, 0x00, 0xFF]


    def toExecutor(self, hex_command_streams):

        for hex_command_stream in hex_command_streams:
            hex_command_stream.append(0xFF)
            print(hex_command_stream)
            self.session.execute(hex_command_stream)

        self.session.execute(self.render) 