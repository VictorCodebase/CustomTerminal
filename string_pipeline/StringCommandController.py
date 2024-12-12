
from string_pipeline import StringPipeline

class StringCommandController:
    COMMANDS = {
        "screen_setup": StringPipeline.ScreenSetupPipeLine, # e.g. screen_setup 80 24 16colors
        # "draw_char": DrawCharacter, #eg. draw_char 0 0 white A
        # "draw_line": DrawLine, #eg. draw_line 60 2 3 10 white *
        # "render_text": RenderText, #eg render_text 40 2 white hello brother
        # "cursor_move": CursorMove, #eg cursor_move 20 5
        # "draw_at_cursor": DrawAtCursor, #eg Draw_at_cursor X white
        "render": StringPipeline.RenderPipeline, #eg render
        # "clear_screen": ClearScreen #eg clear_screen
    }

    @staticmethod   
    def command_pipeline(command_stream):
        expexted_command_name = command_stream[0]

        if expexted_command_name not in StringCommandController.COMMANDS:
            raise ValueError(f"Unknown command: {expexted_command_name}")
        return StringCommandController.COMMANDS[expexted_command_name](command_stream) 
