{}


energy = 1.000000;
rotinv = 0;
    betax   = 1.0000000; alphax  = 0.0000000;
    etax    = 0.0000000; etaxp   = 0.0000000;
    betay   = 1.0000000; alphay  = 0.0000000;
    etay    = 0.0000000; etayp   = 0.0000000;

{----- variables ---------------------------------------------------}


{----- table of elements ---------------------------------------------}

drift : drift, l = 0.100000, ax = 50.00, ay = 50.00;

quad  : quadrupole, l = 0.100000, k = 2.000000, ax = 50.00, ay = 50.00;
dquad : quadrupole, l = 0.100000, k = 2.000000, ax = 50.00, ay = 50.00;


{----- table of segments ---------------------------------------------}

line      : drift, quad, drift, dquad, drift, quad, drift;
multiline : line, nper=4;

{}
