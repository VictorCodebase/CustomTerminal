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
            raise ValueError("Trailing byte is not 0xFF")
        return True
    



class ScreenSetup(Executor):

    def __init__(self, hex_stream):
        super().__init__(hex_stream)       
        self.width = self.hex_stream[2]
        self.height = self.hex_stream[3]
        self.color_mode_index = self.hex_stream[4]
        self.color_mode_map = {}

        #set the color mode
        self.color_mode_options = {
            0x00: self.generate_mono_colors,
            0x01: self.generate_16_colors,
            0x02: self.generate_256_colors
            }

    def execute(self):
        if not self.integrity_check(3):
            return False

        print(f"Screen setup: {self.width}x{self.height}, color mode {self.color_mode_index}")
        try:
            self.color_mode_map = self.color_mode_options[self.color_mode_index]()
        except KeyError:
            print(f"No color mode exists for the provided color_mode_index: {self.color_mode_map}")
            return False
        return [[[" " for _ in range(self.width)] for _ in range(self.height)], self.color_mode_map]
    
    def generate_mono_colors(self):
        return {"text": "", "reset": "\033[0m"}

    def generate_16_colors(self):
        base_colors = list(range(30, 38))  # 0–7 standard colors (30–37)
        bright_colors = list(range(90, 98))  # 8–15 bright colors (90–97)

        color_map = {}
        for i, code in enumerate(base_colors + bright_colors):
            color_map[i] = f"\033[{code}m"
        color_map["reset"] = "\033[0m"  # Reset color
        return color_map
    
    def generate_256_colors(self):
        color_map = {}
        for i in range(256):
            color_map[i] = f"\033[38;5;{i}m"
        color_map["reset"] = "\033[0m"  # Reset color
        return color_map

class MoveCursor(Executor):
    def __init__(self, color_mode_map, hex_stream):
        super().__init__(hex_stream)
        self.x = self.hex_stream[2]
        self.y = self.hex_stream[3]
        

    def execute(self, screen, cursor_state):
        if not self.integrity_check(2):
            return False

        # Check if target position is within screen bounds
        max_width = len(screen[0])
        max_height = len(screen)
        if not (0 <= self.x < max_width and 0 <= self.y < max_height):
            print(f"Error: Target position ({self.x}, {self.y}) is out of bounds. Try x values between 0 and {max_width - 1}, and y values between 0 and {max_height - 1}")
            return False

        # Update cursor state
        cursor_state["x"] = self.x
        cursor_state["y"] = self.y
        print(f"> Cursor moved to ({self.x}, {self.y})")
        return True


class DrawCharacter(Executor):
    def __init__(self, color_mode_map, hex_stream):
        super().__init__(hex_stream)
        self.x = self.hex_stream[2]
        self.y = self.hex_stream[3]
        self.color = self.hex_stream[4]
        self.char = self.hex_stream[5]
        self.color_mode_map = color_mode_map

    def execute(self, screen, cursor_state):
        # Check the integrity of the command
        if not self.integrity_check(4):  # Expecting 4 arguments: x, y, color, char
            return False
        if self.color not in self.color_mode_map:
            print(f"Error: Invalid color mode {self.color}")
            return False
        try:
            startx = self.x + cursor_state["x"]
            starty = self.y + cursor_state["y"]
            max_width = len(screen[0])
            max_height = len(screen)
            print(f"> Drawing character {chr(self.char)} at ({startx}, {starty}) from cursor position {cursor_state}")
            screen[self.y + cursor_state["y"]][self.x + cursor_state["x"]] = (f"{self.color_mode_map[int(self.color)]} {chr(self.char)} {self.color_mode_map['reset']}")
        except IndexError:
            print(f"Error: draw_char coordinates out of bounds.")
            return False
        return True
class DrawLine(Executor):
    def __init__(self, color_mode_map, hex_stream):
        super().__init__(hex_stream)
        self.x1 = self.hex_stream[2]
        self.y1 = self.hex_stream[3]
        self.x2 = self.hex_stream[4]
        self.y2 = self.hex_stream[5]
        self.color = self.hex_stream[6]
        self.char = self.hex_stream[7]
        self.color_mode_map = color_mode_map

    def execute(self, screen, cursor_state):
        if not self.integrity_check(6):  # Expecting 6 arguments: x1, y1, x2, y2, color, char
            return False
        
        if self.color not in self.color_mode_map:
            print(f"Error: Invalid color mode {self.color}")
            return False

        # Adjust coordinates based on cursor position
        start_x = self.x1 + cursor_state["x"]
        start_y = self.y1 + cursor_state["y"]
        end_x = self.x2 + cursor_state["x"]
        end_y = self.y2 + cursor_state["y"]

        char_representation = f"{self.color_mode_map[int(self.color)]}{chr(self.char)}{self.color_mode_map['reset']}"

        try:
            # Draw a horizontal line
            if start_y == end_y:
                for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                    screen[start_y][x] = char_representation

            # Draw a vertical line
            elif start_x == end_x:
                for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                    screen[y][start_x] = char_representation

            # Draw a diagonal line using Bresenham's algorithm
            else:
                dx = abs(end_x - start_x)
                dy = abs(end_y - start_y)
                sx = 1 if start_x < end_x else -1
                sy = 1 if start_y < end_y else -1
                err = dx - dy

                x, y = start_x, start_y
                while True:
                    screen[y][x] = char_representation
                    if x == end_x and y == end_y:
                        break
                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x += sx
                    if e2 < dx:
                        err += dx
                        y += sy

            print(f"> Line drawn from ({start_x}, {start_y}) to ({end_x}, {end_y}) relative to cursor position {cursor_state}")
        except IndexError:
            print("Error: draw_line coordinates out of bounds.")
        return True



class RenderText(Executor):
    def __init__(self, color_mode_map, hex_stream):
        super().__init__(hex_stream)
        self.x = self.hex_stream[2]
        self.y = self.hex_stream[3]
        self.color = self.hex_stream[4]
        self.text = self.hex_stream[5:hex_stream.index(0xFF)]
        self.color_mode_map = color_mode_map

    def execute(self, screen, cursor_state):
        startx = self.x + cursor_state["x"]
        starty = self.y + cursor_state["y"]

        if self.color not in self.color_mode_map:
            print(f"Error: Invalid color mode {self.color}")
            return False
        
        try:
            for i, char in enumerate(self.text):
                screen[starty][startx + i] = f"{self.color_mode_map[int(self.color)]}{chr(char)}{self.color_mode_map['reset']}"
            print(f"> Text rendered at ({startx}, {starty}) from cursor position {cursor_state}")
        except IndexError:
            print("Error: Coordinates out of bounds.")
        return True

class RendarCharOnCursor(Executor):
    def __init__(self, color_mode_map, hex_stream):
        super().__init__(hex_stream)
        self.color = self.hex_stream[2]
        self.char = self.hex_stream[3]
        self.color_mode_map = color_mode_map

    def execute(self, screen, cursor_state):

        if self.color not in self.color_mode_map:
            print(f"Error: Invalid color mode {self.color}")
            return False
        
        try:
            screen[cursor_state["y"]][cursor_state["x"]] = f"{self.color_mode_map[int(self.color)]}{chr(self.char)}{self.color_mode_map['reset']}"
        except IndexError:
            print("Error: Coordinates out of bounds.")
        print(f"> Character {chr(self.char)} rendered at cursor position {cursor_state}")
        return True
    
class ClearScreen(Executor):
    def __init__(self, hex_stream):
        super().__init__(hex_stream)

    def execute(self, screen, cursor_state):
        for i in range(len(screen)):
            for j in range(len(screen[i])):
                screen[i][j] = " "
        cursor_state["x"] = 0
        cursor_state["y"] = 0
        print("> Screen cleared, cursor reset to (0, 0)")
        return True


class CommandSwitch: 
    def __init__(self):
        self.screenInit = False
        self.screen = None
        self.cursor_position = {"x": 0, "y": 0} #default cursor position
        self.commandQueue = Queue()
        self.color_mode_map = {}
        
        self.COMMANDS = {
            0x01: ScreenSetup,
            0x02: DrawCharacter,
            0x03: DrawLine,
            0x04: RenderText,
            0x05: MoveCursor,
            0x06: RendarCharOnCursor,
            0x07: ClearScreen,
            0x08: RenderAll,
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
        
        #! Special commands
        # Screen setup
        if command == 0x01:
            #Returns the screen matrix[0] and a color mode map[1]
            screen_data = self.COMMANDS[command](self.hex_stream).execute()
            if screen_data == False:
                return False
            self.screen = screen_data[0]
            self.color_mode_map = screen_data[1]
            self.screenInit = True
            return True
        
        # Clear screen
        if command == 0x07:
            return self.COMMANDS[command](self.hex_stream).execute(self.screen, self.cursor_position)
        
        # Render all
        if command == 0x08:
            return self.COMMANDS[command]().execute(self.commandQueue, self.screen, self.color_mode_map, self.cursor_position)

        self.appendCommand()
        return is_done

class RenderAll(CommandSwitch):
    def execute(self, commandQueue, screen, color_mode_map,cursor_position):
        while not commandQueue.empty():
            commandStream = commandQueue.get()
            command = commandStream[0]
            self.COMMANDS[command](color_mode_map, commandStream).execute(screen, cursor_position)
        print("\n".join("".join(row) for row in screen))
        return True