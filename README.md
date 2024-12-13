#

## Terminal <🖥️/>

### Problem </>

I needed a system that could interpret and execute commands provided as hexadecimal byte streams. These commands needed to be validated, executed in sequence.  
To make the system accessible, I also introduced a string execution pipeline that allows users to provide commands in a human-readable format.

The challenge was to ensure that the two pipelines (hex and string) remained consistent, robust, and easy to extend.

Example hex command: `0x01 0x03 0x50 0x18 0x01 0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A 0xFF` 

- The command can be broken into:  
`0x01 0x03 0x50 0x18 0x01` - Screen Setup 80 24 16colors  
`0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A` - Draw line 60 2 3 10 white *  
`0xFF` - End of Stream

Example string commands:  
`screen_setup 80 24 16colors` - translated internally to hex: **0x01 0x03 0x50 0x18 0x01 0xFF**  
`cursor_move 20 5` - translated internally to **0x05 0x02 0x14 0x05 0xFF**  

### Hex Execution Pipeline </>  

#### Architecture

the goal behind this architecture in the pipeline is to ensure easy to follow and debug steps that each validate or transorfm the data.  

Solid principles implemented to achieve this are:  

- `Single Responsibility Principle (SRP)` - Each class and method handles a single aspect of the pipeline. For example, validation, parsing, and execution are separated into distinct methods
- `Open/Closed Principle (OCP)` - The COMMANDS dictionary allows for easy extension with new commands without modifying existing code.

1. **Hex Input Validation** - Ensure the incoming hex stream is convertable to hex commands without breaking.  
2. **Command Parsing** - Convert the hex stream into a series of executable commands
3. **Command Validation** - Ensure all executable commands are accurate and executable
4. **Command Execution** - Iteratively pass all validated commands for execution  



#### Example flow

Consider this input hex stream:

```Hex
0x01 0x03 0x50 0x18 0x01 0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A 0xFF
```

The input is recieved as a string input as that is the return type of `input()` method in python
The terminal uses " " and "," as delimeters to get a `raw string stream`

- **Hex Input Validation** runs methods to ensure all the strings in the `raw string stream` are actually hex and parsable  
- **Command Parsing** Converts the `raw string stream` to a `hex command stream`  
- **Command Validation** Runs checks on all command streams in the `hex command stream` to ensure all of the are executable  
- **Command Execution** Validated commands are iteratively ran through the executor for execution  

||
|---|
|**Hex Input Validation** - runs methods to ensure all the strings in the `raw string stream` are actually hex and parsable |
|---|

