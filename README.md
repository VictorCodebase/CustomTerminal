
# Terminal

## Solution Overview

In my solution, I implement a terminal that can take either:  

- hex streams (`0x01 0x03 0x50 0x18 0x01 0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A 0xFF`)
-  string inputs (`screen_setup 80 24 16colors` - translated internally to hex: **0x01 0x03 0x50 0x18 0x01 0xFF** )

The challenge was to ensure that the two pipelines (hex and string) remained consistent, robust, and easy to extend. Sufficiently respecting the SOLID principles


## Hex Execution Pipeline  
```mermaid
graph TD;
    Terminal --> run_hex
    run_hex --> HexCommandValidator
    HexCommandValidator-->validate_hex_input;
    HexCommandValidator-->validate_length_bytes;
    HexCommandValidator-->validate_hex_commands;
    run_hex-->HexParser;
    HexParser-->parse_hex;
    run_hex-->HexCommandHandler;
    HexCommandHandler --> to_executor
    
```

### Architecture

1. **Hex Input Validation** - Ensure the incoming hex stream is convertable to hex commands without breaking.  
2. **Command Parsing** - Convert the hex stream into a series of executable commands
3. **Command Validation** - Ensure all executable commands are accurate and executable
4. **Command Execution** - Iteratively pass all validated commands for execution  

> The goal behind this architecture in the pipeline is to ensure easy to follow and debug steps that each validate or transform the data up to the point of execution  

**Solid principles implemented to achieve this are:**  

- `Single Responsibility Principle (SRP)` - Each class and method handles a single aspect of the pipeline. For example, validation, parsing, and execution are separated into distinct methods
- `Open/Closed Principle (OCP)` - The [COMMANDS dictionary](https://github.com/VictorCodebase/CustomTerminal/blob/main/Constants.py) allows for easy extension with new commands without modifying existing code.


### Example flow

Consider this input hex stream:

```Python
0x01 0x03 0x50 0x18 0x01 0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A 0xFF
```

*The terminal uses " " and "," as delimeters to get a `raw string stream`*  

|Hex Command Pipeline|
|---|
|**Hex Input Validation** - runs methods to ensure all the strings in the `raw string stream` are convertable to hex and parsable |
|*Output: True*|
|**Command Parsing** Converts the `raw string stream` to a `hex command stream`|
|*Output: [0x01 0x03 0x50 0x18 0x01 0xFF], [0x03 0x06 0x3C 0x02 0x03 0x0A 0x07 0x2A 0xFF]*|
|**Command Validation** Runs checks on all command streams in the `hex command stream` to ensure all of the are executable|
|*Output: True*|
|**Command Execution** Validated commands are iteratively ran through the executor for execution|
|*Output: True*|

### Running Hex Commands
To setup your environment and clone this project, please follow instructions here:  
[**Instructions**](https://github.com/VictorCodebase/CustomTerminal/edit/main/README.md#running-the-solution)

Run the program:
```bash
python terminal.py
```

## String Execution Pipeline

### Architecture:

## Running the solution  
### Preriquisites

1. **Python 3.8 or higher**  
   Download Python from [python.org](https://www.python.org/downloads/).

2. **Dependencies**  
   Ensure the following standard Python libraries are available:
   
   - `argparse` (for parsing command-line arguments)
   - `sys` (for system-level operations)

3. **Terminal Emulator**  
   A terminal or command prompt (e.g., `bash`, `zsh`, `cmd`, or `PowerShell`).

---

### Step-by-Step Setup

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone <repository-url>
cd <repository-folder>

