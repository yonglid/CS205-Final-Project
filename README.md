# CS205-Final-Project
Final Project
Current team: Peter Chang, Yong Li Dich, Alexander Wu, Anita Chandrahas 

Project research: The tunicate, or commonly known as the sea squirt, exhibit the phenomenon of blood flow direction reversal. There are two main potential methods researched on how the tunicate carries out this nonpareil event: 1) two pacemakers with the same rates but with variation 2) two pacemakers with different rates that change at every k where k is between 1 and infinity pumps. The math was initially coded out in python to generate a video simulation of the blood flow in order to observe the two possible etiologies for the blood flow reversal.

For this project, in order to assist in more efficient and productive research to test out more hypotheses on this phenomenon, the team attempted to parallelize the python code. The python code was coded into C code, writing data points of voltage in correlation with time into a file, which is taken in by a python program to create data plots for visualization/simulation. 

The main point was to allow for less time spent running the code and more time looking into reasons for the blood flow reversal, though the domain of blood flow simulation is also very interesting to explore (like the lattice boltzmann approach). 

Methods tried: random variation method and a controlled shifting method

Parallelization techniques: OpenACC, Prange, and OpenMP 

Base line blood flow simulation model: Hodgkin-Huxley 

Implemented blood flow simulation (with the least ODE's): Mitchell Schaffer 

Language: Current code in Python from Peter's research project - re-coding in C + transforming with Cython 

Benchmarking:  

Step = 10^-2, L=3.0, N=300  

10ms, res=10: time=1.06  

100ms, res=10: time=6.02  

100ms, res=100: time=5.76  

1000ms, res=600: time=52.2  

10000ms, res=600: time=527.0  (GFlop/s: .016)

30000ms, res=600: time=1753.3  (GFlop/s: .0144)


C Implementation: (Step = 10^-2, L=3.0, N=300)  

30000ms, res=600, time=125.010000 (GFlop/s: 0.203)  
60000ms, res=600, time=307.410000 (GFlop/s: 0.165)  
150000ms, res=600, time=856.340000 (GFlop/s: 0.148)  
500000ms, res=600, time=2986.510000 (GFlop/s: 0.142)  

OpenACC: (Step = 10^-2, L=3.0, N=300)  

30000ms, res=600, time=61.090000 (GFlop/s: 0.415)  
60000ms, res=600, time=123.010000 (GFlop/s: 0.412)  
150000ms, res=600, time=308.050000 (GFlop/s: 0.412)  
500000ms, res=600, time=1029.380000 (GFlop/s: 0.411)  

![alt tag](https://github.com/yonglid/CS205-Final-Project/blob/master/c_speedup.png)
