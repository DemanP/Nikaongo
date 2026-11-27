# https://en.wikipedia.org/wiki/ANSI_escape_code

cReset: str     = "\x1b[0m"
cError: str     = "\x1b[38;2;230;69;83m"
cDebug: str     = "\x1b[38;2;14;80;130m"

cKeyword: str   = "\x1b[38;5;10m"

cHighlight: str = "\x1b[47m"
cRegister: str  = "\x1b[48;5;237m"
cLabels: list[str] = [
    "\x1b[48;5;8m",
    "\x1b[48;5;9m",
    "\x1b[48;5;10m",
    "\x1b[48;5;11m",
    "\x1b[48;5;12m",
    "\x1b[48;5;13m",
    "\x1b[48;5;14m",
    "\x1b[48;5;208m",
    "\x1b[48;5;211m",
    "\x1b[48;5;213m",
]