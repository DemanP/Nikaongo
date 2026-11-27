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
stor <address> <value>
    Example: stor 0 174
tkst <address> <text>
    Example: tkst 0 Xelo vorld!
inkr <address>
    Example: inkr 0
    174 in address 0 => 175 in address 0
qump <program address>
    Example: qump 3
    Note: use program interface to get the address

Use ! symbol for comments.
Use #<address> to read value (aka use the value from the address).
    Example: stor #0 174
    62 in address 0 => stor 62 174
```

## NIKAONGO Doc

```txt
Emulejwn ty komand:
-x | --xelp                      - print xelp info
--                               - eksit
-d | --displej <mod>             - cenq displej mod (0 - dehimal, 1 - xeks, 2 - tekst)
    Eksampl: -d 2
-e | --eksekjut <vejt tym>       - eksekjut program antil pauz; vejt tym is ty sekond
-f | --fyl
    <fyl nejm> <vejt tym> <ty fleg> - wryt ty isntrackwn from e fyl to eksekjut kivi; vejt tym is ty sekond
    Ty fleg:
        -w  = wov fyl ty instrakwn
-k | --klir <ty mod>             - klir data
    Ty eksampl:
        -k (klir ol)
        -k m (klir memori)
        -k p (klir program)

PIKO ty instrakwn:
stor <ad'res'> <valju>
    Eksampl: stor 0 174
tkst <ad'res'> <tekst>
    Eksampl: tkst 0 Xelo vorld!
inkr <ad'res'>
    Eksampl: inkr 0
    174 in ad'res' 0 => 175 in ad'res' 0
qump <program ad'res'>
    Eksampl: qump 3
    Nout: jus program kao tu get ad'res'

Jus ! simbol for ty kom'ent.
Jus #<ad'res'> tu rid valju.
    Eksampl: stor #0 174
    62 in ad'res' 0 => stor 62 174
```
