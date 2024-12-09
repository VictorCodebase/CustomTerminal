import convertor
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

def run_hex():
    command = input("\nEnter command (HEX): ")
    return
    
if __name__ == "__main__":
    main()
