import convertor


class CommandFactory:
    COMMANDS = {
        "screen_setup": convertor.ScreenSetup, # e.g. screen_setup 80 24 16colors
        "draw_char": convertor.DrawCharacter, #eg. draw_char 0 0 white A
        "draw_line": convertor.DrawLine, #eg. draw_line 6 2 3 10 white *
        "render_text": convertor.RenderText, #eg render_text 2 2 white hello brother
        "cursor_move": convertor.CursorMove, #eg cursor_move 2 2
        "Draw_at_cursor": convertor.DrawAtCursor, #eg Draw_at_cursor X white
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

    print("\n\nTERMINAL")
    while running:
        command = input("\nEnter command: ")
        command_name = command.split(" ")[:1]
        args = command.split(" ")[1:] 

        # Create command object
        session = CommandFactory.create(command_name[0], session, args).to_hex(session)
        


if __name__ == "__main__":
    main()
