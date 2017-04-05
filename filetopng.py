import matplotlib.pyplot as plt 
import math 
import numpy as np 

#Constants
L = 3.0
N = 300 
BCL = 400.0 
sd = 20.0 

# Resolution variable 
# 100: very high res
# 400: high res
# 1600 low res/real time 
resolution = 600

def file_to_png(file): 

	#setting y and x limits of the current axes (ylim( (ymin, ymax) ))
	plt.ylim(0, 1)
	plt.xlim(0, L)
	plt.xlabel('res:' + str(resolution) + ', L: ' + str(L) + ', N: ' + str(N) + ', BCL: ' + str(BCL) + ', sd: ' + str(sd))
	plt.plot(ary1,V_old)
		n = int(m/resolution)
		plt.savefig('data_%d.png'%(n,))
		plt.gcf().clear()
		print n,"/",int(frames)