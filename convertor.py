import executor

class Command:
    #TODO: Ensure user does not input anything that can be converted to 0xFF or be larger than input size
    def __init__(self, session, args):
        self.args = args
        self.session = session

    def to_hex(self, screenSession=None):
        """Convert command arguments to hex stream. Override in subclasses."""
        raise NotImplementedError

    def serveInstructions(self):
        print("\nYour input was invalid. The following syntax is expected for the corresponding command:\n \tscreen_setup <screen_width (int)> <screen_height (int)> <color_mode (monochrome, 16colors, 256colors)")

    def convert_color(self, color, mode):
        color_map = {}
        if mode == "monochrome":
            color_map = {"black": 0x00, "white": 0x01}
        elif mode == "16colors":
            color_map = {
                "black": 0x00, "red": 0x01, "green": 0x02, "yellow": 0x03,
                "blue": 0x04, "magenta": 0x05, "cyan": 0x06, "white": 0x07,
                "bright_black": 0x08, "bright_red": 0x09, "bright_green": 0x0A,
                "bright_yellow": 0x0B, "bright_blue": 0x0C, "bright_magenta": 0x0D,
                "bright_cyan": 0x0E, "bright_white": 0x0F
            }
        elif mode == "256colors":
            if not (0 <= int(color) <= 255):
                raise ValueError("Color index must be between 0 and 255 for 256 color mode.")
            return int(color)  # Directly return as integer

        if color not in color_map:
            raise ValueError(f"Color '{color}' not recognized for mode '{mode}'.")
        return color_map[color]

    def execute(stream):
        executor.CommandSwitch(stream).execute()

#!Is this necessary
class Logger:
    @staticmethod    
    def valueErr(message):
        print(f"\n[x] Failed: value error, {message}")
        quit()

    
    def log(message):
        print(f"\n[v] Success: {message}")
    

class ScreenSetup(Command):
    HEX_ID = 0x1
    print("Screen Setup Command")
    instructions = ""

    def to_hex(self, screenSession=None):

        if screenSession is not None:
            print("Screen session already initiated. Please clear screen before setting up a new one.")
            return screenSession

        allowed_args = 3
        if len(self.args) != allowed_args:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")
        
        width, height, color = self.args
        color_mode_map = {"monochrome": 0x00, "16colors": 0x01, "256colors": 0x02}
        if color not in color_mode_map: Logger.valueErr("Color not recognized")

        try:
            width = int(width)
            height = int(height)
            color = int(color_mode_map[color])

        except:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")

        stream = [self.HEX_ID, allowed_args, width, height, color, 0xFF]
        hex_stream = [f"0x{byte:02X}" for byte in stream]
        print("Hex Stream:", " ".join(hex_stream))


        intiatedScreenSession = executor.CommandSwitch()
        intiatedScreenSession.execute(stream)
        return intiatedScreenSession


class DrawCharacter(Command):
    HEX_ID = 0x2
    def to_hex(self, screenSession=None):
        allowed_args = 4
        if len(self.args) != allowed_args:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")
        
        x, y, color, char = self.args


        try:
            x = int(x)
            y = int(y)
            char = ord(char)
            color = self.convert_color(color, "monochrome")
            stream = [self.HEX_ID, allowed_args, x, y, color, char, 0xFF]
            screenSession.execute(stream)
            return screenSession
            #return stream #draw_char 3 4 blue A
        except:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")

class DrawLine(Command):
    HEX_ID = 0x3
    def to_hex(self, screenSession=None):
        if (screenSession is None):
            print("Screen session must be initiated before running this command")
        allowed_args = 6
        if len(self.args) != allowed_args:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")
        
        x1, y1, x2, y2, colorIndex, char = self.args

        try:
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)
            colorIndex = self.convert_color(colorIndex, "monochrome")
            char = ord(char)

            stream = [self.HEX_ID, allowed_args, x1, y1, x2, y2, colorIndex, char, 0xFF]
            screenSession = screenSession.execute(stream)
            return screenSession
        except:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")


class RenderText(Command):
    HEX_ID = 0x4

    def to_hex(self, screenSession=None):
        allowed_args = 4 #This is the minimum args acceptible, no upper bound
        if len(self.args) < allowed_args:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")

        x, y, colorIndex, *textChars = self.args
        chars = self.textCharsToOrd(textChars)

        try:
            x = int(x)
            y = int(y)
            colorIndex = self.convert_color(colorIndex, "monochrome")

            stream = [self.HEX_ID, allowed_args + len(chars), x, y, colorIndex]
            stream.extend(chars)
            stream.append(0xFF)
            screenSession.execute(stream)
            return screenSession
            #return stream
        except:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")
            

    def textCharsToOrd(self, lists):
        ordChars = []
        combined_list = []
        for list in lists:
            combined_list.extend(list)
        
        for char in combined_list:
            ordChars.append(ord(char))
        return ordChars

class CursorMove(Command):
    HEX_ID = 0x5

    def to_hex(self, screenSession=None):
        if (screenSession is None):
            print("Screen session must be initiated before running this command.")

        allowed_args = 2
        if len(self.args) != allowed_args:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")

        x, y = self.args
        try:
            x = int(x)
            y = int(y)

            stream = [self.HEX_ID, allowed_args, x, y, 0xFF]
            screenSession.execute(stream)
            return screenSession
        except:
            print("len", len(self.args))
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")

class DrawAtCursor(Command):
    HEX_ID = 0x6
    allowed_args = 2

    def to_hex(self, screenSession=None):
        if (screenSession is None):
            print("Screen session must be initiated before drawing at cursor.")
            return screenSession
        if len(self.args) != self.allowed_args:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")

        char, color = self.args
        try:
            char = ord(char)
            color = self.convert_color(color, "monochrome")
            stream = [self.HEX_ID, self.allowed_args, color, char, 0xFF]
            screenSession.execute(stream)
            return screenSession
        except:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")
        


class ClearScreen(Command):
    HEX_ID = 0x7
    allowed_args = 0

    def to_hex(self, screenSession=None):
        if (screenSession is None):
            print("Screen session must be initiated before clearing screen.")
            return screenSession
        if len(self.args) != self.allowed_args:
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")
        
        stream = [self.HEX_ID, self.allowed_args, 0xFF]
        screenSession.execute(stream)
        return screenSession



class Render(Command):
    HEX_ID = 0x8
    allowed_args = 0
    
    def to_hex(self, screenSession=None):
        if (screenSession is None):
            print("Screen session must be initiated before rendering.")
        if len(self.args) != self.allowed_args:
            print(len(self.args))
            print(f"[x] Command failed, Please ensure all your inputs for this command are correct")

        stream = [self.HEX_ID, self.allowed_args, 0xFF]

        print("Screen session:", screenSession)
        screenSession.execute(stream)
        return screenSession
        