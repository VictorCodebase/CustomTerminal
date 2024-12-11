import string_channel
from hex_pipeline import HexCommandHandler
from hex_pipeline import HexCommandValidator
from hex_pipeline import HexParser
import executor

import argparse



# Example usage:
def main():
    parser = argparse.ArgumentParser(description="Terminal")
    parser.add_argument("--readable", action="store_true", help="Run with human-readable commands")
    args = parser.parse_args()
    running = True
    session = None
    #! global instructions should be phased out
    instructions = "\t- Screen setup: screen_setup <width> <height> <colors>\n\t- Draw character: draw_char <x> <y> <color> <char>\n\t- Draw line: draw_line <x> <y> <length> <color> <char>\n\t- Render text: render_text <x> <y> <color> <text>\n\t- Cursor move: cursor_move <x> <y>\n\t- Draw at cursor: Draw_at_cursor <char> <color>\n\t- Render: render\n\t- Clear screen: clear_screen\n"

    print("\n\nTERMINAL")
    
    while running:
        if args.readable:
            session = run_readable(session, instructions)
        else:
            session = run_hex()

        

def run_readable(session, instructions):
    command = input("\nEnter command: ")
    command_name = (command.split(" ")[:1])[0].lower()
    args = command.split(" ")[1:] 
    
    try:
        session = string_channel.CommandFactory.create(command_name, session, args).to_hex(session)
    except ValueError as e:
        print(f"\n[X] Command failed\nYour entered command \"{command_name}\" in the input \"{command}\" is not valid. \nHere are commands you can run: \n{instructions} \n\nIf pasting the command fails, internal program error might have occured. Please debug.")
        return session
    return session

def run_hex():
    command = input("\nEnter command (HEX): ")
    command_stream = [item.strip() for item in command.replace(",", " ").split()]

    
    try:
        hex_stream = [int(item, 16) for item in command_stream if item]
    except:
        print(f"\n[X] Command failed\nYour input \"{command}\" contains a value that is not valid hex.")
        return
    
    # Ensure input stream has no critical errors (that will break the parser)
    hex_command_validator = HexCommandValidator.HexCommandValidator(hex_stream)
    if not hex_command_validator.validify_hex_input():
        return
    if not hex_command_validator.validate_length_bytes():
        return
    
    # Parse the hex stream into commands
    hex_parser = HexParser.HexParser(hex_stream)
    hex_commands = hex_parser.hex()

    # Ensure the commands are valid
    if not hex_command_validator.validify_hex_commands(hex_commands):
        return
    
    # Execute the commands
    handler = HexCommandHandler.HexCommandHandler()
    handler.toExecutor(hex_commands)

    # hex_commands = HexParser.HexParser(hex_stream).hex()
    
    # hex_command_validator = HexCommandValidator.HexCommandValidator(hex_stream)
    # input_valid = hex_command_validator.validifyHexInput()
    # commands_valid = hex_command_validator.validifyHexCommands(hex_commands)

    # if input_valid and commands_valid:
    #     handler = HexCommandHandler.HexCommandHandler()
    #     handler.toExecutor(hex_commands)

if __name__ == "__main__":
    main()
