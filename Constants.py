
END_OF_FILE = 0xFF

COLOR_MAP_16COLORS = {
    "black": 0x00, "red": 0x01, "green": 0x02, "yellow": 0x03,
    "blue": 0x04, "magenta": 0x05, "cyan": 0x06, "white": 0x07,
    "bright_black": 0x08, "bright_red": 0x09, "bright_green": 0x0A,
    "bright_yellow": 0x0B, "bright_blue": 0x0C, "bright_magenta": 0x0D,
    "bright_cyan": 0x0E, "bright_white": 0x0F
}

COLOR_MAP_MONO = {
    "black": 0x00, "white": 0x01
}

COLOR_MODE_MAPS = {
    "monochrome" : {"black": 0x00, "white": 0x01 },
    "16colors" : {
    "black": 0x00, "red": 0x01, "green": 0x02, "yellow": 0x03,
    "blue": 0x04, "magenta": 0x05, "cyan": 0x06, "white": 0x07,
    "bright_black": 0x08, "bright_red": 0x09, "bright_green": 0x0A,
    "bright_yellow": 0x0B, "bright_blue": 0x0C, "bright_magenta": 0x0D,
    "bright_cyan": 0x0E, "bright_white": 0x0F,
    },
    "256colors":""
}


'''
Map of all acceptable commands and their corresponding lengths
<hex command> <hex legth>
'''
COMMANDS_AND_THEIR_LENGTHS = {
    0x01: 3,
    0x02: 4,
    0x03: 6,
    0x04: 3,
    0x05: 2,
    0x06: 2,
    0x07: 1,
}

COMMANDS = {
    "screen_setup": {
        "hex_id": 0x01,
        "arg_length": 3,
        "signature": ['int', 'int', 'string'],
        "Instructions": "\n\tScreen setup: screen_setup <screen_width (int)> <screen_height (int)> <color_mode (monochrome, 16colors, or 256colors)>\n\tExample: screen_setup 80 24 16colors"
    },
    "draw_char": {
        "hex_id": 0x02,
        "arg_length": 4,
        "signature": ['int', 'int', 'string', 'char']
    },
    "draw_line": {
        "hex_id": 0x03,
        "arg_length": 6,
        "signature": ['int', 'int', 'int', 'string', 'char']
    },
    "render": {
        "hex_id": 0x08,
        "arg_length": 0,
        "signature": []
    }
}
