import os, time
import colors as CS

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MAX_VALUE: int = 255
MEMORY_SIZE: int = 256
memory: bytearray = bytearray(MEMORY_SIZE)

MIN_ARGS: int = 2

PROGRAM_SIZE: int = 256
program: bytearray = bytearray(PROGRAM_SIZE)
program_write_pointer: int = 0
program_pointer: int = 0
program_running: bool = False
MIN_WAIT_TIME: float = 1 / 60
wait_time: float = MIN_WAIT_TIME

VALUE_SYMBOL: str = "#"
HEX_SYMBOL: str = "x"

# Display Modes:
# 0 - decimal (default)
# 1 - hex
# 2 - ASCII character
display_mode: int = 0
display_mode_names: list[str] = ["dehimal", "xeks", "tekst"]

instruction_names: list[str] = ["stor", "copi", "tkst", "qump", "inkr"]
instruction_codes: dict[str, int] = {}
for i, name in enumerate(instruction_names):
    instruction_codes[name] = i

error: str = ""
help_info: str =\
'''
Emulejwn ty komand:
-x | --xelp - print xelp info
-d | --displej <mod> - cenq displej mod (0 - dehimal, 1 - xeks, 2 - tekst)
    Eksampl: -d 2
-f | --fyl <fyl nejm> <vejt tym> - eksekjut e fyl; vejt tym is ty sekond
    Eksampl: -f test.piko 1
-k | --klir <ty mod> - klir memori
    Ty eksampl:
        -k (klir ol)
        -k m (klir memori)
        -k p (klir program)

PIKO ty instrakwn:
stor <ad'res'> <valju>
    Eksampl: stor 0 174
tkst <ad'res'> <tekst>
    Eksampl: tkst 0 Xelo vorld!
inkr <ad'res'>
    Eksampl: inkr 0
    174 in ad'res' 0 => 175 in ad'res' 0
qump <program ad'res'>
    Eksampl: qump 3
    Nout: jus program kao tu get ad'res'

Jus #<ad'res'> tu rid valju.
    Eksampl: stor #0 174
    62 in ad'res' 0 => stor 62 174
'''

def set_error(error_text: str) -> None:
    global error
    error = error_text

def write_memory(address: int, value: int) -> None:
    if address >= MEMORY_SIZE:
        set_error(f"Memori ad'res' {address} is tu big, maks memori ad'res' is {MEMORY_SIZE - 1}")
        return
    elif value > MAX_VALUE:
        set_error(f"Value {value} is tu big, maks valju is {MAX_VALUE}")
        return
    memory[address] = value
def read_memory(address: int) -> int:
    if address >= MEMORY_SIZE:
        set_error(f"Memori ad'res' {address} is tu big, maks memori ad'res' is {MEMORY_SIZE - 1}")
        return 0
    return memory[address]

def clear_screen() -> None:
    os.system("cls")
def refresh() -> None:
    clear_screen()
    print("-- PIKO Emulejwn --")

    print(f"[MEMORI | {MEMORY_SIZE} ty byt]", end=" ")
    print(f"[Displej mod: {display_mode_names[display_mode]}]")
    print_memory(0, MEMORY_SIZE)

    print(f"[PROGRAM | {PROGRAM_SIZE} ty byt]")
    print_bytearray(program, 0, PROGRAM_SIZE, mode = 1, highlight = program_pointer)

    print()
    print(f"{CS.cDebug}[?] --xelp or -x for xelp{CS.cReset}")
    if error:
        print()
        print(f"{CS.cError}{error}{CS.cReset}")
        set_error("")
def print_bytearray(ba: bytearray, start: int, end: int, mode: int = 0, highlight: int = -1) -> None:
    line_length: int = 16
    value_width: int = 4
    if mode == 2:
        value_width = 1
        line_length *= 2
    line: str = "─" * line_length * value_width

    start_line: bool = True
    print("┌" + line + "┐")
    for i in range(start, end):
        if start_line:
            print("│", end="")
            start_line = False
        value: int = ba[i]
        value_text: str = str(value)
        if mode == 0:
            value_text = "{0:{width}}".format(value_text, width=value_width)
        elif mode == 1:
            value_text = hex(value)[2:].zfill(2).upper()
            value_text = "{0:{width}}".format(value_text, width=value_width)
        elif mode == 2:
            if value == 0:
                value_text = ' '
            else:
                value_text = chr(value)
        if i == highlight:
            value_text = CS.cHighlight + value_text + CS.cReset
        print(value_text, end = "")
        if (i - start) % line_length == line_length - 1:
            print("│")
            start_line = True
    print("└" + line + "┘")
    if (end - start) % line_length != 0:
        print()
def print_memory(start: int, end: int) -> None:
    print_bytearray(memory, start, end, mode = display_mode)

def get_value(code: str) -> int:
    if code.startswith(VALUE_SYMBOL):
        code = code[1:]
        return read_memory(get_value(code))
    if code.startswith(HEX_SYMBOL):
        code = code.removeprefix(HEX_SYMBOL)
        return int(code, 16)
    return int(code)
def exec_instruction(instruction_code: int, args: list[int]) -> None:
    # store instruction
    instruction: str = instruction_names[instruction_code]
    address: int = args[0]
    if address >= MEMORY_SIZE:
        set_error(f"Ad'res' {address} not alavd. Max ad'res' is {MEMORY_SIZE - 1}")
        return
    if instruction == "stor":
        value: int = args[1]

        hex_address: str = hex(address)[2:]
        if hex_address[0] == "f": # all F_ addresses are registers
            write_memory(read_memory(address), value)
        else: # otherwise store normally
            write_memory(address, value)
    elif instruction == "copi":
        copy_from_address: int = args[1]
        write_memory(address, read_memory(copy_from_address))
    
    elif instruction == "tkst":
        characters: list[int] = args[1:]
        for i in range(len(characters)):
            write_memory(address + i, characters[i])
    elif instruction == "qump":
        global program_pointer, program_write_pointer
        program_pointer = address # jump to the address
        program_write_pointer = address
    
    elif instruction == "inkr":
        write_memory(address, read_memory(address) + 1)
def exec_current_instruction() -> None:
    global program_pointer

    instruction_code: int = program[program_pointer]
    args: list[int] = []
    program_pointer += 1
    if instruction_names[instruction_code] == "tkst":
        address: int = program[program_pointer]
        args.append(address)
        program_pointer += 1

        text_length: int = program[program_pointer]
        program_pointer += 1
        
        for i in range(text_length):
            args.append(program[program_pointer])
            program_pointer += 1
    else:
        for i in range(MIN_ARGS):
            args.append(program[program_pointer])
            program_pointer += 1
    exec_instruction(instruction_code, args)

def parse_instruction(instruction: str) -> bool:
    global program_write_pointer
    instruction_name, *args = instruction.split()
    if instruction_name not in instruction_names:
        set_error(f"Instrakwn \"{instruction_name}\" not ekzist!")
        return False

    # write byte codes for this instruction
    codes: list[int] = [instruction_codes[instruction_name]]
    if instruction_name == "tkst":
        codes.append(int(args[0])) # append the write address
        text: str = " ".join(args[1:])
        codes.append(len(text)) # append text length
        for char in text:
            codes.append(ord(char))
    else:
        for arg in args:
            codes.append(get_value(arg))

    # write byte codes into program data
    for code in codes:
        program[program_write_pointer] = code
        program_write_pointer += 1
    if len(codes) - 1 < MIN_ARGS:
        program_write_pointer += MIN_ARGS - len(codes) + 1
    
    return True
def parse_file(file_name: str) -> None:
    global program_running
    file = open(file_name, "r")
    code: str = file.read()
    file.close()
    line_index: int = 0
    for line in code.splitlines():
        if not parse_instruction(line):
            set_error(f"Fyl \"{file_name}\", lyn {line_index}: {error}")
            return
        line_index += 1
    program_running = True

def main() -> None:
    global display_mode, memory, program, program_pointer, program_write_pointer, wait_time, program_running

    running: bool = True
    while running:
        # if program is running
        while program_running:
            exec_current_instruction()
            if error:
                program_running = False
            elif wait_time:
                refresh()
                time.sleep(wait_time)

        # and this all is live writing and executing the program
        refresh()

        instruction: str = input(">>> ")
        
        if instruction == "" or instruction.isspace():
            exec_current_instruction()
            program_write_pointer = program_pointer
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
            try:
                wait_time = float(args[0])
            except:
                wait_time = MIN_WAIT_TIME
            parse_file(file_name)
        elif instruction.startswith("-k") or instruction.startswith("--klir"):
            _, *args = instruction.split()
            clean_mode: list[str] = ["m", "p"]
            if len(args):
                clean_mode = args
            if "m" in clean_mode:
                memory = bytearray(MEMORY_SIZE)
            if "p" in clean_mode:
                program = bytearray(PROGRAM_SIZE)
                program_pointer = 0
                program_write_pointer = 0
        else:
            if parse_instruction(instruction):
                exec_current_instruction()


main()