import logging
from string_pipeline import StringPipeline


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class StringCommandController:
    COMMANDS = {
        "screen_setup": StringPipeline.ScreenSetupPipeLine, # e.g. screen_setup 80 24 16colors
        "draw_char": StringPipeline.DrawCharPipeline, #eg. draw_char 0 0 white A
        "draw_line": StringPipeline.DrawLinePipeLine, #eg. draw_line 60 2 3 10 white *
        "render_text": StringPipeline.RenderTextPipeLine, #eg render_text 40 2 white hello brother
        "cursor_move": StringPipeline.CursorMovePipeLine, #eg cursor_move 20 5
        "draw_at_cursor": StringPipeline.DrawAtCursorPipeLine, #eg Draw_at_cursor X white
        "render": StringPipeline.RenderPipeline, #eg render
        "clear_screen": StringPipeline.ClearScreenPipeLine #eg clear_screen
    }

    @staticmethod   
    def command_pipeline(command_stream):
        expexted_command_name = command_stream[0].lower()

        if expexted_command_name not in StringCommandController.COMMANDS:
            logging.error(f"Unknown command: {expexted_command_name}")
            return None
        return StringCommandController.COMMANDS[expexted_command_name](command_stream) 

