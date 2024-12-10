import convertor
import parser
import executor

import argparse



# Example usage:
def main():
    parser = argparse.ArgumentParser(description="Terminal")
    parser.add_argument("--readable", action="store_true", help="Run with human-readable commands")
    args = parser.parse_args()
    running = True
    session = None
    instructions = "\t- Screen setup: screen_setup <width> <height> <colors>\n\t- Draw character: draw_char <x> <y> <color> <char>\n\t- Draw line: draw_line <x> <y> <length> <color> <char>\n\t- Render text: render_text <x> <y> <color> <text>\n\t- Cursor move: cursor_move <x> <y>\n\t- Draw at cursor: Draw_at_cursor <char> <color>\n\t- Render: render\n\t- Clear screen: clear_screen\n"

    print("\n\nTERMINAL")
    
    while running:
        if args.readable:
            session = run_readable(session, instructions)
        else:
            session = run_hex(session, instructions)

        

def run_readable(session, instructions):
    command = input("\nEnter command: ")
    command_name = (command.split(" ")[:1])[0].lower()
    args = command.split(" ")[1:] 
    try:
        session = convertor.CommandFactory.create(command_name, session, args).to_hex(session)
    except ValueError as e:
        print(f"\n[X] Command failed\nYour entered command \"{command_name}\" in the input \"{command}\" is not valid. \nHere are commands you can run: \n{instructions} \n\nIf pasting the command fails, internal program error might have occured. Please debug.")
        return session
    return session

def run_hex(session, instructions):
    render = [0x08, 0x00, 0xFF]

    command = input("\nEnter command (HEX): ")
    if "," in command:
        command_stream = command.split(",")
    else:
        command_stream = command.split(" ")

    
    try:
        hex_stream = [int(item.strip(), 16) for item in command_stream if item.strip()]
    except:
        print(f"\n[X] Command failed\nYour input \"{command}\" contains a value that is not valid hex.")
        return session
    
    hex_command_streams = parser.Parse(hex_stream).hex()
    

    session = executor.CommandSwitch()

    for hex_command_stream in hex_command_streams:
        hex_command_stream.append(0xFF)
        print(hex_command_stream)
        session.execute(hex_command_stream)



    session.execute(render) 
    # 0x01 0x03 0x50 0x18 0x01 0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A 0x02 0x04 0x00 0x00 0x06 0x41 0x06 0x02 0x01 0x58 0xFF
    # 0x01 0x03 0x50 0x18 0x01 0x04 0x12 0x28 0x02 0x07 0x68 0x65 0x6C 0x6C 0x6F 0x20 0x62 0x72 0x6F 0x74 0x68 0x65 0x72 0x20 0xFF
    

    return session
    
if __name__ == "__main__":
    main()
