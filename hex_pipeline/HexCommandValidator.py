import Constants
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HexCommandValidator:
    def __init__(self, hex_stream):
        self.hex_stream = hex_stream

    def validate_hex_input(self):
        try:
            for item in self.hex_stream:
                int(item, 16)  # Try converting to hex to check validity
            return True
        except ValueError:
            logging.error(f"[X] Command failed\nYour input \"{self.hex_stream}\" contains a value that is not valid hex.")
            return False

    def validate_length_bytes(self):
        index = 0
        while index < len(self.hex_stream):
            if self.hex_stream[index] == Constants.END_OF_FILE:
                return True
            if index + 1 >= len(self.hex_stream):
                logging.error(f"Invalid command at index {index}: Length byte is missing.")
                return False

            length = self.hex_stream[index + 1]
            if index + 2 + length > len(self.hex_stream):
                logging.error(f"Ivalid command at index {index}: Length {length} goes out of bounds.")
                return False

            index += 2 + length
        
        logging.error("Invalid command: No EOF byte found")
        return False

    def validate_hex_commands(self, commands):
        received_length = len(self.hex_stream)
        calculated_length = 0
        
        logging.debug("commands: ", commands)
        for command in commands:
            command_hex = [f"0x{byte:02X}" for byte in command]
            hex_id = command[0]  # The first byte is the command ID
            command_length = command[1]  # The second byte is the length of arguments
            command_instructions = command[2:-1]  # The arguments are between the length byte and EOF
            end_of_file = command[-1]  # The last byte should be the EOF (0xFF)

            if not self.validate_hex_command(hex_id, command_instructions):
                return False

            if end_of_file != Constants.END_OF_FILE:
                logging.error(f"Invalid command stream, the EOF byte wasn't the expected 0xFF for: {command_hex}")
                return False

            # Look up the command in COMMANDS using the hex_id
            command_info = next((info for info in Constants.COMMANDS.values() if info["hex_id"] == hex_id), None)

            if not command_info:
                logging.error(f"Invalid command stream, the hex_id '{hex(hex_id)}' was not found in the commands list for: {command_hex}")
                return False
            
            # Validate the length based on the retrieved command_info
            if len(command_instructions) != command_info['arg_length']:
                if int(command_info['arg_length']) < Constants.MAX_ARG:
                    logging.error(f"Invalid number of arguments for command with hex_id '{hex_id}'. Expected {command_info['arg_length']} arguments, but got {len(command_instructions)}.")
                    return False

            # Add up the command lengths
            calculated_length += command_length
            logging.debug("new calc len:", calculated_length)

        unaccounted_for_bytes = len(commands) * 3  # For each command, there are 3 extra bytes (command name, command len, end of file)
        total_calculated_length = calculated_length + unaccounted_for_bytes
        received_length_with_added_bytes = received_length + len(commands) - 1  # each command has an extra 255, apart from the last
        if total_calculated_length != received_length_with_added_bytes:
            logging.debug("Unaccounted:", unaccounted_for_bytes)
            logging.debug("calculated:", calculated_length)
            logging.error(f"Received commands failed len test, the total input length is {received_length_with_added_bytes} while the calculated len summed to {total_calculated_length}\nInput was {self.hex_stream}")
            return False
        
        return True 

    def validate_hex_command(self, hex_id, args):
        # Look up the command by hex_id
        command_info = next((info for info in Constants.COMMANDS.values() if info["hex_id"] == hex_id), None)

        if not command_info:
            logging.error(f"Unknown hex command ID '{hex(hex_id)}'.")
            return False

        if len(args) != command_info['arg_length']:
            if int(command_info['arg_length']) < Constants.MAX_ARG: 
                logging.error(f"Inal number of rguments for command with hex_id '{hex_id}'. Expected {command_info['arg_length']} arguments, but got {len(args)}.")
                return False
        return True
