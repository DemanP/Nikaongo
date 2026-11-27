# PIKO DOC

## ENGLISH Doc

```txt
Emulation commands:
-x | --xelp                         - print help info
--                                  - exit
-d | --displej <mod>                - change display mode (0 - decimal, 1 - hex, 2 - text)
    Example: -d 2
-e | --eksekjut <wait time>         - execute program until pauz (instruction); wait time is in seconds
-f | --fyl
    <file name> <wait time> <flags> - execute a file; wait time is in seconds
    Flags:
        -w  = show file contents/instructions
    Example: -f test.piko 1
-k | --klir <modes>                 - clear data
    Examples:
        -k (clear all)
        -k m (clear memory)
        -k p (clear program)

Note: press Enter on an empty line to contine execution

PIKO instructions:
stor <address> <value>                      = store value in the address
    Example: stor 0 174
tkst <address> <text>                       = store text starting from the address
    Example: tkst 0 Xelo vorld!

inkr <address>                              = increment value in the address
    Example: inkr 0
    174 in address 0 => 175 in address 0

qump <program address> <condition address>  = jump to address (move program pointer) if value in condition address is 0
    Example: qump 3
    Note: use program interface to get the address or just use labels

pauz                                        = pause (halt) the instructions

Use ! symbol for comments.
Use #<address> to read value (aka use the value from the address).
    Example: stor #0 174
    62 in address 0 => stor 62 174
```

## NIKAONGO Doc

```txt
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
stor <ad'res'> <valju>                    = stor valju in ad'res'
    Eksampl: stor 0 174
tkst <ad'res'> <tekst>                    = stor tekst in ad'res'
    Eksampl: tkst 0 Xelo vorld!

inkr <ad'res'>                            = inkrement valju in ad'res'
    Eksampl: inkr 0
    174 in ad'res' 0 => 175 in ad'res' 0
ksor <ad'res'> <valju>                    = ekslusiv or bitvin valju in ad'res' to valju to stor in ad'res'

qump <program ad'res'> <koniwn ad'res'>   = qump tu ad'res' if valji in kondiwn ad'res' is 0
    Eksampl: qump 3
    Nout: jus program kao tu get ad'res'

pauz                                      = pauz ty instrakwn

Jus ! simbol for ty kom'ent.
Jus #<ad'res'> tu rid valju.
    Eksampl: stor #0 174
    62 in ad'res' 0 => stor 62 174
```
