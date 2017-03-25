#used to create stochastic-BCL.mp4

import math
import numpy as np
import matplotlib.pyplot as plt
import time

#Constants
timestep = 10**(-2)
L = 3.0
N = 300
spacestep = L/float(N)
v_crit = .13
t_in = .1
t_out = 2.4
t_open = 130.0
t_close = 150.0
K = .001
BCL = 400.0
sd = 20.0

#Resolution variable
#100: very high res      400: high res (75 minutes)
#1600: low res/real time (50 minutes)
resolution = 600

#Gate condition
def g(v,h):
    if v <= v_crit:
        return (1 - h)/t_open
    else:
        return (-h)/t_close

#Single cell voltage condition
def f(v,h):
    return h*(v**2)*(1-v)/t_in - (v/t_out)

#initial values  
def v_init(x):
    if x <= 4*spacestep:
        return .8
    elif x >= L-4*spacestep:
        return .8
    else:
        return 0
        
def h_init(x):
    return 1

#returns h^(m+1)
def update_h(v,h):
    return g(v,h)*timestep + h

#returns v^(m+1) at spot k on middle parts given time m and spot k
def stdupdate_v(k,V,H):
    return (((V[k+1] - 2*V[k] + V[k-1])*(K/(spacestep**2))) + f(V[k],H[k]))* timestep + V[k]
    
def lupdate_v(k,V,H):
    return (((2*V[1] - 2*V[0])*(K/(spacestep**2))) + f(V[0],H[0]))* timestep + V[0]
    
def rupdate_v(k,V,H):
    return (((2*V[N-1] - 2*V[N])*(K/(spacestep**2))) + f(V[N],H[N]))* timestep + V[N]
    
#generate random fluctuations
def rand():
    return int(np.random.normal(BCL,sd))

def main(T_output):
    
    print "Initializing..."
    
    L_var = rand()
    R_var = rand()
    
    T = int(T_output/timestep)

    frames = math.floor(T/resolution)

    if (K*timestep)/(spacestep**2) > .5:
        print "CFL condition not met"
        return 0
    
    #initial time row
    m = 0
    
    #data array
    #stores voltage, v, at each location, x, in an array
    #stores one array per timestamp
    width = N+1
    height = int(T_output + 2)
    #V = [[0 for x in range(width)] for y in range(height)]
    
    V_old = [0 for x in range(width)]
    V_new = [0 for x in range(width)]
    
    #for storing the spots to be printed
    V = [[0 for x in range(width)]for y in range(height)]
    
    #array for gate function
    #H = [[0 for x in range(width)] for y in range(height)]
    
    H_old = [0 for x in range(width)]
    H_new = [0 for x in range(width)]
    
    #fill in the first array with the initial voltage
    #do once each for N cells
    for i in range(0,N+1):
        x = i*spacestep
        #V[0][i] = v_init(x)
        V_old[i] = v_init(x)
    
    V_new = V_old
    
    ary1 = []
    for i in range(0,N+1):
        ary1.append(i*spacestep)
    
    #Initialize H values
    for i in range(0,N+1):
        #H[0][i] = 1
        H_old[i] = 1
    
    print "Loading frame:"
    
    while m < T+1:
        plt.ylim(0,1)
        plt.xlim(0,L)
        plt.xlabel('res:' + str(resolution) + ', L: ' + str(L) + ', N: ' + str(N) + ', BCL: ' + str(BCL) + ', sd: ' + str(sd))
        if m % resolution == 0:
            plt.plot(ary1,V_old)
            n = int(m/resolution)
            plt.savefig('data_%d.png'%(n,))
            plt.gcf().clear()
            print n,"/",int(frames)
            
        #fill in interior grid points
        for k in range(1,N):
            V_new[k] = stdupdate_v(k,V_old,H_old)
            
        #fill in left boundary
        V_new[0] = lupdate_v(k,V_old,H_old)
        #fill in right boundary
        V_new[N] = rupdate_v(k,V_old,H_old)
        
        for k in range(0,N+1):    
            H_new[k] = update_h(V_old[k],H_old[k])
            
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
     
    """#storing data at time T into a text file
    f = open("full_data_100ms",'w')
    for i, array in enumerate(V[T]):
        s = str(ary1[i]) + ' ' + str(V[T][i]) + '\n'
        f.write(s)
    f.close()"""
    
    """plt.ylim(0,1)
    plt.xlim(0,10)
    plt.plot(ary1,V[T_output])
    plt.show()"""

start = time.time()
#output at T = 100 ms
main(60000)
print "Time: ", time.time()-start