import sys
import string
import os

input = '2_eq.cdl'
output = '2_eq+so2.cdl'
rst_out = output.split('.')[0] + '.rst'

if (not os.path.exists(input)):
	if (os.path.exists("2_eq.rst")):
		os.system("ncdump 2_eq.rst > 2_eq.cdl")
	else:
		print("check input files")
		sys.exit()

atom_line = 3
position_line = 1153
velocity_line = 2272
lengths_line = 2281

with open(input, 'r') as textfile:
	lines = textfile.readlines()

if len(lines) > lengths_line: 
	lines[atom_line] = "	atom = 1127 ;\n"
	lines[position_line].split
	lines[position_line] = lines[position_line].split(";")[0][:-1] + ',' + """
  55.0, 21.0, 11.0,
  55.0, 21.0, 12.4632,
  53.8051, 21.68966, 10.51218, 
  56.19482, 21.68976, 10.51198,
  55.0, 19.6203, 10.51248,
  55.0, 11.0, 11.0,
  55.0, 11.0, 12.4632,
  53.8051, 11.68966, 10.51218, 
  56.19482, 11.68976, 10.51198,
  55.0, 9.6203, 10.51248 ;
"""
	lines[velocity_line] = lines[velocity_line].split(";")[0][:-1] + ',' + """
  0.0986198371867947, 0.176258975883912, 0.126565219156263,
  0.124721981646369, -0.109159348948368, -0.135879248014089,
  -0.152937279252986, -0.127448045307781, -0.185378047259104, 
 -0.892943612734045, -1.43893565119664, -0.99095133078249,
  -0.0581562958389957, -0.0378204364586102, -0.18881653654859,
  0.837076522246773, 0.14403568778562, 0.282161359443848,
  0.711578549189854, 0.305418045325057, 0.798439072426564,
  -0.0092732376408462, -0.204833445375591, 0.160901361983327,
  0.0957076013680753, -0.0484351726846302, -1.02233564847374,
  1.08348389068325, -0.160954201079178, 1.67604340000654 ;
"""
	lengths_split = lines[lengths_line].split(" ")
	lengths_split[3] = '90.000000000000,'
	lines[lengths_line] = " ".join(lengths_split)

with open(output, 'w') as outfile:
	outfile.writelines(lines)


if (not os.path.exists(rst_out)):
	os.system("ncgen -o " + rst_out + " " + output)
else:
	print("not writing output!")

os.system("rm " + input)
os.system("rm " + output)
