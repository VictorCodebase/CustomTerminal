import logging
import Constants
import SessionManager
import executor

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class CommandPipeline:

    @property
    def session(self):
        return SessionManager.SessionManager.get_session()

    def __init__(self, command):
        self.command = command

    def validate_input(self):
        raise NotImplementedError

    def validate_command_structure(self):
        command_name = self.command[0].lower()
        try:
            command_info = Constants.COMMANDS[command_name]
        except KeyError:
            logging.error(f"The command '{command_name}' does not exist in the constants dictionary.")
            return False

        expected_arg_length = command_info['arg_length']
        expected_hex_id = command_info['hex_id']
        probable_command_instructions = command_info['instructions']

        if len(self.command) != expected_arg_length + 1 and expected_arg_length < 99:  # +1 for the command name
            logging.error(f"Invalid number of arguments. {probable_command_instructions}")
            return False

        # make command info accessible to other methods as command structure is accurate
        self.hex_id = expected_hex_id
        self.command_length = expected_arg_length
        self.command_instructions = probable_command_instructions
        return True
    

    def parse(self):
        raise NotImplementedError

    def command_handler(self, hex_stream):
        self.session.session.execute(hex_stream)


class ScreenSetupPipeLine(CommandPipeline):
    COLOR_MODE_MAP = {"monochrome": 0x00, "16colors": 0x01, "256colors": 0x02}

    def validate_input(self):
        if not self.validate_command_structure():
            return False

        _, width, height, color_mode = self.command

        if color_mode not in self.COLOR_MODE_MAP:
            logging.error(f"Invalid color mode '{color_mode}'. Valid options are: {', '.join(self.COLOR_MODE_MAP.keys())}")
            return False

        try:
            int(width)
            int(height)
        except ValueError:
            logging.error("Width and height must be integers.")
            return False

        return True

    def parse_input(self):
        _, width, height, color_mode = self.command
        width = int(width)
        height = int(height)
        stream = [self.hex_id, self.command_length, width, height, self.COLOR_MODE_MAP[color_mode], Constants.END_OF_FILE]
        hex_stream = [f"0x{byte:02X}" for byte in stream]
        logging.info("Input translated to hex stream: " + " ".join(hex_stream))
        return stream

    def command_handler(self, hex_stream):
        initiated_screen_session = executor.CommandSwitch()
        initiated_screen_session.execute(hex_stream)
        SessionManager.SessionManager.set_session(SessionManager.SessionShared(initiated_screen_session, "16colors"))
        print(self.session)



class DrawCharPipeline(CommandPipeline):
    
        def validate_input(self):
            print(self.session)
            if not self.session or self.session.session is None:
                logging.error("No screen has been set up. Please run 'screen_setup' first.")
                return False
            
            if not self.validate_command_structure():
                return False
            try:
                _, x, y, color, char = self.command
            except ValueError:
                logging.error("Invalid number of arguments. draw_char <x> <y> <color> <char>")
                return False
    
            if color not in Constants.COLOR_MAP_16COLORS:
                logging.error(f"Invalid color '{color}'. Valid options are: {', '.join(Constants.COLOR_MAP_16COLORS.keys())}")
                return False
    
            try:
                int(x)
                int(y)
            except ValueError:
                logging.error("X and Y must be integers.")
                return False
    
            return True
    
        def parse_input(self):
            _, x, y, color, char = self.command
            x = int(x)
            y = int(y)
            color = Constants.COLOR_MAP_16COLORS[color]
            char = ord(char)
            stream = [self.hex_id, self.command_length, x, y, color, char, Constants.END_OF_FILE]
            hex_stream = [f"0x{byte:02X}" for byte in stream]
            logging.info("Input translated to hex stream: " + " ".join(hex_stream))
            return stream


class DrawLinePipeLine(CommandPipeline):
    
        def validate_input(self):
            if not self.session or self.session.session is None:
                logging.error("No screen has been set up. Please run 'screen_setup' first.")
                return False
            
            if not self.validate_command_structure():
                return False
            
            try:
                _, x1, y1, x2, y2, color, char = self.command
            except ValueError:
                logging.error("Invalid number of arguments. draw_line <x> <y> <length> <color> <char>")
                return False
    
            if color not in Constants.COLOR_MAP_16COLORS:
                logging.error(f"Invalid color '{color}'. Valid options are: {', '.join(Constants.COLOR_MAP_16COLORS.keys())}")
                return False
    
            try:
                int(x1)
                int(y1)
                int(x2)
                int(y2)
            except ValueError:
                logging.error("X, Y, and length must be integers.")
                return False
    
            return True
    
        def parse_input(self):
            _, x1, y1, x2, y2, color, char = self.command
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            color = Constants.COLOR_MAP_16COLORS[color]
            char = ord(char)
            stream = [self.hex_id, self.command_length, x1, y1, x2, y2, color, char, Constants.END_OF_FILE]
            hex_stream = [f"0x{byte:02X}" for byte in stream]
            logging.info("Input translated to hex stream: " + " ".join(hex_stream))
            return stream

class RenderTextPipeLine(CommandPipeline):
        
        def validate_input(self):
            if not self.session or self.session.session is None:
                logging.error("No screen has been set up. Please run 'screen_setup' first.")
                return False
            
            if not self.validate_command_structure():
                return False
            
            try:
                _, x, y, color, *text = self.command
            except ValueError:
                logging.error("Invalid number of arguments. render_text <x> <y> <color> <text>")
                return False
    
            if color not in Constants.COLOR_MAP_16COLORS:
                logging.error(f"Invalid color '{color}'. Valid options are: {', '.join(Constants.COLOR_MAP_16COLORS.keys())}")
                return False
    
            try:
                int(x)
                int(y)
            except ValueError:
                logging.error("X and Y must be integers.")
                return False
    
            return True
    
        def parse_input(self):
            # Necessary command bytes are up to index 4, the rest are text
            text_with_spaces = " ".join(self.command[4:])
            _, x, y, color, *text = self.command
            x = int(x)
            y = int(y)
            color = Constants.COLOR_MAP_16COLORS[color]
            text = [ord(char) for char in text_with_spaces]
            stream = [self.hex_id, self.command_length, x, y, color] + text + [Constants.END_OF_FILE]
            hex_stream = [f"0x{byte:02X}" for byte in stream]
            logging.info("Input translated to hex stream: " + " ".join(hex_stream))
            return stream
            

class CursorMovePipeLine(CommandPipeline):
            
            def validate_input(self):
                if not self.session or self.session.session is None:
                    logging.error("No screen has been set up. Please run 'screen_setup' first.")
                    return False
                
                if not self.validate_command_structure():
                    return False
                
                try:
                    _, x, y = self.command
                except ValueError:
                    logging.error("Invalid number of arguments. cursor_move <x> <y>")
                    return False
        
                try:
                    int(x)
                    int(y)
                except ValueError:
                    logging.error("X and Y must be integers.")
                    return False
        
                return True
        
            def parse_input(self):
                _, x, y = self.command
                x = int(x)
                y = int(y)
                stream = [self.hex_id, self.command_length, x, y, Constants.END_OF_FILE]
                hex_stream = [f"0x{byte:02X}" for byte in stream]
                logging.info("Input translated to hex stream: " + " ".join(hex_stream))
                return stream
            

class DrawAtCursorPipeLine(CommandPipeline):
    
        def validate_input(self):
            if not self.session or self.session.session is None:
                logging.error("No screen has been set up. Please run 'screen_setup' first.")
                return False

            if not self.validate_command_structure():
                return False

            try:
                _, char, color = self.command
            except ValueError:
                logging.error("Invalid number of arguments. draw_at_cursor <color> <char>")
                return False

            if color not in Constants.COLOR_MAP_16COLORS:
                logging.error(f"Invalid color '{color}'. Valid options are: {', '.join(Constants.COLOR_MAP_16COLORS.keys())}")
                return False

            return True

        def parse_input(self):
            _, char, color = self.command
            color = Constants.COLOR_MAP_16COLORS[color]
            char = ord(char)
            stream = [self.hex_id, self.command_length, color, char, Constants.END_OF_FILE]
            hex_stream = [f"0x{byte:02X}" for byte in stream]
            logging.info("Input translated to hex stream: " + " ".join(hex_stream))
            return stream


class RenderPipeline(CommandPipeline):

        def validate_input(self):
            if not self.session or self.session.session is None:
                logging.error("No screen has been set up. Please run 'screen_setup' first.")
                return False

            if not self.validate_command_structure():
                return False

            return True

        def parse_input(self):
            stream = [self.hex_id, Constants.END_OF_FILE]
            hex_stream = [f"0x{byte:02X}" for byte in stream]
            logging.info("Input translated to hex stream: " + " ".join(hex_stream))
            return stream

class ClearScreenPipeLine(CommandPipeline):
    
        def validate_input(self):
            if not self.session or self.session.session is None:
                logging.error("No screen has been set up. Please run 'screen_setup' first.")
                return False

            if not self.validate_command_structure():
                return False

            return True

        def parse_input(self):
            stream = [self.hex_id, self.command_length, Constants.END_OF_FILE]
            hex_stream = [f"0x{byte:02X}" for byte in stream]
            logging.info("Input translated to hex stream: " + " ".join(hex_stream))
            return stream

