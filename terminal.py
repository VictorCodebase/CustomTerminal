
from hex_pipeline import HexCommandHandler
from hex_pipeline import HexCommandValidator
from hex_pipeline import HexParser

from string_pipeline import StringCommandController

import argparse
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def main():
    parser = argparse.ArgumentParser(description="Terminal")
    parser.add_argument("--readable", action="store_true", help="Run with human-readable commands")
    args = parser.parse_args()
    running = True
    print("\n\nTERMINAL")
    
    while running:
        if args.readable:
            run_readable()
        else:
            run_hex()

        

def run_readable():
    command = input("\nEnter command: ")
    command_stream = [item.strip() for item in command.replace(",", " ").split()]

    command_pipeline = StringCommandController.StringCommandController.command_pipeline(command_stream)
    if not command_pipeline: return None
    if not command_pipeline.validate_command_structure(): return None
    if not command_pipeline.validate_input(): return None
    hex_stream = command_pipeline.parse_input()
    command_pipeline.command_handler(hex_stream)


def run_hex():
    command = input("\nEnter command (HEX): ")
    command_stream = [item.strip() for item in command.replace(",", " ").split()]

    # Pre-validation of the raw command string (Raw hex stream is generatable from the raw command string))
    try:
        hex_stream = [int(item, 16) for item in command_stream if item]
    except ValueError:
        logging.error(f"[X] Command failed\nYour input \"{command}\" contains a value that is not valid hex.")
        return

    # Validate hex stream (to ensure that it won't break the parser)
    hex_command_validator = HexCommandValidator.HexCommandValidator(hex_stream)
    if not hex_command_validator.validate_length_bytes():
        return
    
    # Parse the hex stream into commands
    hex_parser = HexParser.HexParser(hex_stream)
    hex_commands = hex_parser.hex()

    # Ensure the commands are valid
    if not hex_command_validator.validate_hex_commands(hex_commands):
        return
    
    # Execute the commands
    handler = HexCommandHandler.HexCommandHandler()
    handler.toExecutor(hex_commands)


if __name__ == "__main__":
    main()
