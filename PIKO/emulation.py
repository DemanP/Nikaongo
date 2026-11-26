import os, time
import colors as CS

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MAX_VALUE: int = 255
MEMORY_SIZE: int = 256
memory: bytearray = bytearray(MEMORY_SIZE)

# Display Types:
# 0 - decimal (default)
# 1 - hex
# 2 - ASCII character
display_type: int = 0

instruction_names: list[str] = ["stor", "copi", "tkst"]
instruction_codes: dict[str, int] = {}
for i, name in enumerate(instruction_names):
    instruction_codes[name] = i

error: str = ""
help_info: str =\
'''
Ty komand:
-x | --xelp - print xelp info
-d | --displej <mod> - cenq displej mod (0 - dehimal, 1 - xeks, 2 - tekst)
    Eksampl: -d 2
-f | --fyl <fyl nejm> <vejt tym> - eksekjut e fyl; vejt tym is ty sekond
    Eksampl: -f test.piko 1

Ty instrakwn:
stor <ad'res'> <valju>
    Eksampl: stor 0 174
copi <ad'res'> <copi ad'res'>
    Eksampl: copi 0 1
tkst <ad'res'> <tekst>
    Eksampl: tkst 0 Xelo vorld!
'''

def set_error(error_text: str) -> None:
    global error
    error = error_text

def refresh() -> None:
    os.system("cls")
    print("-- PIKO Emulejwn --")
    print(f"[Memori | {MEMORY_SIZE} ty byt]")
    print_memory(0, MEMORY_SIZE)
    print()
    print(f"{CS.cDebug}[?] --xelp or -x for xelp{CS.cReset}")
    if error:
        print()
        print(f"{CS.cError}{error}{CS.cReset}")
        set_error("")
def print_memory(start: int, end: int) -> None:
    line_length: int = 16
    for i in range(start, end):
        value: int = memory[i]
        value_text: str = str(value)
        if display_type == 0:
            value_text = f"{value_text:4}"
        elif display_type == 1:
            value_text = hex(value)[2:].zfill(2).upper()
            value_text = f"{value_text:4}"
        elif display_type == 2:
            if value == 0:
                value_text = '×'
            else:
                value_text = chr(value)

        print(value_text, end = "")
        if (i - start) % line_length == line_length - 1:
            print()
    if (end - start) % line_length != 0:
        print()
def exec_instruction(code: int, args: list) -> None:
    # store instruction
    address: int = int(args[0])
    if address >= MEMORY_SIZE:
        set_error(f"Ad'res' {address} not alavd. Max ad'res' is {MEMORY_SIZE - 1}")
        return
    if code == 0:
        value: int = int(args[1])
        if value > MAX_VALUE:
            set_error(f"Can't store {value}, max value is {MAX_VALUE}")
            return
        memory[address] = value
    elif code == 1:
        address_copy: int = int(args[1])
        memory[address_copy] = memory[address]
    elif code == 2:
        text: str = " ".join(args[1:])
        for i in range(len(text)):
            memory[address + i] = ord(text[i])

def parse_instruction(instruction: str) -> None:
    instruction_name, *args = instruction.split()
    if instruction_name in instruction_codes:
        exec_instruction(instruction_codes[instruction_name], args)
    else:
        set_error(f"Instrakwn \"{instruction_name}\" not ekzist!")
def parse_file(file_name: str, wait_time: float = 0.0) -> None:
    file = open(file_name, "r")
    code: str = file.read()
    file.close()
    for line in code.splitlines():
        parse_instruction(line)
        refresh()
        time.sleep(wait_time)

def main() -> None:
    global display_type

    running: bool = True
    while running:
        refresh()

        instruction: str = input(">>> ")
        
        if instruction == "" or instruction.isspace():
            continue
        elif instruction.startswith("-e") or instruction.startswith("--eksit"):
            running = False
            print(f"{CS.cDebug}Eksit{CS.cReset}")
            continue
        elif instruction.startswith("-d") or instruction.startswith("--displej"):
            _, d_type = instruction.split()
            display_type = int(d_type)
            continue
        elif instruction.startswith("-x") or instruction.startswith("--xelp"):
            os.system("cls")
            print(help_info)
            input("Pres Enter tu ekzit...")
            continue
        elif instruction.startswith("-f") or instruction.startswith("--fyl"):
            _, file_name, *args = instruction.split()
            wait_time: float = 0.0
            if len(args) and args[0].isnumeric():
                wait_time = float(args[0])
            parse_file(file_name, wait_time)
            continue

        parse_instruction(instruction)

main()