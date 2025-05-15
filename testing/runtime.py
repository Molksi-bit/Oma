#File for runtime research

import at
import numpy as np
import datetime

#Initiate sfsf4q lattice
e =2.5e9
vrb = np.deg2rad(-0.28)
vbb = np.deg2rad(4.25)-2*vrb
vmqdwb = np.deg2rad(0.18)
vmb = np.deg2rad(2.75)-vmqdwb

#Driftspaces
ds = at.Drift("ds", 0.0)
lo = at.Drift("lo", 0.025)
l1 = at.Drift("l1", 0.1)
l2 = at.Drift("l2", 0.0)
ml1 = at.Drift("ml1", 0.1)
ml2 = at.Drift("ml2", 0.1)
ml3 = at.Drift("ml3", 0.1)
ml4 = at.Drift("ml4", 0.1)
ul1 = at.Drift("ul1", 0.1)
ul2 = at.Drift("ul2", 0.1)
ul3 = at.Drift("ul3", 0.18)
ul4 = at.Drift("ul4", 0.1)
ul5 = at.Drift("ul5", 2.8)

#Quadrupoles
qd  = at.Quadrupole("qd", 0.13, -9.178248)#-9.178248
uq1 = at.Quadrupole("uq1",0.1, 8.622044)
uq2 = at.Quadrupole("uq2",0.2, -9.061654)
uq3 = at.Quadrupole("uq3",0.25, 9.292629)
uq4 = at.Quadrupole("uq4",0.1, -9.636278)
mqf = at.Quadrupole("mqf",0.18, 9.260511)
mqd = at.Quadrupole("mqd",0.13, -9.178248 )


#Bends
bb = at.Dipole("bb", 1.1,vbb, entry_angle = vbb/2,exit_angle =vbb/2)
mb = at.Dipole("mb",0.75,vmb, entry_angle=vmb/2,exit_angle= vmb/2)

#Sextupoles
sd = at.Sextupole("sd", 0.05, -240.375491)
sf = at.Sextupole("sf", 0.05, 264.999571)

#Combined function reverse bends
mqdwb = at.Dipole("mqdwb", 0.15, vmqdwb,-8.454023)
rb =at.Dipole("rb", 0.17, vrb, 8.642872)

#Marker

Mstart = at.Marker("Mstart")
Mend = at.Marker("Mend")
Bstart= at.Marker("Bstart")
Bend= at.Marker("Bend")
Cstart= at.Marker("Cstart")
Cend= at.Marker("Cend")
Sstart= at.Marker("Sstart")
Send= at.Marker("Send")
Rstart= at.Marker("Rstart")
Rend= at.Marker("Rend")


matching_list = [Mstart,ul5,uq4,ul4,uq3,ul3,uq2,ul2,uq1,ul1,Mend]
DC_list = []
bump_list = [Bstart,mb,ml4,sd,sd,ml3,mqdwb,ml2,mqf,ml1,sf,sf,l1,rb,l1,mqd,l1,sd,sd,l1,Bend]
UC_half = [bb,l1,sd,sd,l1,qd,l1,rb,l1,sf]
UC = [sf,l1,rb,l1,qd,l1,sd,sd,l1,bb,l1,sd,sd,l1,qd,l1,rb,l1,sf]
center_list =[Cstart]+ UC_half + UC+UC+ UC_half[::-1] +[Cend]
sector_list =[Sstart]+ matching_list + bump_list+ center_list+ bump_list[::-1]+matching_list[::-1]+[Send]
ring = at.Lattice(sector_list, name= "Old", energy = e)

#runtime functions
runtimes = []
for i in range(10):
    t_start = datetime.datetime.now()


    t_end = datetime.datetime.now()
    runtimes.append((t_end-t_start).total_seconds())
print(f"Average Runtime: {np.mean(runtimes):.6f}s")

