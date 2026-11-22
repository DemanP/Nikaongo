import os
import translate as ntr

# SUGGESTION: rename main.py to script.py

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Flags:
quit_flag: str = "-q"
debug_flag: str = "-d"
debug_persistent_flag: str = "-dp"
skip_flag: str = "--"

debug_persistent: bool = False

script_mode: int = 1
# script modes:
# 0 - exit script mode
# 1 - translate English to Nikaongo
# 2 - translate Nikaongo to English
while script_mode:
    # flags resets
    debug = debug_persistent
    
    text = input(">>> ")
    if not text:
        script_mode = 0
        print("Fast Quit")

    split_text = text.split(" ")
    flags = list(filter(lambda word: word.startswith('-'), split_text))
    skips: list[int] = []
    word_skipped: list[str] = []

    for flag in flags:  # for each found flag, trigger the relative toggle, and remove the flag
        if flag == quit_flag:
            script_mode = 0
            print(f"-- script set to Quit mode --")
            break  # no need to proceed with other flags (for now)
        elif flag == debug_flag:
            print(f"-- Debug Toggled --")
            debug = not debug
        elif flag == debug_persistent_flag:
            print(f"-- Debug persistent toggle set to {not debug_persistent} --")
            debug_persistent = not debug_persistent
            debug = debug_persistent
        elif flag == skip_flag:
            skips.append(split_text.index(flag))
        split_text.remove(flag)

    if script_mode == 1:
        for i in skips:
            word_skipped.append(split_text[i])
            split_text[i] = "__SKIP__"
        word_skipped.append("")
        result = ""
        texts = " ".join(split_text).split("__SKIP__")
        for text in texts:
            result_part = ntr.translate(text, debug)
            result += result_part + word_skipped.pop(0)
        print(result)