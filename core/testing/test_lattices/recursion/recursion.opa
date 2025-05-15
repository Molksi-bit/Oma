{..ocuments\programming\oma\testing\test_lattices\recursion\recursion.opa}


energy = 1.000000;
rotinv = 0;
    betax   = 1.0104634; alphax  = 0.0000000;
    etax    = 0.4658124; etaxp   = 0.0000000;
    betay   = 2.1050007; alphay  = 0.0000000;
    etay    = 0.0000000; etayp   = 0.0000000;

{----- variables ---------------------------------------------------}


{----- table of elements ---------------------------------------------}

dr : drift, l = 0.200000, ax = 50.00, ay = 50.00;

qd : quadrupole, l = 0.100000, k = 5.000000, ax = 50.00, ay = 50.00;
qf : quadrupole, l = 0.100000, k = -2.000000, ax = 50.00, ay = 50.00;

cf : combined, l = 0.100000, t = 12.250000, k = -5.000000, t1 = 0.000000,
     t2 = 0.000000, ax = 50.00, ay = 50.00;


{----- table of segments ---------------------------------------------}

half : qd, dr, cf;
full : half, -half;

{..ocuments\programming\oma\testing\test_lattices\recursion\recursion.opa}
