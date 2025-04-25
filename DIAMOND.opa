{D:\Profile\a3673\Desktop\Masterarbeit\code\translated_files\DIAMOND.opa}



energy = 3.0;
rotinv = 0;
    betax   = 0.1000000; alphax  = 0.0000000;
    etax    = 0.0000000; etaxp   = 0.0000000;
    betay   = 0.1000000; alphay  = 0.0000000;
    etay    = 0.0000000; etayp   = 0.0000000;


{----- variables ---------------------------------------------------}


{----- table of elements ---------------------------------------------}
Q1: quadrupole, l=0.4, k =-0.83895, ax = 50.00, ay = 50.00;
Q2: quadrupole, l=0.6, k =1.306257, ax = 50.00, ay = 50.00;
Q3: quadrupole, l=0.4, k =-0.9689, ax = 50.00, ay = 50.00;
Q4: quadrupole, l=0.4, k =-0.541851, ax = 50.00, ay = 50.00;
Q5: quadrupole, l=0.6, k =1.47457, ax = 50.00, ay = 50.00;
Q6: quadrupole, l=0.4, k =-1.06217, ax = 50.00, ay = 50.00;
Q8: quadrupole, l=0.4, k =1.31013, ax = 50.00, ay = 50.00;
Q7: quadrupole, l=0.4, k =-0.91025, ax = 50.00, ay = 50.00;
Q9: quadrupole, l=0.4, k =0.513758, ax = 50.00, ay = 50.00;
Q10: quadrupole, l=0.4, k =-1.32386, ax = 50.00, ay = 50.00;
Q11: quadrupole, l=0.6, k =1.25454, ax = 50.00, ay = 50.00;
Q12: quadrupole, l=0.4, k =-0.65258, ax = 50.00, ay = 50.00;
BB: bending, l=1.4, t = 11.250026307393714, k = 0.0, t1 = 5.624955857917344, t2 = 5.624955857917344, ax = 50.00, ay = 50.00;
S1: sextupole, l=0.3, k =25.909, n = 1, ax = 50.00, ay = 50.00;
S2: sextupole, l=0.2, k =-22.483, n = 1, ax = 50.00, ay = 50.00;
DK: drift, l=2.92, ax = 300.00, ay = 300.00;
DQ: drift, l=0.71, ax = 300.00, ay = 300.00;
DQR: drift, l=0.56, ax = 300.00, ay = 300.00;
DLR: drift, l=0.5, ax = 300.00, ay = 300.00;
DL: drift, l=0.5, ax = 300.00, ay = 300.00;
D2: drift, l=0.5, ax = 300.00, ay = 300.00;
D3: drift, l=0.52, ax = 300.00, ay = 300.00;
D4A: drift, l=0.3, ax = 300.00, ay = 300.00;
D5: drift, l=0.3, ax = 300.00, ay = 300.00;
D4B: drift, l=0.15, ax = 300.00, ay = 300.00;
MD4: drift, l=0.3, ax = 300.00, ay = 300.00;
MD5: drift, l=0.5, ax = 300.00, ay = 300.00;
MDK: drift, l=9.97, ax = 300.00, ay = 300.00;


{----- table of segments ---------------------------------------------}
ACHROMAT:  BB, D3, Q7, D4A, S2, D4B, Q8, D5, S1, D5, Q8, D4B, S2, D4A, Q7, D3, BB;
HIGHBETA:  DK, Q1, DL, Q2, DQ, Q3, D2;
LOWBETA:  DK, Q4, DL, Q5, DQ, Q6, D2;
RACEBETA:  MDK, Q12, DLR, Q11, DQR, Q10, MD4, Q9, MD5;
BASIC:  RACEBETA, ACHROMAT, -LOWBETA, LOWBETA, ACHROMAT, -HIGHBETA, HIGHBETA, ACHROMAT, -LOWBETA, LOWBETA, ACHROMAT, -HIGHBETA;
RING:  BASIC, -BASIC;


{D:\Profile\a3673\Desktop\Masterarbeit\code\translated_files\DIAMOND.opa}