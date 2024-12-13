
# Terminal <🖥️/>

## Problem </>

I decided to take on a challenge to allow the terminal to take both hex, and human readble commands.  
The human readble comands functionality was very important at giving me hex streams to test the hex input functionality.  

Example hex command: `0x01 0x03 0x50 0x18 0x01 0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A 0xFF` 

- The command can be broken into:  
`0x01 0x03 0x50 0x18 0x01` - Screen Setup 80 24 16colors  
`0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A` - Draw line 60 2 3 10 white *  
`0xFF` - End of Stream

Example string commands (Activated by adding a **--readable** flag when running. ie `python terminal.py --readable`):  
`screen_setup 80 24 16colors` - translated internally to hex: **0x01 0x03 0x50 0x18 0x01 0xFF**  
`cursor_move 20 5` - translated internally to **0x05 0x02 0x14 0x05 0xFF**  

## Solution Architecture <✒️/>  
