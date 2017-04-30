**Table of Contents** 

- [CS205-Final-Project](#)
- [Advanced Features](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#advanced-features)
 -[Lattice-Boltzmann]


# CS205-Final-Project
<p style="font-family:Courier; color:Blue; font-size: 20px;">This text has the font Courier, is Blue, and 20px.</p>

Final Project
Current team: Peter Chang, Yong Li Dich, Alexander Wu, Anita Chandrahas 

Project research: The tunicate, commonly known as the sea squirt, exhibits the phenomenon of blood flow direction reversal. There are two main potential methods researched on how the tunicate carries out this nonpareil event: 1) two pacemakers with the same rates but with natural deviations 2) two pacemakers with different rates that change at every k where k is between 1 and infinity pumps. The math was initially coded out in python to generate a video simulation of the blood flow in order to observe the two possible etiologies for the blood flow reversal.

One major issue with the research was the length of simulation generation. For each 30 second video, about 45 minutes of computations were needed, which is much too long when multiple parameters are needed to be tested. For this project, in order to assist in more efficient and productive research to test out more hypotheses on this phenomenon, the team implemented various parallelisations in order to drastically speed up the simulations. The python code was coded into C code, writing data points of voltage in correlation with time into a file, which is taken in by a python program to create data plots for visualization/simulation. 

The main point was to allow for less time spent running the code and more time looking into reasons for the blood flow reversal, though the domain of blood flow simulation is also very interesting to explore (like the lattice boltzmann approach). 

Basic Physiological Equations

In order for a heart to pump blood, a pacemaker is required at the end of the heart fibers. This pacemaker creates electric jolts at a certain interval in order to send waves throughout the entire fiber. The heart of a sea squirt may be modeled as having two pacemakers, one at either end of the heart fiber (Krijgsman, Miller and Waldrop), which allows for blood to flow in both directions. A unique feature about wave mechanics within a heart fiber is that waves which collide do not pass through each other as most waves do. Rather, the nature of the mechanics causes the two waves to "collapse" upon collision. This allows only one of the directions to be dominant at any given moment.

Based on the Mitchell-Schaeffer model, there are two main components that govern the propagation of waves within the heart, the first is the processes of individual heart cells and the second is diffusion between adjacent heart cells. When dealing with individual heart cells, there are two differential equations that govern how electric potential is stored. The first is the primary equation for voltage (Cain and Schaeffer):

<a href="https://www.codecogs.com/eqnedit.php?latex=dv/dt&space;=&space;inward&space;current-&space;outward&space;current" target="_blank"><img src="https://latex.codecogs.com/gif.latex?dv/dt&space;=&space;inward&space;current-&space;outward&space;current" title="dv/dt = inward current- outward current" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex==\frac{h}{t_{in}}&space;v^2&space;(1-v)&space;-&space;\frac{v}{t_{out}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=\frac{h}{t_{in}}&space;v^2&space;(1-v)&space;-&space;\frac{v}{t_{out}}" title="=\frac{h}{t_{in}} v^2 (1-v) - \frac{v}{t_{out}}" /></a>

Where t_in and t_out are physiological constants, v is voltage inside the cell, and h is a constant between 0 and 1 that represents how open or closed the cell door which introduces voltage from outside the fiber. The variable h is governed by the piecewise ordinary differential equation:

<a href="https://www.codecogs.com/eqnedit.php?latex=dh/dt=&space;\begin{cases}&space;-h/t_{close}&space;&&space;\text{if&space;}&space;v>v_{crit}\&space;&&space;(1-h)/t_{open}&space;&&space;\text{if&space;}&space;v<v_{crit}&space;\end{cases}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?dh/dt=&space;\begin{cases}&space;-h/t_{close}&space;&&space;\text{if&space;}&space;v>v_{crit}\&space;&&space;(1-h)/t_{open}&space;&&space;\text{if&space;}&space;v<v_{crit}&space;\end{cases}" title="dh/dt= \begin{cases} -h/t_{close} & \text{if } v>v_{crit}\ & (1-h)/t_{open} & \text{if } v<v_{crit} \end{cases}" /></a>

Where t_open and t_close are once again physiological constants and v_crit is a certain voltage level that determines how the cell will behave.

The second important component is the diffusion between cells. The diffusion equation for voltage with respect to time is:

<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{du}{dt}&space;=&space;k&space;\frac{d^2u}{dx^2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{du}{dt}&space;=&space;k&space;\frac{d^2u}{dx^2}" title="\frac{du}{dt} = k \frac{d^2u}{dx^2}" /></a>

Where k is another physiological constant. Diffusion will be a factor of the cell itself, and the cells immediately adjacent to it.  We can estimate the change by diffusion using the standard Heat Equation:

<a href="https://www.codecogs.com/eqnedit.php?latex=K&space;(\frac{u_{k-1}^m&space;-&space;2u_{k}^m&space;&plus;&space;u_{k&plus;1}^m&space;}{(\Delta&space;x)^2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K&space;(\frac{u_{k-1}^m&space;-&space;2u_{k}^m&space;&plus;&space;u_{k&plus;1}^m&space;}{(\Delta&space;x)^2})" title="K (\frac{u_{k-1}^m - 2u_{k}^m + u_{k+1}^m }{(\Delta x)^2})" /></a>

Where K is the diffusion coefficient (.001 for most biological cases), and u is the voltage estimated voltage at time m and at location k. There are boundary conditions on the cells at the beginning and ends of the fiber. By assuming the conditions that no voltage passes through the ends, i.e. du/dx(0,t) = 0 and du/dx(L,t) = 0 these will have an increased effect from the single adjacent cell:

<a href="https://www.codecogs.com/eqnedit.php?latex=K&space;(\frac{2u_{1}^m&space;-&space;2u_{0}^m&space;}{(\Delta&space;x)^2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K&space;(\frac{2u_{1}^m&space;-&space;2u_{0}^m&space;}{(\Delta&space;x)^2})" title="K (\frac{2u_{1}^m - 2u_{0}^m }{(\Delta x)^2})" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=K&space;(\frac{-2u_{N}^m&space;&plus;&space;2u_{N-1}^m&space;}{(\Delta&space;x)^2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K&space;(\frac{-2u_{N}^m&space;&plus;&space;2u_{N-1}^m&space;}{(\Delta&space;x)^2})" title="K (\frac{-2u_{N}^m + 2u_{N-1}^m }{(\Delta x)^2})" /></a>

Where N is the number of cells within the heart fiber.

Methods Implemented in Research:

1) Controlled Shifting method: In this hypothesis, the two pacemakers at the ends of the heart fiber do not have the same rate of heart pumping. At the beginning, one pacemaker will begin with a slow rate and the other begins with a fast rate. After each pump, the slow pacemaker will increase speed by a small amount and the fast pacemaker will decrease its speed. Naturally, the side with the faster rate will dominate initially, however they will eventually trade dominance and the blood flow will change. Intuitively, this hypothesis will clearly generate blood flow reversals, however the main goal was to see if the simulations generated were realistic.

2) Random Variation method: In this method, the two pacemakers maintain the same average pacemaker rate but with some standard deviation between each pump. This hypothesis requires more testing in order to determine whether reversals can occur and with which parameters (such as diffusion rate, fiber length, number of cells, etc.) this model can be sustained, all while being biologically consistent. This parameter heavy model is the reason why parallelising this code is important. Multiple tests must be run with different constants in order to determine whether this model can prove to be sufficient.

Parallelization techniques: OpenACC, OpenACC P100 (SPMD), Prange, and OpenMP 

Base line blood flow simulation model: Hodgkin-Huxley 

Implemented blood flow simulation (with the least ODE's): Mitchell Schaffer 

Language: Current code in Python from Peter's research project - re-coding in C + transforming with Cython 

Benchmarking:

Since heart fibers range between 10 micrometers and 100 micrometers, we ran a few separate cases for benchmarking. L=3.0cm is a biologically reasonable fiber length for a tunicate. Consequently, an N of 300 will give a 100 micrometer fiber cell, N=600 gives a 50 micrometer fiber cell, and N=3000 gives a 10 micrometer fiber cell. Using the larger values of N will allow the code to experience greater speedup.

(Step = 10^-2, L=3.0cm, N=300) 

Python Serial 

10ms, res=10: time=1.06  
100ms, res=10: time=6.02  
100ms, res=100: time=5.76  
1000ms, res=600: time=52.2  
10000ms, res=600: time=527.0  (GFlop/s: .016)
30000ms, res=600: time=1753.3  (GFlop/s: .0144)

Cython Parallel

Cython Implementation (Step = 10^-2, L=3.0, N=300)

10000ms, res=600: time=463.6690833568573 (GFlop/s: 0.018)
30000ms, res=600: time=1553.7774078845978 (GFlop/s: 0.016)
60000ms, res=600: time=3242.5310328006744 (GFlop/s: 0.016))

C Implementation: (Step = 10^-2, L=3.0, N=300)  

30000ms, res=600, time=125.010000 (GFlop/s: 0.203)  
60000ms, res=600, time=307.410000 (GFlop/s: 0.165)  
150000ms, res=600, time=856.340000 (GFlop/s: 0.148)  
500000ms, res=600, time=2986.510000 (GFlop/s: 0.142)  

OpenACC 

30000ms, res=600, time=61.090000 (GFlop/s: 0.415)  
60000ms, res=600, time=123.010000 (GFlop/s: 0.412)  
150000ms, res=600, time=308.050000 (GFlop/s: 0.412)  
500000ms, res=600, time=1029.380000 (GFlop/s: 0.411)  

OpenACC (NVIDIA Tesla P100): (Step = 10^-2, L=3.0, N= 300)

30000ms, res=600, time=55.990000 (GFlop/s: 0.453)  
60000ms, res=600, time=103.770000 (GFlop/s: 0.489)
150000ms, res=600, time=271.700000 (GFlop/s: 0.467)
500000ms, res=600, time=903.990000, (GFlop/s: 0.467)

![alt tag](https://github.com/yonglid/CS205-Final-Project/blob/master/c_speedup.png)

(Step = 10^-2, L=3.0cm, N=600)

Python Serial 

10ms, res=10: time=1.02  
100ms, res=10: time=10.04  
100ms, res=100: time=8.28 
1000ms, res=600: time=87.96  
10000ms, res=600: time=784.6  (GFlop/s: .0215)
30000ms, res=600: time=2480.43  (GFlop/s: .0203)

# Advanced Features

###Modeling: The Lattice Boltzmann Model (LBM)

To model blood flow, one might typically think about using the Navier-stokes equation for fluid dynamics simulations. However, blood is a a multiphase non-Newtonian viscoelastic fluid. These properties essentially mean the continuum approximations of Navier-stokes do not hold for modeling blood flow.

Overall, there are a few advantages of using LBM to model blood flow. 

1)	It can be used to simulate multiphase flow
2)	It can more readily include complex boundary conditions
3)	It can easily be parallelized. 

Boltzmann’s theory of kinetic gasses essentially says that gasses or fluids can be regarded as small particles with random motions. This idea is simplified by the Lattice-Boltzmann method is a simplification of Boltzmann’s original idea by restricting the number of particles and confining the velocity vectors to the nodes of a lattice. Thus, LBM is an ideal balance between microscopic (bottom-up) and macroscopic (top-down) molecular dynamic simulations.

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM1.png)
**Lattice-Boltzman uses discrete particles on a lattice which can be summed to create a simplified 2D Navier-stokes model.

We focus on the two-dimensional blood flow simulation by using LBM to model Navier stokes.

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM2.png)
*Lattice scheme to model Navier-Stokes.*

The basic process of Lattice-Boltzmann is illustrated below:

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM3.png)
*Each point on the lattice has particles with discrete velocities.*

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM4.png)
*Transport phase: shift of data along each independent velocity vector.*

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM5.png)
*Relaxation phase: Determines the microscopic dynamics towards local equilibrium and macroscopic transport coefficients (tune to get desired dynamics)*


![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM6.png)
*Repeat transport and relaxation*


Citations

B. J. Krijgsman, Biological Reviews, 31, 288, 1956

C. C. Mitchell, D. G. Schaeffer, Bulletin of Mathematical Biology, 65, 767, 2003

L. D. Waldrop and L. Miller, Journal of Experimental Biology, 218, 2753, 2015

J. W. Cain, D. G. Schaeffer, SIAM Review 48, 537, 2006

J. W. Cain, E. G. Tolacheva, D. G. Shaeffer, and D. J. Gauthier, Physical Review E70, 061906, 2004

M. E. Kriebel, Journal of General Physiology, 50, 2097, 1967

M. E. Kriebel, Biological Bulletin, 134, 434, 1968

C. H. Luo and Y. Rudy, Circulation Research 74, 1071, 1994
