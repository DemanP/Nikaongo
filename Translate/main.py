import os
import translate as ntr

# SUGGESTION: rename main.py to script.py

os.chdir(os.path.dirname(os.path.abspath(__file__)))

quit_flag: str = "-q"
debug_flag: str = "-d"
debug: bool = False

script_mode: int = 1
# script modes:
# 0 - exit script mode
# 1 - translate English to Nikaongo
# 2 - translate Nikaongo to English
while script_mode:
    # flags resets
    debug = False
    
    text = input(">>> ")
    split_text = text.split(" ")
    flags = list(filter(lambda word: word.startswith('-'), split_text))
    for flag in flags:  # for each found flag, trigger the relative toggle, and remove the flag
        if flag == quit_flag:
            script_mode = 0
            break  # no need to proceed with other flags (for now)
        elif flag == debug_flag:
            print(f"-- Debug On --")
            debug = True
        split_text.remove(flag)

    if script_mode == 1:
        text = "".join(split_text)
        result = ntr.translate(text, debug)
        print(result)