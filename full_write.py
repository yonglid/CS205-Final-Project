#Output is "full_data" containing voltages at time intervals.

import math
import numpy as np
import matplotlib.pyplot as plt
import time

#Constants
timestep = 10**(-2)         #How many computations per ms of data
L = 3.0                     #Length of the heart fiber in cm
N = 300                     #Number of "cells" in the fiber
spacestep = L/float(N)      #cm size per array
v_crit = .13                #Coefficient for voltage model
t_in = .1                   #Coefficient for cell gate model
t_out = 2.4                 #""
t_open = 130.0              #""
t_close = 150.0             #""
K = .001                    #Coefficient for numerical stability
BCL = 400.0                 #Mean of heart rate
sd = 20.0                   #SD of heart rate

#Resolution variable
#Determines how often to produce plot of voltage
#Recommend around 600, can be varied dependent on size of computation
resolution = 10

#Gate condition
def g(v,h):
    if v <= v_crit:
        return (1 - h)/t_open
    else:
        return (-h)/t_close

#Single cell voltage condition
def f(v,h):
    return h*(v**2)*(1-v)/t_in - (v/t_out)

#Creates a heart "pump" by charging first few cells  
def v_init(x):
    if x <= 4*spacestep:
        return .8
    elif x >= L-4*spacestep:
        return .8
    else:
        return 0

#initial condition for cell gates       
def h_init(x):
    return 1

#returns gate constant, h, at time m+1
def update_h(v,h):
    return g(v,h)*timestep + h

#returns voltage at spot k, time m_1, for middle heart cells
#must be given time m and location k
def stdupdate_v(k,V,H):
    return (((V[k+1] - 2*V[k] + V[k-1])*(K/(spacestep**2))) + f(V[k],H[k]))* timestep + V[k]

#boundary conditions    
def lupdate_v(k,V,H):
    return (((2*V[1] - 2*V[0])*(K/(spacestep**2))) + f(V[0],H[0]))* timestep + V[0]
    
def rupdate_v(k,V,H):
    return (((2*V[N-1] - 2*V[N])*(K/(spacestep**2))) + f(V[N],H[N]))* timestep + V[N]
    
#generates next time of heart pump with some natural variance
def rand():
    return int(np.random.normal(BCL,sd))


def main(T_output):   
    print "Initializing..."
    
    L_var = rand()                      #determines next pacemaker pulse time
    R_var = rand()

    T = int(T_output/timestep)          #number of ms to compute divided by granularity

    frames = math.floor(T/resolution)   #number of plots to be created

    #Conditions must satisfy this for numerical stability
    if (K*timestep)/(spacestep**2) > .5:
        print "CFL condition not met"
        return 0
    
    #data arrays for voltage
    width = N+1
    
    V_old = [0 for x in range(width)]
    V_new = [0 for x in range(width)]
    
    #data arrays for gate function
    H_old = [0 for x in range(width)]
    H_new = [0 for x in range(width)]
    
    #fill in the first array with the initial voltage
    #do once each for N cells
    for i in range(0,N+1):
        x = i*spacestep
        V_old[i] = v_init(x)
    
    V_new = V_old
    
    ary1 = []
    for i in range(0,N+1):
        ary1.append(i*spacestep)
    
    #Initialize H values
    for i in range(0,N+1):
        H_old[i] = 1
    
    print "Loading frame:"

    m = 0
    
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
            
        #fill in interior grid points
        for k in range(1,N):
            V_new[k] = stdupdate_v(k,V_old,H_old)
            
        #fill in left boundary
        V_new[0] = lupdate_v(k,V_old,H_old)
        #fill in right boundary
        V_new[N] = rupdate_v(k,V_old,H_old)
        
        #update door constants
        for k in range(0,N+1):    
            H_new[k] = update_h(V_old[k],H_old[k])
         
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

start = time.time()
#Value in main is number of milliseconds to compute
main(10)        #using 60000 gives 1 minute of simulation
print "Time: ", time.time()-start