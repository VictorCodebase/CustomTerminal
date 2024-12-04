
class Executor:

    def __init__(self, hex_stream):
        self.hex_stream = hex_stream

        self.command = self.hex_stream[0]
        self.instructionLength = self.hex_stream[1] # to check stream integrity
        self.trailingHex = self.hex_stream[-1] # to check stream integrity


    def integrity_check(self, expectedLength):
        if self.instructionLength != expectedLength:
            raise ValueError(f"Expected length {expectedLength}, but got {self.instructionLength}")
        if self.trailingHex != 0xFF:
            print("Trailing",self.trailingHex)
            raise ValueError("Trailing byte is not 0xFF")
        return True
            

class ScreenSetup(Executor):
    def __init__(self, hex_stream):
        super().__init__(hex_stream)       
        self.width = self.hex_stream[2]
        self.height = self.hex_stream[3]
        self.color = self.hex_stream[4]

    def execute(self):
        if not self.integrity_check(3):
            return False
        
        return True
    

class CommandSwitch:
    def __init__(self, hex_stream):
        self.hex_stream = hex_stream
        self.screenInit = False
        self.COMMANDS = {
            0x01: ScreenSetup,
            #0x2: 0x2,
            # "draw_line": 0x3,
            # "render_text": 0x4,
            # "cursor_movement": 0x5,
            # "draw_at_cursor": 0x6,
            # "clear_screen": 0x7
        }

    def execute(self):
        command = self.hex_stream[0]
        is_done = False
        if command in self.COMMANDS:
            print("command found")
            is_done = self.COMMANDS[command](self.hex_stream).execute()
        else:
            raise ValueError("Command not recognized")
        
        if is_done and command == 0x01:
            self.screenInit = True
        
        return is_done
