#Output is "full_data" containing voltages at time intervals.

import cython
import math
import numpy as np
cimport numpy as np
import matplotlib.pyplot as plt
import time
from cython.parallel import prange, parallel 
from cython import boundscheck

#Constants
cdef double timestep = 0.01         #How many computations per ms of data
cdef double L = 3.0                     #Length of the heart fiber in cm
cdef int N = 300                     #Number of "cells" in the fiber
cdef double spacestep = L/float(N)      #cm size per array
cdef double v_crit = .13                #Coefficient for voltage model
cdef double t_in = .1                   #Coefficient for cell gate model
cdef double t_out = 2.4                 #""
cdef double t_open = 130.0              #""
cdef double t_close = 150.0             #""
cdef double K = .001                    #Coefficient for numerical stability
cdef double BCL = 400.0                 #Mean of heart rate
cdef double sd = 20.0                   #SD of heart rate

#Resolution variable
#Determines how often to produce plot of voltage
#Recommend around 600, can be varied dependent on size of computation
cdef double resolution = 10

#Gate condition
cdef g(double v, double h):
    if v <= v_crit:
        return (1 - h)/t_open
    else:
        return (-h)/t_close


#Single cell voltage condition
def f(double v, double h):
    return h*(v**2)*(1-v)/t_in - (v/t_out)

#Creates a heart "pump" by charging first few cells  
def v_init(double x):
    if x <= 4*spacestep:
        return .8
    elif x >= L-4*spacestep:
        return .8
    else:
        return 0

#initial condition for cell gates       
def h_init(double x):
    return 1

#returns gate constant, h, at time m+1
@boundscheck(False)
def update_h(double[:] V,double[:] H,int n):
    cdef double[:] out = np.array([0]*n,dtype=np.float)
    cdef int k
    cdef double val
    for k in prange(0,n,schedule='dynamic',nogil=True,num_threads=4):
        if V[k] <= v_crit:
            val = (1 - H[k])/t_open
        else:
            val = (-H[k])/t_close
        out[k] = val*timestep + H[k]
    return out

#returns voltage at spot k, time m_1, for middle heart cells
#must be given time m and location k
@boundscheck(False)
def stdupdate_v(double[:] V,double[:] H,int n):
    cdef double[:] out = np.array([0]*n,dtype=np.float)
    cdef int k
    cdef double val
    for k in prange(1,n+1,schedule ='dynamic',nogil=True,num_threads=4):
        val = H[k]*(V[k]**2)*(1-V[k])/t_in - (V[k]/t_out)
        out[k-1] = (((V[k+1] - 2*V[k] + V[k-1])*(K/(spacestep**2))) + val)*timestep + V[k]
    return out

#boundary conditions    
def lupdate_v(np.ndarray[double, ndim=1] V,np.ndarray[double, ndim=1] H):
    return (((2*V[1] - 2*V[0])*(K/(spacestep**2))) + f(V[0],H[0]))* timestep + V[0]
    
def rupdate_v(np.ndarray[double, ndim=1] V,np.ndarray[double, ndim=1] H):
    return (((2*V[N-1] - 2*V[N])*(K/(spacestep**2))) + f(V[N],H[N]))* timestep + V[N]
    
#generates next time of heart pump with some natural variance
def rand():
    return int(np.random.normal(BCL,sd))

width = N+1
V_old = np.array([0 for x in range(width)],dtype=np.float)
V_new = np.array([0 for x in range(width)],dtype=np.float)
    
#data arrays for gate function
cdef double[:] H_old = np.array([0 for x in range(width)],dtype=np.float)
cdef double[:] H_new = np.array([0 for x in range(width)],dtype=np.float)

def main(double T_output):   
    print "Initializing..."
    
    L_var = rand()                      #determines next pacemaker pulse time
    R_var = rand()

    cdef int T = int(T_output/timestep)          #number of ms to compute divided by granularity
    
    cdef int frames = math.floor(T/resolution)   #number of plots to be created

    #Conditions must satisfy this for numerical stability
    if (K*timestep)/(spacestep**2) > .5:
        print "CFL condition not met"
        return 0
    
    #data arrays for voltage
    cdef int width = N+1

    cdef np.ndarray[double, ndim=1] V_old = np.array([0 for x in range(width)],dtype=np.float)
    cdef np.ndarray[double, ndim=1] V_new = np.array([0 for x in range(width)],dtype=np.float)
    
    #data arrays for gate function
    cdef np.ndarray[double, ndim=1] H_old = np.array([0 for x in range(width)],dtype=np.float)
    cdef np.ndarray[double, ndim=1] H_new = np.array([0 for x in range(width)],dtype=np.float)
    
    #fill in the first array with the initial voltage
    #do once each for N cells
    for i in range(0,N+1):
        x = i*spacestep
        V_old[i] = v_init(x)
    
    V_new = V_old
    
    #cdef double 
    ary1 = np.array([])
    for i in range(0,N+1):
        ary1 = i*spacestep
    
    #Initialize H values
    for i in range(0,N+1):
        H_old[i] = 1
    
    print "Loading frame:"

    cdef int m = 0
    while m < T+1:
        #occasionally append voltage data in txt file
        if m % resolution == 0:
            # plt.plot(ary1,V_old)
            f = open("full_data","a")
            for i, array in enumerate(V_old):
                s = str(V_old[i]) + ' '
                f.write(s)
            f.write('\n')
            n = int(m/resolution)
            # plt.savefig('data_%d.png'%(n,))
            # plt.gcf().clear()

            print n,"/",int(frames)

        #prange here 
        #fill in interior grid points
        V_new[1:width-1] = stdupdate_v(V_old,H_old,width-2)
        
        #fill in left boundary
        V_new[0] = lupdate_v(V_old,H_old)
        #fill in right boundary
        V_new[N] = rupdate_v(V_old,H_old)
                
        #prange here 
        #update door constants
        H_new[0:width] = update_h(V_old,H_old,width)
                
        #if time for a new pump, add voltage   
        if int((m+1)*timestep) == L_var:
            for i in range(0,5):
                V_new[i] = .8
            L_var = rand()+L_var
        
        if int((m+1)*timestep) == R_var:
            for i in range(N-4,N+1):
                V_new[i] = .8
            R_var = rand()+R_var

        V_old = V_new
        H_old = H_new 
        
        m += 1