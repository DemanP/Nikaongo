import os, time
import colors as CS

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MAX_VALUE: int = 255
MEMORY_SIZE: int = 256
memory: bytearray = bytearray(MEMORY_SIZE)

VALUE_SYMBOL: str = "#"

# Display Modes:
# 0 - decimal (default)
# 1 - hex
# 2 - ASCII character
display_mode: int = 0
display_mode_names: list[str] = ["dehimal", "xeks", "tekst"]

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
-k | --klir - klir memori

Ty instrakwn:
stor <ad'res'> <valju>
    Eksampl: stor 0 174
copi <ad'res'> <copi ad'res'>
    Eksampl: copi 0 1
tkst <ad'res'> <tekst>
    Eksampl: tkst 0 Xelo vorld!

Jus #<ad'res'> tu rid valju.
    Eksampl: stor #0 174
    62 in ad'res' 0 => stor 62 174
'''

def set_error(error_text: str) -> None:
    global error
    error = error_text

def clear_screen() -> None:
    os.system("cls")
def refresh() -> None:
    clear_screen()
    print("-- PIKO Emulejwn --")
    print(f"[MEMORI | {MEMORY_SIZE} ty byt]", end=" ")
    print(f"[Displej mod: {display_mode_names[display_mode]}]")
    print_memory(0, MEMORY_SIZE)
    print()
    print(f"{CS.cDebug}[?] --xelp or -x for xelp{CS.cReset}")
    if error:
        print()
        print(f"{CS.cError}{error}{CS.cReset}")
        set_error("")
def print_memory(start: int, end: int) -> None:
    line_length: int = 16
    value_width: int = 4
    if display_mode == 2:
        value_width = 1
        line_length *= 2
    line: str = "─" * line_length * value_width

    start_line: bool = True
    print("┌" + line + "┐")
    for i in range(start, end):
        if start_line:
            print("│", end="")
            start_line = False
        value: int = memory[i]
        value_text: str = str(value)
        if display_mode == 0:
            value_text = "{0:{width}}".format(value_text, width=value_width)
        elif display_mode == 1:
            value_text = hex(value)[2:].zfill(2).upper()
            value_text = "{0:{width}}".format(value_text, width=value_width)
        elif display_mode == 2:
            if value == 0:
                value_text = '×'
            else:
                value_text = chr(value)

        print(value_text, end = "")
        if (i - start) % line_length == line_length - 1:
            print("│")
            start_line = True
    print("└" + line + "┘")
    if (end - start) % line_length != 0:
        print()

def get_value(code: str) -> int:
    if code.startswith(VALUE_SYMBOL):
        code = code[1:]
        return memory[get_value(code)]
    return int(code)
def exec_instruction(code: int, args: list) -> None:
    # store instruction
    address: int = get_value(args[0])
    if address >= MEMORY_SIZE:
        set_error(f"Ad'res' {address} not alavd. Max ad'res' is {MEMORY_SIZE - 1}")
        return
    if code == 0:
        value: int = get_value(args[1])
        if value > MAX_VALUE:
            set_error(f"Can't store {value}, max value is {MAX_VALUE}")
            return
        memory[address] = value
    elif code == 1:
        address_copy: int = get_value(args[1])
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
    global display_mode, memory

    running: bool = True
    while running:
        refresh()

        instruction: str = input(">>> ")
        
        if instruction == "" or instruction.isspace():
            continue
        elif instruction.startswith("-e") or instruction.startswith("--eksit"):
            running = False
            print(f"{CS.cDebug}Eksit{CS.cReset}")
        elif instruction.startswith("-d") or instruction.startswith("--displej"):
            _, d_type = instruction.split()
            display_mode = int(d_type)
        elif instruction.startswith("-x") or instruction.startswith("--xelp"):
            clear_screen()
            print(help_info)
            input("Pres Enter tu ekzit...")
            
        elif instruction.startswith("-f") or instruction.startswith("--fyl"):
            _, file_name, *args = instruction.split()
            wait_time: float = 0.0
            if len(args):
                try:
                    wait_time = float(args[0])
                except:
                    set_error(f"Vyt tym \"{args[0]}\" is not namber")
                    continue
            parse_file(file_name, wait_time)
        elif instruction.startswith("-k") or instruction.startswith("--klir"):
            memory = bytearray(MEMORY_SIZE)
        else:
            parse_instruction(instruction)

main()