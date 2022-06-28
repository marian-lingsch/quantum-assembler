start:
    SET d1 jump1
    SET d2 jump2
    SET d3 diffusion1
    SET d4 jump3
    SET d5 jump4
    SET d6 diffusion2
    Havoc d0 0 4
    IFTE d0 d2 d1

jump1:
    Phase -1.0 0.0
    setpc d3

jump2:
    SKIP
    SKIP

diffusion1:
    Diffusion
    IFTE d0 d4 d5

jump3:
    Phase -1.0 0.0
    setpc d6

jump4:
    SKIP
    SKIP

diffusion2:
    Diffusion
    STOP