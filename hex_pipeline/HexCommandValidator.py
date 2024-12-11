
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HexCommandValidator:
    END_OF_FILE = 0xFF

    def __init__(self, hex_stream):
        self.hex_stream = hex_stream
        self.COMMANDSANDLENGTHS = {
                0x01: 3,
                0x02: 4,
                0x03: 6,
                0x04: 3,
                0x05: 2,
                0x06: 2,
                0x07: 1,
            }

    def validify_hex_input(self):
        for hex in self.hex_stream:
            try:
                int(hex)
            except:
                logging.error("Invalid command, the hex stream contains a non-hex value")
                return False
        return True
    
    def validate_length_bytes(self):
        index = 0
        while index < len(self.hex_stream):
            if self.hex_stream[index] == self.END_OF_FILE:
                return True
            if index + 1 >= len(self.hex_stream):
                print(f"Invalid command at index {index}: Length byte is missing.")
                return False

            length = self.hex_stream[index + 1]
            if index + 2 + length > len(self.hex_stream):
                print(f"Invalid command at index {index}: Length {length} goes out of bounds.")
                return False

            index += 2 + length
        
        print("Invalid command: No EOF byte found")
        return False
        

    def validify_hex_commands(self, commands):
        received_length = len(self.hex_stream)
        calculated_length = 0
        
        print("commands: ",commands)
        for command in commands:
            command_name = command[0]
            command_length = command[1]
            command_instructions = command[2:-1]
            end_of_file = command[-1]
            command_hex = [f"0x{byte:02X}" for byte in command]
            
            if end_of_file != self.END_OF_FILE:
                logging.error(f"Invalid command stream, the EOF byte wasn't the expected 0xFF for: {command_hex}")
                return False

            if command_name not in self.COMMANDSANDLENGTHS:
                logging.error(f"Invalid command stream, the command byte was invalid for: {command_hex}")
                return False
            
            if command_length != len(command_instructions):
                logging.error(f"Invalid command stream, mismatch between command length and actual command length in command: {command_hex}\nExpected {command_length} got {len(command_instructions)}")
                return False
            
            # See if all the command lengths add up to the stream received
            calculated_length += command_length
            logging.debug("new calc len:", calculated_length)


        unaccounted_for_bytes = len(commands) * 3 #For each command, there are 3 extra bytes (command name, command len, end of file)
        total_calculate_length = calculated_length + unaccounted_for_bytes
        received_length_with_added_bytes = received_length + len(commands) -1 #each command has an extra 255, apart from the last
        if total_calculate_length != received_length_with_added_bytes:
            logging.debug("Unaccounted:", unaccounted_for_bytes)
            logging.debug("calculated: ", calculated_length)
            logging.error(f"Received commands failed len test, the total input length is {received_length_with_added_bytes} while the calculated len summed to {total_calculate_length}\nInput was {self.hex_stream}")
            return False
        
        return True 