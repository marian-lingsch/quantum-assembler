// d0 is the number to be factored
SET d0 NUMBER1
SET d1 1

start:
    ADD d1 1 d1
    MOD d0 d1 d2
    IFTE d2 start stop

stop:
    STOP


