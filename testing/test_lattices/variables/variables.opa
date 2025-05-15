{..ocuments\programming\oma\testing\test_lattices\variables\variables.opa}


energy = 1.000000;
rotinv = 0;
    betax   = 2.2918668; alphax  = 0.0000000;
    etax    = 1.4748768; etaxp   = 0.0000000;
    betay   = 1.7060698; alphay  = 0.0000000;
    etay    = 0.0000000; etayp   = 0.0000000;

{----- variables ---------------------------------------------------}

angle   = 5;
dangle  = 2*angle;

{----- table of elements ---------------------------------------------}

dr   : drift, l = 0.100000, ax = 50.00, ay = 50.00;

qf   : quadrupole, l = 0.100000, k = -3.655500, ax = 50.00, ay = 50.00;

bend : combined, l = 0.100000, t = dangle, k = 5.000000, t1 = 0.000000,
       t2 = 0.000000, ax = 50.00, ay = 50.00;


{----- table of segments ---------------------------------------------}

cell : dr, qf, dr, bend, dr, qf, dr;

{..ocuments\programming\oma\testing\test_lattices\variables\variables.opa}
