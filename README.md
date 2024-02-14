# water-nanoparticle-MD
This repo is the code for my thesis *"The Effects of Ions on the Adsorption of SO2 on a Water Nanoparticle."* This particular version contains documentation, and files necessary to reproduce results.
## Requirements
- Unix-based system to install the following programs on
- Amber14 (no longer supported but newer versions are [here](https://ambermd.org))
- [Packmol](https://github.com/m3g/packmol)
- Python 3.x
- Ability to use `qsub` to submit pbs scripts
## Reproduction
The following is a general list of steps to run the simulations. **Different branches of this repo contain different simulations,** each have minor diffs from this version. The main branch is the 376 water molecule simulation.

1. From root:
	`cd tleap`
	`packmol < solvateWater.inp`
	`tleap -f tleapScript-water.tls`

Packmol generates the initial configuration of water molecules and tleap adds the other molecules as applicable. The `.prmtop` files produced are stored in `md_inputs` along with the initial configurations.

2. Change back to the root directory and run `qsub [step].pbs` for each step given in numerical order (i.e. 0_min.pbs). You may also run the "RUN_ALL.pbs" script to run every step consecutively.

If you need to stop the simulation, run `qstat` to get the PID, then `qdel [PID]`. 

The simulation out files are stored in `md_outputs`. The trajectory coordinate files are stored in `ptraj`.  You will perform analysis on the production trajectory: `production.mdcrd`.

3. When the simulations have finished without error, run `python gen_trajin.py [# water molecules]` in the `ptraj` directory. This generates the file ptraj uses to calculate the dipoles for each water molecule.
	`cpptraj < extracdipoles.ptrajin`
	`python process.py [frames] [# water molecules]` 

The number of frames depends on both your simulation in-files and ptraj command. Specifically, the coordinates of the simulation are written out every `ntwx` frames. The `nstlim` parameter tells how many steps are in each simulation. In the ptraj command, you may specify to skip certain frames in the line `trajin production.mdcrd 1 last [step (optional)]`. Bottom line, the stdout of the cpptraj command includes the number of frames written to the COM.dat file.

You may want to run `reset.sh` to remove checkpoints, logs, etc.