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
        print(f"Screen setup: {self.width}x{self.height}, color mode {self.color}")
        return [[" " for _ in range(self.width)] for _ in range(self.height)]

class MoveCursor(Executor):
    def __init__(self, hex_stream):
        super().__init__(hex_stream)
        self.x = self.hex_stream[2]
        self.y = self.hex_stream[3]

    def execute(self, screen):
        cursor_state = {"x": 0, "y": 0}
        if not self.integrity_check(2):
            return False

        # Check if target position is within screen bounds
        max_width = len(screen[0])
        max_height = len(screen)
        if not (0 <= self.x < max_width and 0 <= self.y < max_height):
            print(f"Error: Target position ({self.x}, {self.y}) is out of bounds.")
            return False

        # Update cursor state
        cursor_state["x"] = self.x
        cursor_state["y"] = self.y
        print(f"Cursor moved to ({self.x}, {self.y})")
        return True


class DrawCharacter(Executor):
    def __init__(self, hex_stream):
        super().__init__(hex_stream)
        self.x = self.hex_stream[2]
        self.y = self.hex_stream[3]
        self.color = self.hex_stream[4]
        self.char = self.hex_stream[5]

    def execute(self, screen):
        # Check the integrity of the command
        if not self.integrity_check(4):  # Expecting 4 arguments: x, y, color, char
            return False
        try:
            screen[self.x][self.y] = chr(self.char)
        except IndexError:
            print("Error: Coordinates out of bounds.")
        return True

class DrawLine(Executor):
    def __init__(self, hex_stream):
        super().__init__(hex_stream)
        self.x1 = self.hex_stream[2]
        self.y1 = self.hex_stream[3]
        self.x2 = self.hex_stream[4]
        self.y2 = self.hex_stream[5]
        self.color = self.hex_stream[6]
        self.char = self.hex_stream[7]

    def execute(self, screen):
        if not self.integrity_check(6):  # Expecting 6 arguments: x1, y1, x2, y2, color, char
            return False

        char_representation = chr(self.char)

        try:
            if self.y1 == self.y2:
                # Horizontal line
                for x in range(min(self.x1, self.x2), max(self.x1, self.x2) + 1):
                    screen[self.y1][x] = char_representation

            elif self.x1 == self.x2:
                # Vertical line
                for y in range(min(self.y1, self.y2), max(self.y1, self.y2) + 1):
                    screen[y][self.x1] = char_representation

            else:
                # Diagonal line using Bresenham's line algorithm
                dx = abs(self.x2 - self.x1)
                dy = abs(self.y2 - self.y1)
                sx = 1 if self.x1 < self.x2 else -1
                sy = 1 if self.y1 < self.y2 else -1
                err = dx - dy

                x, y = self.x1, self.y1
                while True:
                    screen[y][x] = char_representation
                    if x == self.x2 and y == self.y2:
                        break
                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x += sx
                    if e2 < dx:
                        err += dx
                        y += sy

        except IndexError:
            print("Error: Coordinates out of bounds.")
        return True
    


class RenderText(Executor):
    def __init__(self, hex_stream):
        super().__init__(hex_stream)
        self.x = self.hex_stream[2]
        self.y = self.hex_stream[3]
        self.color = self.hex_stream[4]
        self.text = self.hex_stream[5:hex_stream.index(0xFF)]

    def execute(self, screen):
        try:
            for i, char in enumerate(self.text):
                screen[self.y][self.x + i] = chr(char)

        except IndexError:
            print("Error: Coordinates out of bounds.")
        return True


class CommandSwitch: #controller
    def __init__(self):
        self.screenInit = False
        self.screen = None
        self.commandQueue = Queue()
        self.COMMANDS = {
            0x01: ScreenSetup,
            0x02: DrawCharacter,
            0x03: DrawLine,
            0x04: RenderText,
            0x05: MoveCursor,
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
        
        if command == 0x01:
            self.screen = self.COMMANDS[command](self.hex_stream).execute()
            self.screenInit = True
            return True
        
        if command not in self.COMMANDS:
            print("Command", command)
            raise ValueError("Command not recognized")
        if command == 0x08:
            return self.COMMANDS[command]().execute(self.commandQueue, self.screen)
       
        self.appendCommand()

        
        return is_done

class RenderAll(CommandSwitch):
    def execute(self, commandQueue, screen):
        while not commandQueue.empty():
            commandStream = commandQueue.get()
            command = commandStream[0]
            self.COMMANDS[command](commandStream).execute(screen)
            print("Executed command", command)
        print("\n".join("".join(row) for row in screen))
        return True