# PIKO DOC

## ENGLISH Doc

```txt
Emulation commands:
-x | --xelp - print help info
-d | --displej <mod> - change display mode (0 - decimal, 1 - hex, 2 - text)
    Example: -d 2
-f | --fyl <file name> <wait time> - execute a file; wait time is in seconds
    Example: -f test.piko 1
-k | --klir <modes> - clear
    Examples:
        -k (clear all)
        -k m (clear memory)
        -k p (clear program)

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

Use #<address> to read value (aka use the value from the address).
    Example: stor #0 174
    62 in address 0 => stor 62 174
```

## NIKAONGO Doc

```txt
Emulejwn ty komand:
-x | --xelp - print xelp info
-d | --displej <mod> - cenq displej mod (0 - dehimal, 1 - xeks, 2 - tekst)
    Eksampl: -d 2
-f | --fyl <fyl nejm> <vejt tym> - eksekjut e fyl; vejt tym is ty sekond
    Eksampl: -f test.piko 1
-k | --klir <ty mod> - klir memori
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

Jus #<ad'res'> tu rid valju.
    Eksampl: stor #0 174
    62 in ad'res' 0 => stor 62 174
```
