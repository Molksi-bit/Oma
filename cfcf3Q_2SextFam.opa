{d:\lattices\b3_lat\20269999_final\cfcf3q_2sextfam.opa}


energy = 2.500000;
rotinv = 0;
    betax   = 2.8137431; alphax  = 0.0000000;
    etax    = -0.0000001; etaxp   = 0.0000000;
    betay   = 2.7997862; alphay  = 0.0000000;
    etay    = 0.0000000; etayp   = 0.0000000;

{----- variables ---------------------------------------------------}

vrb   = -0.39;
vbb   = 4.25-2.0*vrb;
vmrb  = -0.155;
vmb  = 2.75-vmrb;

{----- table of elements ---------------------------------------------}

l1    : drift, l = 0.100000, ax = 9.00, ay = 9.00;
ml1   : drift, l = 0.100000, ax = 9.00, ay = 9.00;
ml2   : drift, l = 0.100000, ax = 9.00, ay = 9.00;
ml3   : drift, l = 0.100000, ax = 9.00, ay = 9.00;
ul1   : drift, l = 0.241980, ax = 9.00, ay = 9.00;
ul2   : drift, l = 0.100000, ax = 9.00, ay = 9.00;
ul3   : drift, l = 0.100000, ax = 9.00, ay = 9.00;
ul4   : drift, l = 2.800000, ax = 9.00, ay = 9.00;

uq1   : quadrupole, l = 0.130000, k = -9.342120, ax = 9.00, ay = 9.00;
uq2   : quadrupole, l = 0.280000, k = 9.339833, ax = 9.00, ay = 9.00;
uq3   : quadrupole, l = 0.100000, k = -9.026187, ax = 9.00, ay = 9.00;

sd    : sextupole, l = 0.085000, k = -239.107989, n = 1, ax = 9.00,
        ay = 9.00;
sf    : sextupole, l = 0.130000, k = 242.939426, n = 1, ax = 9.00,
        ay = 9.00;

om_sd : opticsmarker, betax = 2.179736, alphax = 3.762785, betay = 4.487305,
        alphay = -4.575341, etax  = 0.028956, etaxp  = -0.055828,
        etay  = 0.000000, etayp  = 0.000000, ax = 9.00, ay = 9.00;
om_sf : opticsmarker, betax = 4.599550, alphax = 0.000000, betay = 2.407890,
        alphay = 0.000000, etax  = 0.043539, etaxp  = 0.000000,
        etay  = 0.000000, etayp  = 0.000000, ax = 9.00, ay = 9.00;
om_mb : opticsmarker, betax = 0.890413, alphax = -2.246725, betay = 10.234342,
        alphay = 1.067220, etax  = 0.000000, etaxp  = 0.000000,
        etay  = 0.000000, etayp  = 0.000000, ax = 9.00, ay = 9.00;
om_c  : opticsmarker, betax = 4.500085, alphax = 0.000000, betay = 2.297857,
        alphay = -0.000001, etax  = 0.042384, etaxp  = 0.000000,
        etay  = 0.000000, etayp  = 0.000000, ax = 9.00, ay = 9.00;

bb    : combined, l = 1.000000, t = vbb, k = -1.396722, t1 = vbb/2.0,
        t2 = vbb/2.0, ax = 9.00, ay = 9.00;
mb    : combined, l = 0.700000, t = vmb, k = -1.199612, t1 = vmb/2.0,
        t2 = vmb/2.0, ax = 9.00, ay = 9.00;
rb    : combined, l = 0.150000, t = vrb, k = 7.163088, t1 = vrb/2.0,
        t2 = vrb/2.0, ax = 9.00, ay = 9.00;
mrb   : combined, l = 0.150000, t = vmrb, k = 8.409807, t1 = vmrb/2.0,
        t2 = vmrb/2.0, ax = 9.00, ay = 9.00;


{----- table of segments ---------------------------------------------}

uc    : om_sf, sf, l1, rb, l1, sd, om_sd, sd, l1, bb, l1, sd, om_sd, sd, l1,
        rb, l1, sf, om_sf;
dc    : om_sf, sf, ml1, mrb, ml3, sd, om_sd, sd, ml2, mb, om_mb;
arc   : -dc, uc, uc, om_c, uc, uc, dc;
mund  : om_mb, ul1, uq1, ul2, uq2, ul3, uq3, ul4;
sec   : -mund, arc, mund;
sech  : om_c, uc, uc, dc, mund;
sec16 : -mund, arc, mund, nper=16;
ring  : 16*sec;

{d:\lattices\b3_lat\20269999_final\cfcf3q_2sextfam.opa}
