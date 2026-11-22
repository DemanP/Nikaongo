import os
import translate as ntr
import text_colors as CS

# SUGGESTION: rename main.py to script.py

os.system("")  # for magic
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
        print(f"{CS.cDebug}Fast Quit{CS.cr}")

    split_text = text.split(" ")
    flags = list(filter(lambda word: word.startswith('-'), split_text))
    skips: list[int] = []
    word_skipped: list[str] = []

    for flag in flags:  # for each found flag, trigger the relative toggle, and remove the flag
        if flag == quit_flag:
            script_mode = 0
            print(f"{CS.cDebug}-- script set to Quit mode --{CS.cr}")
            break  # no need to proceed with other flags (for now)
        elif flag == debug_flag:
            print(f"{CS.cDebug}-- Debug Toggled --{CS.cr}")
            debug = not debug
        elif flag == debug_persistent_flag:
            debug_persistent = not debug_persistent
            print(f"{CS.cDebug}-- Debug persistent toggle set to {CS.c174 if debug_persistent else CS.c741}{debug_persistent}{CS.cDebug} --{CS.cr}")
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
            print(CS.cDebug, end='')
            result_part = ntr.translate(text, debug)
            result_str = result_part[0]
            result += result_str + word_skipped.pop(0)
        print(CS.cr, result)