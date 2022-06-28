start:
    // The number for which the factors are searched
    SET d0 NUMBER1
    // Havoc is used in range format
    // Each int is represented by 8 bits
    HAVOC d1 0 NUMBER2
    ADD d1 2 d1
    MOD d0 d1 d2
    // d3 amount of iterations of grover's algorithm
    ADD d0 0 d3
    SQRT d3 d3
    DIV d3 4 d3
    MUL d3 3 d3


grover1:
    IFTE d2 jumpTrue1 jumpFalse1

jumpFalse1:
    Phase -1.0 0.0
    IFTE 1 diffusion1 0

jumpTrue1:
    SKIP
    IFTE 1 diffusion1 0

diffusion1:
    Diffusion
    SUB d3 1 d3
    IFTE d3 stop1 grover1

stop1:
    STOP