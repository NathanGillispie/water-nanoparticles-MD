import sys
import os
import math
import string

if (len(sys.argv)!=2):
	raise NameError("arguments must be number of water molecules!")

number_of_molecules = int(sys.argv[1])

with open('extractdipoles.ptrajin', 'w') as outfile:
	outfile.write("""parm ../md_inputs/water_solvated.prmtop
trajin production.mdcrd 1 last
""")
	for i in range(number_of_molecules):
		outfile.write("vector dipole{0} dipole out dipoles/dipole{0}.dat :{1}\n".format(str(i),str(i+1)))
	outfile.write("vector COM center out COM.dat :WAT\n")
	outfile.write("go\nquit\n")
