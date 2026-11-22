import os
import translate as ntr

os.chdir(os.path.dirname(os.path.abspath(__file__)))

quit_flag: str = "-q"
debug_flag: str = "-d"
debug: bool = False
stop: bool = False
while True:
    # flags resets
    debug = False
    
    text = input(">>> ")
    split_text = text.split(" ")
    flags = list(filter(lambda word: word.startswith('-'), split_text))
    for flag in flags:  # for each found flag, trigger the relative toggle, and remove the flag
        split_text.remove(flag)
        if flag == quit_flag:
            stop = True
            break
        if flag == debug_flag:
            print(f"-- Debug On --")
            debug = True
            continue
    
    if stop:  # stops cycle instead of (going through translate phase, then stopping)
        break
    text = "".join(split_text)

    result = ntr.translate(text, debug)
    print(result)