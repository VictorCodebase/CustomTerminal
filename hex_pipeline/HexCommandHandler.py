import executor
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class HexCommandHandler:
    session = executor.CommandSwitch()
    END_OF_FILE = 0xFF
    #TODO: Fix the readme
    # Bug reports:
    #   Breaks on very long inputs
    #   adds uneeded 0xFF in last byte

    render = [0x08, 0x00, END_OF_FILE]

    def toExecutor(self, hex_command_streams):

        for hex_command_stream in hex_command_streams:
            hex_command_stream.append(self.END_OF_FILE)
            logging.debug(hex_command_stream)
            self.session.execute(hex_command_stream)

        self.session.execute(self.render) 





# 0x01 0x03 0x50 0x18 0x01 0x02 0x04 0x00 0x00 0x07 0x41 0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A 0xFF