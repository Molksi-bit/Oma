{d:\lattices\b3_lat\20269999_final\sfsf4q_2sextfam.opa}


energy = 2.500000;
rotinv = 0;
    betax   = 2.8864275; alphax  = 0.0000000;
    etax    = 0.0000000; etaxp   = 0.0000000;
    betay   = 3.1155242; alphay  = 0.0000000;
    etay    = 0.0000000; etayp   = 0.0000000;

{----- variables ---------------------------------------------------}

vrb     = -0.28;
vbb     = 4.25-2.0*vrb;
vmqdwb  = 0.18;
vmb     = 2.75-vmqdwb;

{----- table of elements ---------------------------------------------}

lo     : drift, l = 0.025000, ax = 300.00, ay = 300.00;
l1     : drift, l = 0.100000, ax = 300.00, ay = 300.00;
ml1    : drift, l = 0.100000, ax = 300.00, ay = 300.00;
ml2    : drift, l = 0.100000, ax = 300.00, ay = 300.00;
ml3    : drift, l = 0.100000, ax = 300.00, ay = 300.00;
ml4    : drift, l = 0.100000, ax = 300.00, ay = 300.00;
ul1    : drift, l = 0.100000, ax = 300.00, ay = 300.00;
ul2    : drift, l = 0.100000, ax = 300.00, ay = 300.00;
ul3    : drift, l = 0.180000, ax = 300.00, ay = 300.00;
ul4    : drift, l = 0.100000, ax = 300.00, ay = 300.00;
ul5    : drift, l = 2.800000, ax = 300.00, ay = 300.00;

qd     : quadrupole, l = 0.130000, k = -9.178248, ax = 9.00, ay = 9.00;
uq1    : quadrupole, l = 0.100000, k = 8.622044, ax = 9.00, ay = 9.00;
uq2    : quadrupole, l = 0.200000, k = -9.061654, ax = 9.00, ay = 9.00;
uq3    : quadrupole, l = 0.250000, k = 9.292629, ax = 9.00, ay = 9.00;
uq4    : quadrupole, l = 0.100000, k = -9.636278, ax = 9.00, ay = 9.00;
mqf    : quadrupole, l = 0.180000, k = 9.260511, ax = 50.00, ay = 300.00;

bb     : bending, l = 0.550000, t = vbb/2.0, k = 0.000000, t1 = vbb/2.0,
         t2 = 0.000000, ax = 50.00, ay = 300.00;
mb     : bending, l = 0.750000, t = vmb, k = 0.000000, t1 = vmb/2.0,
         t2 = vmb/2.0, ax = 50.00, ay = 300.00;

sd     : sextupole, l = 0.050000, k = -240.375491, n = 1, ax = 300.00,
         ay = 300.00;
sf     : sextupole, l = 0.050000, k = 264.999571, n = 1, ax = 300.00,
         ay = 300.00;

om_sf  : opticsmarker, betax = 5.786310, alphax = 0.000000, betay = 2.828970,
         alphay = 0.000000, etax  = 0.058092, etaxp  = 0.000000,
         etay  = 0.000000, etayp  = 0.000000, ax = 50.00, ay = 50.00;
om_mb1 : opticsmarker, betax = 1.214774, alphax = -2.023980, betay = 6.281589,
         alphay = -0.123894, etax  = 0.000000, etaxp  = 0.000000,
         etay  = 0.000000, etayp  = 0.000000, ax = 50.00, ay = 50.00;
om_c   : opticsmarker, betax = 0.410624, alphax = 0.000000, betay = 5.370696,
         alphay = 0.000000, etax  = 0.009545, etaxp  = 0.000000,
         etay  = 0.000000, etayp  = 0.000000, ax = 50.00, ay = 50.00;

mqdwb  : combined, l = 0.150000, t = vmqdwb, k = -8.454023, t1 = vmqdwb/2.0,
         t2 = vmqdwb/2.0, ax = 9.00, ay = 9.00;
rb     : combined, l = 0.170000, t = vrb, k = 8.642872, t1 = vrb/2.0,
         t2 = vrb/2.0, ax = 50.00, ay = 300.00;


{----- table of segments ---------------------------------------------}

uc    : om_sf, sf, l1, rb, l1, qd, l1, sd, sd, l1, bb, -bb, l1, sd, sd, l1, qd,
        l1, rb, l1, sf, om_sf;
dc    : om_sf, sf, ml1, mqf, ml2, mqdwb, ml3, sd, sd, ml4, mb, om_mb1;
arc   : -dc, -uc, -uc, om_c, uc, uc, dc;
mund  : om_mb1, ul1, uq1, ul2, uq2, ul3, uq3, ul4, uq4, ul5;
sec   : -mund, arc, mund;
sech  : om_c, uc, uc, dc, mund;
sec16 : -mund, arc, mund, nper=16;
sec2  : 2*sec;
ring  : 16*sec;

{d:\lattices\b3_lat\20269999_final\sfsf4q_2sextfam.opa}
