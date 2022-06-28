start:
    Havoc d0 0 2
    SET d1 2
    SET d2 1
    SET d3 1
    SET d4 stop
    SET d5 loop
    IFTE d0 d5 d4

loop:
    MUL d1 d2 d2
    SUB d0 d3 d0
    IFTE d0 d5 d4

stop:
    STOP