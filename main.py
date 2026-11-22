import os
import translate as ntr

os.chdir(os.path.dirname(os.path.abspath(__file__)))

quit_flag: str = "-q"
debug_flag: str = "-d"
debug: bool = False
run: bool = True
while run:
    # flags resets
    debug = False
    
    text = input(">>> ")
    if quit_flag in text:
        run = False
        text = ''.join(text.split(quit_flag))
    if debug_flag in text:
        print(f"-- Debug On --")
        debug = True
        text = ''.join(text.split(debug_flag))
    
    result = ntr.translate(text, debug)
    print(result)