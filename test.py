class SimulatedTerminal:
    def __init__(self):
        self.screen = None
        self.running = True
        self.command_map = {
            "setup": self.command_setup,
            "draw": self.command_draw,
            "render": self.command_render,
            "clear": self.command_clear,
            "exit": self.command_exit
        }

    def command_setup(self, args):
        if len(args) != 3:
            print("Usage: setup <width> <height> <color_mode>")
            return
        width, height, color_mode = map(int, args)
        self.screen = [[" " for _ in range(width)] for _ in range(height)]
        print(f"Screen setup: {width}x{height}, color mode {color_mode}")

    def command_draw(self, args):
        if not self.screen:
            print("Error: Screen not set up. Use 'setup' first.")
            return
        if len(args) != 4:
            print("Usage: draw <x> <y> <color> <char>")
            return
        x, y, color, char = int(args[0]), int(args[1]), args[2], args[3]
        try:
            self.screen[y][x] = char
            print(f"Drawn '{char}' at ({x}, {y}) with color {color}")
        except IndexError:
            print("Error: Coordinates out of bounds.")

    def command_render(self, args):
        if not self.screen:
            print("Error: Screen not set up. Use 'setup' first.")
            return
        print(self.screen)
        print("\n".join("".join(row) for row in self.screen))

    def command_clear(self, args):
        if not self.screen:
            print("Error: Screen not set up. Use 'setup' first.")
            return
        for y in range(len(self.screen)):
            for x in range(len(self.screen[y])):
                self.screen[y][x] = " "
        print("Screen cleared.")

    def command_exit(self, args):
        self.running = False
        print("Exiting terminal...")

    def process_command(self, command):
        parts = command.strip().split()
        if not parts:
            return
        cmd, args = parts[0], parts[1:]
        handler = self.command_map.get(cmd)
        if handler:
            handler(args)
        else:
            print(f"Unknown command: {cmd}")

    def run(self):
        print("Simulated Terminal. Type 'exit' to quit.")
        while self.running:
            command = input(">> ")
            self.process_command(command)


# Run the terminal
terminal = SimulatedTerminal()
terminal.run()


'''

How It Works
Setup:

Type `setup 80 24 01` to initialize the screen with 80x24 characters and color mode 01.
Draw Characters:

Type `draw 10 15 1 A` to draw the character A at position (10, 15).
Render the Screen:

Type `render` to display the current state of the screen.
Clear the Screen:

Type `clear` to wipe the screen.
Exit:

Type `exit` to quit the program.
'''