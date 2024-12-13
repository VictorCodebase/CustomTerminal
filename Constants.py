
END_OF_FILE = 0xFF
MAX_ARG = 99

'''
Map of all acceptable commands and their corresponding lengths
<hex command> <hex legth>
'''

COMMANDS = {
    "screen_setup": {
        "hex_id": 0x01,
        "arg_length": 3,
        "signature": ['int', 'int', 'string'],
        "instructions": "\n\tScreen setup: screen_setup <screen_width (int)> <screen_height (int)> <color_mode (monochrome, 16colors, or 256colors)>\n\tExample: screen_setup 80 24 16colors"
    },
    "draw_char": {
        "hex_id": 0x02,
        "arg_length": 4,
        "signature": ['int', 'int', 'string', 'char'],
        "instructions": "\n\tDraw character: draw_char <x (int)> <y (int)> <color (string)> <char (char)>\n\tExample: draw_char 0 0 white A"
    },
    "draw_line": {
        "hex_id": 0x03,
        "arg_length": 6,
        "signature": ['int', 'int', 'int', 'string', 'char'],
        "instructions": "\n\tDraw line: draw_line <x (int)> <y (int)> <length (int)> <color (string)> <char (char)>\n\tExample: draw_line 60 2 3 10 white *"
    },
    "render_text": {
        "hex_id": 0x04,
        "arg_length": 99,
        "signature": ['int', 'int', 'string', 'string'],
        "instructions": "\n\tRender text: render_text <x (int)> <y (int)> <color (string)> <text (string array)>\n\tExample: render_text 40 2 white hello brother"
    },
    "cursor_move": {
        "hex_id": 0x05,
        "arg_length": 2,
        "signature": ['int', 'int'],
        "instructions": "\n\tCursor move: cursor_move <x (int)> <y (int)>\n\tExample: cursor_move 20 5"
    },
    "draw_at_cursor": {
        "hex_id": 0x06,
        "arg_length": 2,
        "signature": ['string', 'char'],
        "instructions": "\n\tDraw at cursor: draw_at_cursor <color (string)> <char (char)>\n\tExample: draw_at_cursor white A"
    },
    "clear_screen": {
        "hex_id": 0x07,
        "arg_length": 0,
        "signature": [],
        "instructions": "\n\tClear screen: clear_screen\n\tExample: clear_screen"
    },
    "render": {
        "hex_id": 0x08,
        "arg_length": 0,
        "signature": [],
        "instructions": "\n\tRender: render\n\tExample: render"
    }
}
