import os
import math
import sys
import string

# Possible values: "angle" and "velocity"
# This is to decide which parameters to change when
# altering the velocities in the check files.
modify = "angle"

# REMEMBER TO SUBTRACT ONE FROM THE LINE NUBMER IN YOUR TEXT EDITOR 
# (assuming they start numbering at 0)
velocity_line = 4526

number_of_runs = 29 #number of trials to generate
number_of_digits = 2 #used for zero-padding in the file naming

# describes names of directories to be generated/used
checks_dir = "chk_multi"
trajectories_dir = "ptj_multi"
pbs_dir = "pbs_multi"
ptrajin_dir = "ptj_multi/ptrajin"
queue_file = "MULTI_PROD.sh"

def queue_file_gen():
	if (os.path.exists(queue_file)):
		input = ""
		while (input != "y") and (input != "n"):
			input = raw_input("Queue file exists. Would you like to replace it? (y/n)\n")
		if input == 'n':
			return
	else:
		print("Queue file does not exist. Generating...")
	with open(queue_file, 'w') as outfile:
		for counter in range(number_of_runs):
			c_string = str(counter+1).zfill(number_of_digits)
			filename = os.path.join(pbs_dir,"4_PRODUCTION-NVT_{0}.pbs\n".format(c_string))
			outfile.write("qsub " + filename)
	os.system("chmod +x " + queue_file)

def check_files_gen():
	input = os.path.join('checkpoints','3_eq-so2.cdl')
	output = os.path.join(checks_dir,'4.cdl')
	rst_in = input.split('.')[0] + '.rst'
	rst_out_str = output.split('.')[0] + "_"
	if (not os.path.exists(input)):
		if (os.path.exists(rst_in)):
			os.system("ncdump " + rst_in + " > " + input)
		else:
			print("check input files")
			sys.exit()

	for counter in range(number_of_runs):
		c_string = str(counter+1).zfill(number_of_digits)
		local_filename = "4_{0}.rst".format(c_string)
		filename = os.path.join(checks_dir, local_filename)
		answer = ""
		if os.path.exists(filename):
			while (answer != "y") and (answer != "n"):
				answer = raw_input("Check file exists. Would you like to overwrite all check files? (y/n)\n")
			if answer == 'n':
				break
		
		with open(input, 'r') as textfile:
			lines = textfile.readlines()

		if modify == "velocity":
			velocity_string = str(-float(counter)/10 - 0.1)

			if len(lines) > velocity_line + 3:
				line1 = lines[velocity_line].split(',')
				line2 = lines[velocity_line + 1].split(',')
				line3 = lines[velocity_line + 2].split(',')
				line1[0] = velocity_string
				line2[0] = velocity_string
				line3[0] = velocity_string
				lines[velocity_line]     = string.join(line1,',')
				lines[velocity_line + 1] = string.join(line2,',')
				lines[velocity_line + 2] = string.join(line3,',')

			with open(output, 'w') as outfile:
				outfile.writelines(lines)
			
		if modify == "angle":
			velocity = 1.0
			velocity_x = str(velocity*math.cos((counter * math.pi)/(number_of_runs*2.0)))
			velocity_y = str(velocity*math.sin((counter * math.pi)/(number_of_runs*2.0)))
			
			if len(lines) > velocity_line + 3:
				line1 = lines[velocity_line].split(',')
				line2 = lines[velocity_line + 1].split(',')
				line3 = lines[velocity_line + 2].split(',')
				line1[0] = velocity_x
				line2[0] = velocity_x
				line3[0] = velocity_x
				line1[1] = velocity_y
				line2[1] = velocity_y
				line3[1] = velocity_y
				lines[velocity_line]     = string.join(line1,',')
				lines[velocity_line + 1] = string.join(line2,',')
				lines[velocity_line + 2] = string.join(line3,',')

			with open(output, 'w') as outfile:
				outfile.writelines(lines)

		os.system("ncgen -o " + rst_out_str + c_string + ".rst " + output)
		os.system("rm " + output)
	os.system("rm " + input)

def pbs_files_gen():
	for counter in range(number_of_runs):
		c_string = str(counter+1).zfill(number_of_digits)
		local_filename = "4_PRODUCTION-NVT_{0}.pbs".format(c_string)
		filename = os.path.join(pbs_dir, local_filename)
		input = ""
		if os.path.exists(filename):
			while (input != "y") and (input != "n"):
				input = raw_input("PBS file exists. Would you like to overwrite all PBS files? (y/n)\n")
			if input == 'n':
				break
		with open(filename, 'w') as outfile:
			# Beginning of each pbs script:
			outfile.write("""#!/bin/bash
#PBS -l nodes=1:ppn=8,walltime=48:00:00
#PBS -o logs/job.out
#PBS -e logs/job.err
NCPU=`wc -l < $PBS_NODEFILE`
NNODES=`uniq $PBS_NODEFILE | wc -l`
cd $PBS_O_WORKDIR

""")
			chk_in = os.path.join(checks_dir,'4_{0}.rst'.format(c_string))
			chk_out = os.path.join(checks_dir,'4_{0}.rst'.format(c_string))
			ptraj_out = os.path.join(trajectories_dir,'4_{0}.mdcrd'.format(c_string))
			md_out = os.path.join(trajectories_dir, '4_{0}.out'.format(c_string))

			outfile.write("mpirun -n ${{NCPU}} /opt/amber14/bin/sander.MPI -O -i md_inputs/4_production.in -o {md_out} -p md_inputs/water_so2.prmtop -c {chk_in} -r {chk_out} -x {ptraj}".format(md_out=md_out, chk_in=chk_in, chk_out=chk_out, ptraj=ptraj_out))

def makedir(name):
	if isinstance(name, str):
		if not os.path.exists(name):
			os.mkdir(name)
		else:
			print(name + " exists.")

def ptraj_multi_gen():
	ptraj_script = os.path.join(trajectories_dir, "trajectory_analysis.sh")
	if (os.path.exists(ptraj_script)):
		input = ""
		while (input != "y") and (input != "n"):
			input = raw_input("Ptraj script exists. Would you like to replace it? (y/n)\n")
		if input == 'n':
			return
	else:
		print("Ptraj script does not exist. Generating...")
	with open(ptraj_script, 'w') as outfile:
		for counter in range(number_of_runs):
			c_string = str(counter+1).zfill(number_of_digits)
			i_file = os.path.join("4_{0}.dat ".format(c_string))
			o_file = os.path.join("4_{0}.txt\n".format(c_string))
			outfile.write("cpptraj < ptrajin/closestwaters_{0}.ptrajin\n".format(c_string))
			outfile.write("python retention_closest.py " + i_file + o_file)
	os.system("chmod +x " + ptraj_script)

def ptrajin_gen():
	for counter in range(number_of_runs):
		c_string = str(counter+1).zfill(number_of_digits)
		local_filename = "closestwaters_{0}.ptrajin".format(c_string)
		filename = os.path.join(ptrajin_dir, local_filename)
		input = ""
		if os.path.exists(filename):
			while (input != "y") and (input != "n"):
				input = raw_input("A ptrajin file exists. Would you like to overwrite all ptrajin files? (y/n)\n")
			if input == 'n':
				break
		with open(filename, 'w') as outfile:
			outfile.write("parm ../md_inputs/water_so2.prmtop\ntrajin 4_{0}.mdcrd\n".format(c_string))
			outfile.write("closestwaters 4 :SO2 center closestout 4_{0}.dat\n".format(c_string))
			outfile.write("go\nquit\n")

def main():
	# MAKE DIRECTORIES
	for name in [checks_dir, trajectories_dir, pbs_dir, ptrajin_dir]:
		makedir(name)

	# QUEUE FILE
	print("\nQueue files...")
	queue_file_gen()

	# CHECKPOINT FILES
	print("\nCheck files...")
	check_files_gen()

	# PBS FILES
	print("\nPBS files...")
	pbs_files_gen()

	# PTRAJ MULTI SCRIPT
	print("\nPTRAJ MULTI SCRIPT...")
	ptraj_multi_gen()

	# PTRAJIN SCRIPTS
	print("\nPTRAJIN files...")
	ptrajin_gen()

if __name__ == "__main__":
	main()