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
        command_name = self.command[0]
        try:
            command_info = Constants.COMMANDS[command_name]
        except KeyError:
            logging.error(f"The command '{command_name}' does not exist in the constants dictionary.")
            return False

        expected_arg_length = command_info['arg_length']
        hex_id = command_info['hex_id']

        if len(self.command) != expected_arg_length + 1:  # +1 for the command name
            logging.error(f"Invalid number of arguments. {command_info['Instructions']}")
            return False

        # make command info accessible to other methods as command structure is accurate
        self.hex_id = hex_id
        self.command_length = expected_arg_length
        self.command_instructions = command_info['Instructions']
        return True
    

    def parse(self):
        raise NotImplementedError

    def command_handler(self, hex_stream):
        self.session.execute(hex_stream)


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
        SessionManager.SessionManager.set_session(initiated_screen_session)
        print(self.session)


class RenderPipeline(CommandPipeline):

    def validate_input(self):
        print(self.session)
        if not self.session:
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

