import os, sys, time
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

COMMENT_SYMBOL: str = "!"
VALUE_SYMBOL:   str = "#"
HEX_SYMBOL:     str = "x"

# Display Modes:
# 0 - decimal (default)
# 1 - hex
# 2 - ASCII character
display_mode: int = 0
display_mode_names: list[str] = ["dehimal", "xeks", "tekst"]

instruction_names: dict[int, str] = {
    0:   "stor",
    1:   "copi",
    2:   "tkst",
    3:   "qump",
    4:   "inkr",
    5:   "strr",
    255: "pauz"
}
instruction_codes: dict[str, int] = {}
for i in instruction_names:
    instruction_codes[instruction_names[i]] = i

# console/emulator
running: bool = True
labels: dict[str, int] = {}

error: str = ""
help_info: str =\
f'''
Emulejwn ty komand:
-x | --xelp                         - print xelp info
--                                  - eksit
-d | --displej <mod>                - cenq displej mod (0 - dehimal, 1 - xeks, 2 - tekst)
    Eksampl: -d 2
-e | --eksekjut <vejt tym>          - eksekjut program antil pauz; vejt tym is ty sekond
-f | --fyl
    <fyl nejm> <vejt tym> <ty fleg> - wryt ty isntrackwn from e fyl to eksekjut kivi; vejt tym is ty sekond
    Ty fleg:
        -w  = wov fyl ty instrakwn
    Eksampl: -f test.piko 1 -w
-k | --klir <ty mod>                - klir data
    Ty mod:
        -k   = klir ol
        -k m = klir memori
        -k p = klir program
        -k l = klir ty lejbel
    Eksampl: -k m l <= klir memori to ty lejbel

PIKO ty instrakwn:
{CS.cKeyword}stor{CS.cReset} <ad'res'> <valju>
    Eksampl: stor 0 174
{CS.cKeyword}tkst{CS.cReset} <ad'res'> <tekst>
    Eksampl: tkst 0 Xelo vorld!
{CS.cKeyword}inkr{CS.cReset} <ad'res'>
    Eksampl: inkr 0
    174 in ad'res' 0 => 175 in ad'res' 0
{CS.cKeyword}qump{CS.cReset} <program ad'res'>
    Eksampl: qump 3
    Nout: jus program kao tu get ad'res'

Jus ! simbol for ty kom'ent.
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

def set_program_pointer(address: int) -> None:
    global program_pointer, program_running
    program_pointer = address
    if program_pointer >= PROGRAM_SIZE:
        program_running = False
        program_pointer = PROGRAM_SIZE - 1
def increment_program_pointer() -> None:
    set_program_pointer(program_pointer + 1)

def clear_screen() -> None:
    os.system("cls")
def refresh() -> None:
    clear_screen()
    print("-- PIKO Emulejwn --")

    print(f"[MEMORI | {MEMORY_SIZE} ty byt]", end=" ")
    print(f"[Displej mod: {display_mode_names[display_mode]}]")
    print_memory(0, MEMORY_SIZE)

    print(f"[PROGRAM | {PROGRAM_SIZE} ty byt]")
    print_program(0, PROGRAM_SIZE)

    if len(labels):
        print()
        print("Ty lejbel")
        for i, label in enumerate(labels):
            print(CS.cLabels[i % len(CS.cLabels)] + f"{label} - x{hex(labels[label])[2:].zfill(2).upper()}" + CS.cReset)

    print()
    print(f"{CS.cDebug}[?] --xelp or -x for xelp{CS.cReset}")
    if error:
        print()
        print(f"{CS.cError}{error}{CS.cReset}")
        set_error("")
def print_bytearray(ba: bytearray, start: int, end: int, mode: int = 0, highlights: dict[int, list[str]] = {}) -> None:
    MAX_EMPTY_SYMBOL_VALUE: int = 32
    line_length: int = 16
    value_width: int = 4
    if mode == 2:
        value_width = 1
        line_length *= 2
    line: str = "─" * line_length * value_width

    start_line: bool = True
    print("┌" + line + "┐")
    for index in range(start, end):
        if start_line:
            print("│", end="")
            start_line = False
        value: int = ba[index]
        value_text: str = str(value)
        if mode == 0:
            value_text = "{0:{width}}".format(value_text, width=value_width)
        elif mode == 1:
            value_text = hex(value)[2:].zfill(2).upper()
            value_text = "{0:{width}}".format(value_text, width=value_width)
        elif mode == 2:
            if value < MAX_EMPTY_SYMBOL_VALUE:
                value_text = ' '
            else:
                value_text = chr(value)
        
        if index in highlights:
            value_text_copy = value_text
            value_text = ""
            for char_index, char in enumerate(value_text_copy):
                highlight_index: int = int(char_index / len(value_text_copy) * len(highlights[index]))
                value_text += highlights[index][highlight_index]
                value_text += char
            value_text += CS.cReset
            # value_text = highlights[index][0] + value_text + CS.cReset
        
        print(value_text, end = "")
        if (index - start) % line_length == line_length - 1:
            print("│")
            start_line = True
    print("└" + line + "┘")
    if (end - start) % line_length != 0:
        print()
def print_memory(start: int, end: int) -> None:
    print_bytearray(memory, start, end, mode = display_mode,
                    highlights = {
                        
                    })
def print_program(start: int, end: int) -> None:
    highlights: dict[int, list[str]] = { program_pointer: [CS.cHighlight] }
    for i, label in enumerate(labels):
        label_address: int = labels[label]
        if label_address not in highlights:
            highlights[label_address] = []
        highlights[label_address].append(CS.cLabels[i % len(CS.cLabels)])
    print_bytearray(program, start, end, mode = 1, highlights = highlights)

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
    
    # -- Storing Data --
    if instruction == "stor":
        value: int = args[1]
        write_memory(address, value)

        # hex_address: str = hex(address)[2:]
        # if hex_address[0] == "f": # all F_ addresses are registers
        #     write_memory(read_memory(address), value)
        # else: # otherwise store normally
        #     write_memory(address, value)
    elif instruction == "strr":
        address = read_memory(address)
        # hex_address: str = hex(address)[2:]
        # if hex_address[0] == "f": # all F_ addresses are registers
        value: int = args[1]
        write_memory(address, value)
    elif instruction == "copi":
        copy_from_address: int = args[1]
        write_memory(address, read_memory(copy_from_address))
    elif instruction == "tkst":
        characters: list[int] = args[1:]
        for i in range(len(characters)):
            write_memory(address + i, characters[i])
    
    # -- Addresses --
    elif instruction == "qump":
        global program_pointer, program_write_pointer
        program_pointer = address # jump to the address
        program_write_pointer = address

    # -- Value Manipulations --
    elif instruction == "inkr":
        write_memory(address, read_memory(address) + 1)
    
    # -- Other --
    elif instruction == "pauz":
        global program_running
        program_running = False
def exec_current_instruction() -> None:
    global program_pointer

    instruction_code: int = program[program_pointer]
    args: list[int] = []
    increment_program_pointer()
    if instruction_names[instruction_code] == "tkst":
        address: int = program[program_pointer]
        args.append(address)
        increment_program_pointer()

        text_length: int = program[program_pointer]
        increment_program_pointer()
        
        for i in range(text_length):
            args.append(program[program_pointer])
            increment_program_pointer()
    else:
        for i in range(MIN_ARGS):
            args.append(program[program_pointer])
            increment_program_pointer()
    exec_instruction(instruction_code, args)

def remove_comment(line: str) -> str:
    a = line.split(COMMENT_SYMBOL)
    return a[0]
def analyze_instruction(instruction: str, address: int) -> tuple[int, bool]:
    instruction_name, *args = instruction.split()

    # write byte codes for this instruction
    codes_count: int = 1
    if instruction_name == "tkst":
        codes_count += 2 # add 2 for address and text length
        text: str = " ".join(args[1:])
        codes_count += len(text)
    else:
        codes_count += len(args)

    added_label: bool = instruction_name not in instruction_codes and instruction_name[0].isalpha() and not len(args)
    if added_label:
        labels[instruction_name] = address
    
    return codes_count, added_label
def parse_instruction(instruction: str, write: bool = True) -> bool:
    global program_write_pointer

    # remove the comments
    instruction = remove_comment(instruction)

    # if empty line, there is no instruction, but no error, so return True
    if instruction.isspace() or instruction == "":
        return True

    instruction_name, *_args = instruction.split()
    args: list[str] = []

    # label handling
    for arg in _args:
        if arg in labels:
            arg = str(labels[arg])
        args.append(arg)
    
    if instruction_name not in instruction_codes:
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

    if write:
        # write byte codes into program data
        for code in codes:
            program[program_write_pointer] = code
            program_write_pointer += 1
        if len(codes) - 1 < MIN_ARGS:
            program_write_pointer += MIN_ARGS - len(codes) + 1
    
    return True
def parse_file(file_name: str, show_contents: bool = False) -> None:
    global program_running
    file = open(file_name, "r")
    code: str = file.read()
    file.close()
    
    cleaned_code: str = ""
    for line in code.splitlines():
        cleaned_code += remove_comment(line) + "\n"

    if show_contents:
        clear_screen()
        print("-- Fyl ty instrakwn --")
        print(cleaned_code)
        input()

    analyzed_code: str = ""
    program_address: int = program_write_pointer
    for line in cleaned_code.splitlines():
        if line.isspace() or line == "":
            continue

        length, added_label = analyze_instruction(line, program_address)
        
        if not added_label:
            analyzed_code += line + "\n"
        program_address += length

    # parse the instructions
    line_index: int = 0
    for line in analyzed_code.splitlines():
        if not parse_instruction(line):
            set_error(f"Fyl \"{file_name}\", lyn {line_index}: {error}")
            return
        line_index += 1
    
    program_running = True


def exec_command(command: str) -> None:
    global wait_time, program_pointer, program_write_pointer
    command, *args = command.split()
    if command == "--":
        global running
        running = False
        print(f"{CS.cDebug}Eksit{CS.cReset}")
    elif command in ("-d", "--displej"):
        global display_mode
        d_type = args[0]
        display_mode = int(d_type)
    elif command in ("-x", "--xelp"):
        clear_screen()
        print(help_info)
        input("Pres Enter tu ekzit...")
    elif command in ("-f", "--fyl"):
        file_name, *args = args
        try:
            wait_time = float(args[0])
        except:
            wait_time = MIN_WAIT_TIME
        parse_file(file_name, "-w" in args)
    elif command in ("-k", "--klir"):
        global memory, program
        clean_mode: list[str] = ["m", "p", "l"] # default clean mode is cleaning all
        if len(args):
            clean_mode = args
        if "m" in clean_mode:
            memory = bytearray(MEMORY_SIZE)
        if "p" in clean_mode:
            program = bytearray(PROGRAM_SIZE)
            program_pointer = 0
            program_write_pointer = 0
        if "l" in clean_mode:
            labels.clear()
    elif command in ("-e", "--eksekjut"):
        global program_running
        try:
            wait_time = float(args[0])
        except:
            wait_time = MIN_WAIT_TIME
        program_running = True
    elif command in ("-p", "--pojnter"):
        address: int = 0
        if len(args):
            address_arg: str = args[0]
            if address_arg in labels:
                address = labels[address_arg]
            else:
                address = get_value(address_arg)
        program_pointer = address
        program_write_pointer = address
def console() -> None:
    global running, program_write_pointer, program_running

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
        elif instruction.startswith("-"):
            exec_command(instruction)
        else:
            _, added_label = analyze_instruction(instruction, program_write_pointer)
            if added_label:
                continue

            if parse_instruction(instruction):
                exec_current_instruction()

def main() -> None:
    if len(sys.argv) > 1:
        global wait_time
        wait_time = MIN_WAIT_TIME
        parse_file(sys.argv[1])
    console()

if __name__ == "__main__":
    main()