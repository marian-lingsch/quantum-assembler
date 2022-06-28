start:
    SET d1 jump1
    SET d2 jump2
    SET d3 diffusion
    Havoc d0 0 4
    IFTE d0 d2 d1

jump1:
    Phase -1.0 0.0
    setpc d3

jump2:
    SKIP
    SKIP

diffusion:
    Diffusion
    STOP
