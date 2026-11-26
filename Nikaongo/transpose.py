text: str =\
'''I am trying
to tranpose this!
Please help...'''
lines: list[str] = text.splitlines()

separator: str = " "
separation_width: int = 1

transposed: str = ""
transposed_list: list[str] = []
run: bool = True
char_index: int = 0
while run:
    any_line_going = False
    for line in lines:
        if char_index < len(line):
            any_line_going = True
            transposed += line[char_index]
        else:
            transposed += separator
        transposed += separator * separation_width
    if not any_line_going:
        run = False
    transposed += '\n'
    char_index += 1
print(transposed)