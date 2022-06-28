start:
    Havoc d0 0 2
    SET d1 mul
    SET d2 2
    SET d4 1
    ADD d0 d1 d3
    SETPC d3

mul:
    MUL d4 d2 d4
    MUL d4 d2 d4
    MUL d4 d2 d4
    MUL d4 d2 d4
    STOP

