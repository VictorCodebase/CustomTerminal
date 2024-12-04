from queue import Queue

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

class CursorMove(Executor):
    def __init__(self, hex_stream):
        super().__init__(hex_stream)
        self.x = self.hex_stream[2]
        self.y = self.hex_stream[3]

    def execute(self):
        # Check the integrity of the command
        if not self.integrity_check(2):  # Expecting 2 arguments: x and y
            return False
        # Perform the cursor movement (you can replace this with your actual implementation)
        print(f"Cursor moved to position ({self.x}, {self.y})")
        return True

    

class CommandSwitch: #controller
    def __init__(self):
        self.screenInit = False
        self.commandQueue = Queue()
        self.COMMANDS = {
            0x01: ScreenSetup,
            0x05: CursorMove,
            0x08: RenderAll,
            # "draw_line": 0x3,
            # "render_text": 0x4,
            # "cursor_movement": 0x5,
            # "draw_at_cursor": 0x6,
            # "clear_screen": 0x7
        }
    def appendCommand(self):  
        if self.hex_stream[0] == 0x01:
            self.screenInit = True      
        self.commandQueue.put(self.hex_stream)
        print("Command appended to queue, please enter another command")

    def execute(self, hex_stream):
        self.hex_stream = hex_stream
        command = self.hex_stream[0]
        is_done = False

        if not self.screenInit and command != 0x01:
            print("Screen not initialized")
            return False
        if command not in self.COMMANDS:
            print("Command", command)
            raise ValueError("Command not recognized")
        if command == 0x08:
            return self.COMMANDS[command]().execute(self.commandQueue)
       
        self.appendCommand()

        
        return is_done

class RenderAll(CommandSwitch):
    def execute(self, commandQueue):
        while not commandQueue.empty():
            commandStream = commandQueue.get()
            command = commandStream[0]
            self.COMMANDS[command](commandStream).execute()
            print("Executed command", command)
        return True