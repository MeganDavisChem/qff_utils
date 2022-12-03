#!/usr/bin/python
#run as missingcheck.py <filename> <# points>
import os 
from sys import argv
#read in energy.dat
#energy_file = open("energy.dat", "r")
energy_file = open("{}".format(argv[1]), "r")
energies = energy_file.readlines()
energy_file.close()
#specify qffSize
qffSize = int(argv[2])
master = 'master.cl.olemiss.edu'

if argv[3] == 'cfour':
    cfour = True
else:
    cfour = False

#initialize stuff
miss = 1
missing = False
missing_numbers = []

#start searching through energies
for i in range(0,len(energies)):
    #set current number to iteration + number of missing points
    j = i + miss

    if os.uname()[1] == 'sequoia' or cfour:
        number = '{:04}/'.format(j)
    else:
        number = '{:04}.'.format(j)

    #check if current number is missing
    if not (number in energies[i]):
        missing = True

    #iterate over missing points until one is found
    while missing:
        miss = miss + 1
        missing_numbers.append(number)
        j = i + miss
        if os.uname()[1] == 'sequoia' or cfour:
            number = '{:04}/'.format(j)
        else:
            number = '{:04}.'.format(j)
        #return to main loop once a number is found
        if number in energies[i]:
            missing = False

#check for final point
if os.uname()[1] == 'sequoia' or cfour:
    if not ('{:04}/'.format(qffSize) in energies[-1]):
        missing_numbers.append('{:04}/'.format(qffSize))
else:
    if not ('{:04}.'.format(qffSize) in energies[-1]):
        missing_numbers.append('{:04}.'.format(qffSize))


#write submit script for eland or mcsr
missingscript = "submiss_{}".format(argv[1].split(".")[0])

f = open(missingscript,"w")
if os.uname()[1] == master:
    if cfour:
        for num in missing_numbers:
            f.write("(cd "+num+" && sbatch ZMAT.sh)\n")
    else:
        for num in missing_numbers:
            f.write("sbatch *"+num+'sh\n')
elif os.uname()[1] == 'sequoia':
    for num in missing_numbers:
        f.write("(cd "+num+" && qsub ZMAT.pbs)\n")
else:
    for num in missing_numbers:
        f.write("qsub *"+num+'pbs\n')
f.close()
os.chmod(missingscript, 0755)
