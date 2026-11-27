'''
This is the file for PIO emulation only.

It includes execution of instructions written in the program and ability to change both memory and program data.
'''

MAX_VALUE: int = 255
MEMORY_SIZE: int = 128
memory: bytearray = bytearray(MEMORY_SIZE)

MIN_ARGS: int = 2

PROGRAM_SIZE: int = 256
program: bytearray = bytearray(PROGRAM_SIZE)
program_write_pointer: int = 0
program_pointer: int = 0
program_running: bool = False

instruction_names: dict[int, str] = {
    0:   "stor",
    1:   "copi",
    2:   "tkst",
    3:   "qump",
    4:   "inkr",
    5:   "ksor",
    
    255: "pauz"
}
instruction_codes: dict[str, int] = {}
for i in instruction_names:
    instruction_codes[instruction_names[i]] = i


# -- Memory Management --
def write_memory(address: int, value: int) -> None:
    if address >= MEMORY_SIZE:
        # set_error(f"Memori ad'res' {address} is tu big, maks memori ad'res' is {MEMORY_SIZE - 1}")
        return
    elif value > MAX_VALUE:
        # set_error(f"Value {value} is tu big, maks valju is {MAX_VALUE}")
        return
    memory[address] = value
def read_memory(address: int) -> int:
    if address >= MEMORY_SIZE:
        # set_error(f"Memori ad'res' {address} is tu big, maks memori ad'res' is {MEMORY_SIZE - 1}")
        return 0
    return memory[address]
def reset_memory() -> None:
    global memory
    memory = bytearray(MEMORY_SIZE)

# -- Program Management --
def write_program(address: int, value: int) -> None:
    if address >= PROGRAM_SIZE:
        return
    elif value > MAX_VALUE:
        return
    program[address] = value
def read_program(address: int) -> int:
    if address >= PROGRAM_SIZE:
        return
    return program[address]
def reset_program() -> None:
    global program, program_pointer, program_write_pointer
    program = bytearray(PROGRAM_SIZE)   
    program_pointer = 0
    program_write_pointer = 0

def set_program_pointer(address: int) -> None:
    global program_pointer, program_write_pointer, program_running
    program_pointer = address
    if program_pointer >= PROGRAM_SIZE:
        program_running = False
        program_pointer = PROGRAM_SIZE - 1
        program_write_pointer = program_pointer
def increment_program_pointer() -> None:
    set_program_pointer(program_pointer + 1)


# -- Instruction execution --
def parse_address(address: int) -> int:
    if address & 0b10000000 != 0:
        address = address & 0b01111111
        address = read_memory(address)
    return address
def exec_instruction(instruction_code: int, args: list[int]) -> None:
    global program_write_pointer

    # store instruction
    instruction: str = instruction_names[instruction_code]
    address: int = parse_address(args[0])
    
    if address >= MEMORY_SIZE:
        # set_error(f"Ad'res' {address} not alavd. Max ad'res' is {MEMORY_SIZE - 1}")
        return
    
    # -- Storing Data --
    if instruction == "stor":
        value: int = args[1]
        write_memory(address, value)
    elif instruction == "strr":
        address = read_memory(address)
        # hex_address: str = hex(address)[2:]
        # if hex_address[0] == "f": # all F_ addresses are registers
        value: int = parse_address(args[1])
        write_memory(address, value)
    elif instruction == "copi":
        copy_from_address: int = parse_address(args[1])
        write_memory(address, read_memory(copy_from_address))
    elif instruction == "tkst":
        characters: list[int] = args[1:]
        for i in range(len(characters)):
            write_memory(address + i, characters[i])
    
    # -- Addresses --
    elif instruction == "qump":
        global program_pointer
        condition_address: int = parse_address(args[1])
        if not read_memory(condition_address):
            program_pointer = address # jump to the address
            program_write_pointer = address

    # -- Value Manipulations --
    elif instruction == "inkr":
        write_memory(address, read_memory(address) + 1)
    elif instruction == "ksor":
        value: int = args[1]
        value = read_memory(address) ^ value
        write_memory(address, value)
    
    # -- Other --
    elif instruction == "pauz":
        global program_running
        program_running = False
        program_write_pointer = program_pointer
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
