start:
    // The number for which the factors are searched
    SET d0 143
    // Havoc is used in range format
    // Each int is represented by 8 bits
    HAVOC d1 0 8
    SET d2 factor
    SET d3 stop
    IFTE d1 d2 d3

factor:
    MOD d0 d1 d4
    STOP

stop:
    STOP


