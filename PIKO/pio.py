'''
This is the file for PIO emulation only.

It includes execution of instructions written in the program and ability to change both MEMORY and program data.
'''

MAX_VALUE: int = 255
MEMORY_LINE: int = 16
MEMORY_SIZE: int = MEMORY_LINE * 7
MEMORY_FULL: int = 1 + MEMORY_SIZE * MAX_VALUE

# Easy references for registries and memory
MEMORY: bytearray = bytearray(MEMORY_FULL)
R_0 = MEMORY[0]
R_1 = MEMORY[1]
R_CODE_POINTER = MEMORY[2]
R_CODE_OFFSET = MEMORY[3]
R_4 = MEMORY[4]
R_MEMORY_OFFSET = MEMORY[5]
R_6 = MEMORY[6]
R_7 = MEMORY[7]
R_8 = MEMORY[8]
R_9 = MEMORY[9]
R_A = MEMORY[10]
R_B = MEMORY[11]
R_C = MEMORY[12]
R_D = MEMORY[13]
R_E = MEMORY[14]
R_F = MEMORY[15]


MIN_ARGS: int = 2

PROGRAM_SIZE: int = 256

program_running: bool = False  # TODO move to flags once flag registry is set

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


# -- MEMORY Management --
def write_memory(address: int, value: int) -> None:
    if address >= MEMORY_SIZE:
        # set_error(f"Memori ad'res' {address} is tu big, maks memori ad'res' is {MEMORY_SIZE - 1}")
        return
    elif value > MAX_VALUE:
        # set_error(f"Value {value} is tu big, maks valju is {MAX_VALUE}")
        return
    MEMORY[16 + MEMORY_SIZE*R_MEMORY_OFFSET + address] = value
def read_memory(address: int) -> int:
    if address >= MEMORY_SIZE:
        # set_error(f"Memori ad'res' {address} is tu big, maks memori ad'res' is {MEMORY_SIZE - 1}")
        return 0
    return MEMORY[16 + MEMORY_SIZE*R_MEMORY_OFFSET * address]
def reset_memory() -> None:
    return
#    global MEMORY
#    MEMORY = bytearray(MEMORY_FULL)  # please don't use this actually, i think it might work a bit different than you assume it does, will definitely break registries



# -- Program Management --
def write_program(value: int) -> None:
    if value > MAX_VALUE:
        return
    elif 16 + MEMORY_SIZE*R_CODE_POINTER + R_CODE_POINTER > MEMORY_FULL:
        return
    MEMORY[16 + MEMORY_SIZE*R_CODE_POINTER + R_CODE_POINTER] = value
def read_program() -> int:
    if 16 + MEMORY_SIZE*R_CODE_POINTER + R_CODE_POINTER > MEMORY_FULL:
        return  # TODO fix return
    return MEMORY[16 + MEMORY_SIZE*R_CODE_POINTER + R_CODE_POINTER]
def reset_program() -> None:
    return  # please also don't use this
#    global MEMORY, R_CODE_POINTER
#    program = bytearray(PROGRAM_SIZE)
#    R_CODE_POINTER = 0


def set_program_pointer(address: int) -> None:
    global R_CODE_POINTER, program_running
    R_CODE_POINTER = address
    if R_CODE_POINTER >= PROGRAM_SIZE:
        program_running = False
        R_CODE_POINTER = PROGRAM_SIZE - 1

def increment_program_pointer() -> None:
    set_program_pointer(R_CODE_POINTER + 1)


# -- Instruction execution --
def parse_address(address: int) -> int:
    if address & 0b01110000 == 0b01110000: # 7_ and F_
        address = address & 0b10001111  # keeps registry index and index/value bit
    if address & 0b10000000 != 0:
        address = address & 0b01111111
        address = read_memory(address)
    return address
def exec_instruction(instruction_code: int, args: list[int]) -> None:

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
        global R_CODE_POINTER
        condition_address: int = parse_address(args[1])
        if not read_memory(condition_address):
            R_CODE_POINTER = address # jump to the address

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
def exec_current_instruction() -> None:
    global R_CODE_POINTER

    instruction_code: int = read_program()
    args: list[int] = []
    increment_program_pointer()
    if instruction_names[instruction_code] == "tkst":
        address: int = read_program()
        args.append(address)
        increment_program_pointer()

        text_length: int = read_program()
        increment_program_pointer()
        
        for i in range(text_length):
            args.append(read_program())
            increment_program_pointer()
    else:
        for i in range(MIN_ARGS):
            args.append(read_program())
            increment_program_pointer()
    exec_instruction(instruction_code, args)
