// If two IFTE have the same jump adress, the program is not reversible
start:
    Havoc d0 0 2
    SET d1 1
    SET d2 loop
    SET d3 stop
    SET d4 0
    IFTE d0 d2 d3

loop:
    SUB d0 d1 d0
    ADD d4 d1 d4
    IFTE d0 d2 d3

stop:
    STOP