{}


energy = 1.000000;
rotinv = 0;
    betax   = 1.0000000; alphax  = 0.0000000;
    etax    = 0.0000000; etaxp   = 0.0000000;
    betay   = 1.0000000; alphay  = 0.0000000;
    etay    = 0.0000000; etayp   = 0.0000000;

{----- variables ---------------------------------------------------}

var  = 2;

{----- table of elements ---------------------------------------------}

d1     : drift, l = 0.100000, ax = 50.00, ay = 50.00;

marker : marker, ax = 50.00, ay = 50.00;

foc    : quadrupole, l = 0.100000, k = 4.000000, ax = 50.00, ay = 50.00;
defoc  : quadrupole, l = 0.000000, k = 4.000000, ax = 50.00, ay = 50.00;

nbend  : bending, l = 0.500000, t = -10.000000, k = 0.000000, t1 = 0.000000,
         t2 = 0.000000, ax = 50.00, ay = 50.00;
bend   : bending, l = 0.500000, t = 20.000000, k = 0.000000, t1 = 0.000000,
         t2 = 0.000000, ax = 50.00, ay = 50.00;

sf     : sextupole, l = 0.100000, k = -200.000000, n = 1, ax = 50.00,
         ay = 50.00;
sd     : sextupole, l = 0.100000, k = 200.000000, n = 1, ax = 50.00,
         ay = 50.00;

sol    : solenoid, l = 0.100000,  k = 5.000000, ax = 50.00, ay = 50.00;

und    : undulator, l = 0.100000, lamb = 0.002000, bmax = 1.200000,
         f1 = 0.636620, f2 = 0.500000, f3 = 0.424410, gap = 1000.000,
         ax = 50.00, ay = 50.00;

sept   : septum, l = 0.100000, angle = 2.00000, dist = 2.00, thick = 7.00,
         ax = 50.00, ay = 50.00;

kick   : kicker, l = 0.100000, n = 1,  k = 0.000,  x = 0.000,  t = 0.000,
          delay = 0.000 nk = 1, ax = 50.00, ay = 50.00;

om     : opticsmarker, betax = 1.000000, alphax = 0.000000, betay = 1.000000,
         alphay = 0.000000, etax  = 0.000000, etaxp  = 0.000000,
         etay  = 0.000000, etayp  = 0.000000, ax = 50.00, ay = 50.00;

comb   : combined, l = 0.100000, t = 5.000000, k = 5.000000, t1 = 0.000000,
         t2 = 0.000000, m = 200, n = 1, ax = 50.00, ay = 50.00;

phb    : photonbeam, xl = 20.00, style = 0, snap = 0, ax = 50.00,
         ay = 50.00;

gir    : girder, typ = 0, shift = 0.00000, ax = 50.00, ay = 50.00;

mult   : multipole, n = 2,  k = 2.00000000,  lmag = 0.1000, ax = 50.00,
         ay = 50.00;

mon    : monitor, ax = 50.00, ay = 50.00;

hcor   : h-corrector, ax = 50.00, ay = 50.00;

vcor   : v-corrector, ax = 50.00, ay = 50.00;

rot    : rotation, ax = 50.00, ay = 50.00;


{----- table of segments ---------------------------------------------}

mo : marker;

{}
