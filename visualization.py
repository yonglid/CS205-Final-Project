import matplotlib.pyplot as plt 
import math 
import numpy as np 

#Constants
L = 3.0
N = 300 
BCL = 400.0 
sd = 20.0 
timestep = 10**(-2)
T_output = 60000

# Resolution variable 
# 100: very high res
# 400: high res
# 1600 low res/real time 
resolution = 600



def file_to_png(f): 

	print "Initializing..."

	T = int(T_output/timestep)
	frames = math.floor(T/resolution)
	#setting y and x limits of the current axes (ylim( (ymin, ymax) ))
	plt.ylim(0, 1)
	plt.xlim(0, L)
	plt.xlabel('res:' + str(resolution) + ', L: ' + str(L) + ', N: ' + str(N) + ', BCL: ' + str(BCL) + ', sd: ' + str(sd))
	# for testing, will need to change fulldatac.txt to fulldatac 
	# later try putting "f" in the function argument and change code to file = open("%s" % f, "r")
	file = open("%s" % f, "r")
	line = file.readline()
	for i, num in enumerate(line.split()): 
		print num 
	#intial time row 
	# m = 0
	# print "Loading frame:"
	# with open("%s" % f, "r") as f: 
	# 	for i, num in enumerate(line.split()): 
	# 		while m < T + 1: 
	# 		# m_float = map(float, line.split())
	# 			n = int(m/resolution)
	# 			plt.plot(i, num, 'bo')
	# 			plt.savefig('data_%d.png'%(n,))
	# 			print n,"/",int(frames)
			# data = line.split()

	# next, parse through file - split it up and insert - need a loop through the file and plot each thing and save as png 
	# plt.plot(ary1,V_old)
	# 	n = int(m/resolution)
	# 	plt.savefig('data_%d.png'%(n,))
	# 	plt.gcf().clear()
	# 	print n,"/",int(frames)

file_to_png("full_data") 