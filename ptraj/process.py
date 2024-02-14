import numpy as np
import string
import sys
import os

def getCOM(comfile):
	arr = np.loadtxt(comfile, delimiter="  ", dtype=str, skiprows=1)
	arr = np.delete(arr,[0,4,5,6],1)
	arr = arr.astype(np.float)
	return arr

def getdipole(dpfile):
	arr = np.loadtxt(dpfile, delimiter="  ", dtype=str, skiprows=1)
	arr = np.delete(arr,[0],1)
	arr = arr.astype(np.float)
	arr = np.split(arr, 2, 1)
	arr = np.swapaxes(arr, 0, 1)
	return arr

def gen_catarr(frames, molecules):
	com = getCOM('COM.dat') #center of mass

	data = np.zeros((molecules,frames,2,3))
	for molecule in range(molecules):
		data[molecule] = getdipole('dipoles/dipole{0}.dat'.format(str(molecule)))
	data = np.swapaxes(data, 0, 1) #shape: (frames,molecules,2,3)

	#subtract center of mass of the aerosol from each pos of water to get relative pos
	comsubarr = np.repeat(com,molecules,0)
	comsubarr = np.split(comsubarr, frames, 0)
	comsubarr = np.insert(comsubarr, [0, 0, 0], 0, 2)
	comsubarr = np.reshape(comsubarr, (frames, molecules, 2, 3))
	data = np.subtract(data, comsubarr)
	
	#normalizing constants for each molecule for each frame. shape: (frames, molecules)
	normc = np.prod(np.sqrt(np.sum(np.multiply(data,data),3)),2)
	#raw dot product for each molecule for each frame. shape: (frames, molecules)
	dotp = np.sum(np.prod(data,2),2)
	#cos(theta)
	cost = np.divide(dotp,normc)
	
	positions = np.delete(data,0,2) #shape: (frames, molecules, 1, 3)
	distances = np.sqrt(np.sum(np.multiply(positions,positions),3)) #shape: (frames, molecules)
	return np.concatenate((distances, np.resize(cost,(frames,molecules,1))),2)

def main():
	frames = None
	molecules = None

	if (len(sys.argv)<3):
		catarr = np.load('dist+cost.pkl')
	else:
		frames = int(sys.argv[1])
		molecules = int(sys.argv[2])
		catarr = gen_catarr(frames, molecules)
		catarr.dump('dist+cost.pkl')

	bins = 30
	maxd = 17.0
	interval = maxd/bins
	lines = [[i*interval,0] for i in range(bins)]
	for frame in catarr:
		for molecule in range(molecules):
			bin = min(bins - 1, int(frame[molecule][0] // interval))
			lines[bin][1] += frame[molecule][1]
	volume = [0 for i in range(bins + 1)]
	for bin in range(bins):
		volume[bin + 1] = 4.188790205*pow(((bin + 1.0)*interval),3)
		#lines[bin][1] /= (volume[bin+1] - volume[bin])
		lines[bin][1] /= frames
	with open('output.csv', 'w') as outfile:
		for line in lines:
			outfile.write(str(line[0]) + ', ' + str(line[1]) +'\n')


if __name__ == "__main__":
	main()
