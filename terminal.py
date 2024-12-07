import convertor


class CommandFactory:
    COMMANDS = {
        "screen_setup": convertor.ScreenSetup, # e.g. screen_setup 80 24 16colors
        "draw_char": convertor.DrawCharacter, #eg. draw_char 0 0 white A
        "draw_line": convertor.DrawLine, #eg. draw_line 60 2 3 10 white *
        "render_text": convertor.RenderText, #eg render_text 40 2 white hello brother
        "cursor_move": convertor.CursorMove, #eg cursor_move 20 5
        "draw_at_cursor": convertor.DrawAtCursor, #eg Draw_at_cursor X white
        "render": convertor.Render, #eg render
        "clear_screen": convertor.ClearScreen #eg clear_screen
    }
    

    @staticmethod
    def create(command_name, session, args):
        if command_name not in CommandFactory.COMMANDS:
            raise ValueError(f"Unknown command: {command_name}")
        return CommandFactory.COMMANDS[command_name](session, args) # ie ScreenSetup(args)


# Example usage:
def main():
    running = True
    session = None
    instructions = "\t- Screen setup: screen_setup <width> <height> <colors>\n\t- Draw character: draw_char <x> <y> <color> <char>\n\t- Draw line: draw_line <x> <y> <length> <color> <char>\n\t- Render text: render_text <x> <y> <color> <text>\n\t- Cursor move: cursor_move <x> <y>\n\t- Draw at cursor: Draw_at_cursor <char> <color>\n\t- Render: render\n\t- Clear screen: clear_screen\n"

    print("\n\nTERMINAL")
    while running:
        command = input("\nEnter command: ")
        command_name = (command.split(" ")[:1])[0].lower()
        args = command.split(" ")[1:] 
        try:
            session = CommandFactory.create(command_name, session, args).to_hex(session)
        except ValueError as e:
            print(f"\n[X] Command failed\nYour entered command \"{command_name}\" in the input \"{command}\" is not valid. \nHere are commands you can run: \n{instructions}")
            continue   

    
if __name__ == "__main__":
    main()
