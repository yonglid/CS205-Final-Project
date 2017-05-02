**Table of Contents** 

- [CS205-Final-Project](#)
- [Introduction](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#introduction)
  * [Background: Basic Physiological Equations](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#background-basic-physiological-equations)
  * [Potential Hypotheses for Blood Flow Reversal](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#potential-hypotheses-for-blood-flow-reversal)
  * [Problem to tackle](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#problem-to-tackle)
- [Technical description of parallel software solution](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#technical-description-of-parallel-software-solution)
- [Appliciable scaling plots (benchmarking)](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#appliciable-scaling-plots-benchmarking)
- [Advanced Features](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#advanced-features)
  * [p100](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#p100)
  * [Lattice-Boltzmann](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#modeling-the-lattice-boltzmann-model-lbm)


# CS205-Final-Project

Final Project
Current team: Peter Chang, Yong Li Dich, Alexander Wu, Anita Chandrahas 

# Introduction

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/ppt1.png)

The tunicate, commonly known as the sea squirt, exhibits the phenomenon of blood flow direction reversal. There are two main potential methods researched on how the tunicate carries out this nonpareil event: 1) two pacemakers with the same rates but with natural deviations 2) two pacemakers with different rates that change at every k where k is between 1 and infinity pumps. The math was initially coded out in python to generate a video simulation of the blood flow in order to observe the two possible etiologies for the blood flow reversal.

One major issue with the research was the length of simulation generation. For each 30 second video, about 45 minutes of computations were needed, which is much too long when multiple parameters are needed to be tested. For this project, in order to assist in more efficient and productive research to test out more hypotheses on this phenomenon, the team implemented various parallelisations in order to drastically speed up the simulations. The python code was coded into C code, writing data points of voltage in correlation with time into a file, which is taken in by a python program to create data plots for visualization/simulation. 

The main point was to allow for less time spent running the code and more time looking into reasons for the blood flow reversal, though the domain of blood flow simulation is also very interesting to explore (like the lattice boltzmann approach). 

* computational/baseline sequential algorithm
The time complexity of modelling the reversal as in models,  is mainly dependent on the resolution of the model. For high fidelity simulation we need to increase the problem size N , to simulate 300000 ms .
We reduce the complexity by parallelising in two models:

##SIMT parallelization 

Many-core througput oriented GPU architectures:  Here we program first in SIMT for a GPU on Odyssey that gives us the first level of throughput improvement as shown in figure ...

##SIMT parallelization P100 many-core
We further increase the througput by programming in SIMT but for a higher throughput P100 GPU architectures. This enables us to perform more simulations....

##Hybrid SPMD parallelization
openacc + MPI (bcast) 

* put thoroughplot with parallelization 
* time complexity 
* bcast for mpi 
# Background: Basic Physiological Equations

In order for a heart to pump blood, a pacemaker is required at the end of the heart fibers. This pacemaker creates electric jolts at a certain interval in order to send waves throughout the entire fiber. The heart of a sea squirt may be modeled as having two pacemakers, one at either end of the heart fiber (Krijgsman, Miller and Waldrop), which allows for blood to flow in both directions. A unique feature about wave mechanics within a heart fiber is that waves which collide do not pass through each other as most waves do. Rather, the nature of the mechanics causes the two waves to "collapse" upon collision. This allows only one of the directions to be dominant at any given moment.


![test](https://github.com/yonglid/CS205-Final-Project/blob/master/ppt2.png)

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

### Potential Hypotheses for Blood Flow Reversal

1) Controlled Shifting method: In this hypothesis, the two pacemakers at the ends of the heart fiber do not have the same rate of heart pumping. At the beginning, one pacemaker will begin with a slow rate and the other begins with a fast rate. After each pump, the slow pacemaker will increase speed by a small amount and the fast pacemaker will decrease its speed. Naturally, the side with the faster rate will dominate initially, however they will eventually trade dominance and the blood flow will change. Intuitively, this hypothesis will clearly generate blood flow reversals, however the main goal was to see if the simulations generated were realistic.

2) Random Variation method: In this method, the two pacemakers maintain the same average pacemaker rate but with some standard deviation between each pump. This hypothesis requires more testing in order to determine whether reversals can occur and with which parameters (such as diffusion rate, fiber length, number of cells, etc.) this model can be sustained, all while being biologically consistent. This parameter heavy model is the reason why parallelising this code is important. Multiple tests must be run with different constants in order to determine whether this model can prove to be sufficient.

### Problem to tackle

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/ppt3.png)

# Technical description of parallel software solution

Parallelize the code 
- SIMT parallelization - (manycore throughput) - single instruction, multiple thread 
 - Python -> Cython -> Prange
 - Python -> C -> OpenACC (compiler: pgi) 
  - Future fix/tests: Need smaller time step for more accuracy - we can now do this with parallelized version (took too long before) 
  - Added directives 

Separated calculation of voltage points and creation of plots for simulation 

 - Code for calculation is parallelized and points written into a file 
 - Separate visualization python code takes voltage points file in as input 



Parallelization techniques: OpenACC, OpenACC P100 (SPMD), Prange, and OpenMP 

Base line blood flow simulation model: OpenMP+MPI

Implemented blood flow simulation (with the least ODE's): Mitchell Schaffer 

Language: Current code in Python from Peter's research project - re-coding in C + transforming with Cython 

# Application scaling plots (benchmarking):

Since heart fibers range between 10 micrometers and 100 micrometers, we ran a few separate cases for benchmarking. L=3.0cm is a biologically reasonable fiber length for a tunicate. Consequently, an N of 300 will give a 100 micrometer fiber cell, N=600 gives a 50 micrometer fiber cell, and N=3000 gives a 10 micrometer fiber cell.

### (Step = 10^-2, L=3.0cm, N=300) 

#### Python Serial 


| Python Serial ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 10  | 10 | 1.06 || 
| 100 | 10 | 6.02 ||
| 100 | 100 | 5.76 ||
| 1000 | 600 | 52.2 ||
| 10000 | 600 | 527.0 |.016|
| 30000 | 600 | 1753.3 | .0144|

#### Cython

| Cython ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 10000 | 600 | 463.6690833568573 |0.018|
| 30000 | 600 | 1553.7774078845978 |0.016|
| 60000 | 600 | 3242.5310328006744 | 0.016|

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/python_cython_throughput.png" width="512">
<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/python_speedup.png" width="512">

We can see that overall, the Python implementation has very poor performance and the Cython parallelisation does very little to actually improve the throughput. 

#### C Implementation

| C ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 125.010000 |0.203|
| 60000 | 600 | 307.410000 | 0.165|
| 150000 | 600 | 856.340000 | 0.148|
| 500000 | 600 | 2986.510000 | 0.142|

#### OpenACC

| OpenACC ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 61.090000 |0.415|
| 60000 | 600 | 123.010000 | 0.412|
| 150000 | 600 | 308.050000 | 0.412|
| 500000 | 600 | 1029.380000 | 0.411|

#### OpenACC + MPI

60000ms, res=600, time= (GFlop/s: )


#### OpenACC (NVIDIA Tesla P100):

| OpenACC (NVIDIA Tesla P100) ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 55.990000 |0.453|
| 60000 | 600 | 103.770000  | 0.489|
| 150000 | 600 | 271.700000 | 0.467|
| 500000 | 600 | 903.990000 | 0.467|


<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/c_throughput.png" width="512">

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/c_speedup2.png" width="800">

We can see that the C implementation already provides much faster simulation generation than the Python code does. Additionally, the parallelisation of the code produced much better speedups that the parallelisation of the Python code. Using OpenACC, OpenACC + MPI, and then OpenACC on the NVIDIA Tesla P100, our throughput drastically increased and the computation time was at worst, halved.

In order to better show the effects of the parallelisation, we doubled the value N, which would increase the computation in the areas that we had parallelised. An N of 600 works well and maintains good biological accuracy with the hearts cells now being 50 micrometers in length. We did not increase the N any more than this due to the necessity of numerical stability. If .001(cellsize)/(timestep^2) > 1/2, then the numerical approximations that we use will diverge in value and not provide accurate simulations. Using a value of N which is larger than 600 would necessitate a smaller timestep, which would drastically increase computation time and slow down the code more than the parallelisation would speed it up.

### (Step = 10^-2, L=3.0cm, N=600)

#### Python Serial 

| Python Serial  ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 10  | 10 | 1.02 || 
| 100 | 10 | 10.04 ||
| 100 | 100 | 8.28 ||
| 1000 | 600 | 87.96  ||
| 10000 | 600 | 784.6  |.0215|
| 30000 | 600 | 2480.43 | .0203|


#### Cython Implementation


#### C Implementation

| C ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 501.390000 |0.101|
| 60000 | 600 | 999.530000 | 0.101|
| 150000 | 600 | 2532.830000 | 0.100|
| 500000 | 600 | 84072.320000 | 0.100|

#### OpenACC:
| OpenACC ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 118.470000 |0.427|
| 60000 | 600 | 238.150000 | 0.425|
| 150000 | 600 | 599.230000 | 0.422|
| 500000 | 600 | 1989.600000 | 0.424|

#### OpenACC + MPI:

| OpenACC + MPI ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | ||
| 60000 | 600 | | |
| 150000 | 600 | 1264.720000 | |
| 500000 | 600 | 4233.650000 | |



#### OpenACC (NVIDIA Tesla P100):

| OpenACC (NVIDIA Tesla P100) ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 99.860000 |0.506|
| 60000 | 600 | 200.110000  | 0.505|
| 150000 | 600 |501.820000| 0.504|
| 500000 | 600 | 1662.240000 | 0.507|

# Advanced Features
### p100
### Modeling: The Lattice Boltzmann Model (LBM)

To model blood flow, one might typically think about using the Navier-stokes equation for fluid dynamics simulations. However, blood is a a multiphase non-Newtonian viscoelastic fluid. These properties essentially mean the continuum approximations of Navier-stokes do not hold for modeling blood flow. [Click here to see the python code](https://github.com/yonglid/CS205-Final-Project/blob/master/Lattice_Boltzmann.py)

Overall, there are a few advantages of using LBM to model blood flow. 

1)	It can be used to simulate multiphase flow
2)	It can more readily include complex boundary conditions
3)	It can easily be parallelized. 

Boltzmann’s theory of kinetic gasses essentially says that gasses or fluids can be regarded as small particles with random motions. This idea is simplified by the Lattice-Boltzmann method is a simplification of Boltzmann’s original idea by restricting the number of particles and confining the velocity vectors to the nodes of a lattice. Thus, LBM is an ideal balance between microscopic (bottom-up) and macroscopic (top-down) molecular dynamic simulations.

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM1.png)
**_Lattice-Boltzman uses discrete particles on a lattice which can be summed to create a simplified 2D Navier-stokes model._**

We focus on the two-dimensional blood flow simulation by using LBM to model Navier stokes.

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM2.png)

**_Lattice scheme to model Navier-Stokes._**

The basic process of Lattice-Boltzmann is illustrated below:

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM3.png)
**_Each point on the lattice has particles with discrete velocities._**

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM4.png)
**_Transport phase: shift of data along each independent velocity vector._**

![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM5.png)
**_Relaxation phase: Determines the microscopic dynamics towards local equilibrium and macroscopic transport coefficients (tune to get desired dynamics)_**


![test](https://github.com/yonglid/CS205-Final-Project/blob/master/LBM6.png)
**_Repeat transport and relaxation_**


Results: The lattice boltzmann model shows that at least for the approximate values for blood flow, the velocity does not converge to the expected values. One reason for this could be the compressiblity error becomes dominant. To improve this model, one solution is to use incompressible boundary conditons.
  
![test](https://github.com/yonglid/CS205-Final-Project/blob/master/figure_1.png)



# Citations

B. J. Krijgsman, Biological Reviews, 31, 288, 1956

C. C. Mitchell, D. G. Schaeffer, Bulletin of Mathematical Biology, 65, 767, 2003

L. D. Waldrop and L. Miller, Journal of Experimental Biology, 218, 2753, 2015

J. W. Cain, D. G. Schaeffer, SIAM Review 48, 537, 2006

J. W. Cain, E. G. Tolacheva, D. G. Shaeffer, and D. J. Gauthier, Physical Review E70, 061906, 2004

M. E. Kriebel, Journal of General Physiology, 50, 2097, 1967

M. E. Kriebel, Biological Bulletin, 134, 434, 1968

C. H. Luo and Y. Rudy, Circulation Research 74, 1071, 1994

Y. Liu, Applied Mathematical Modelling, 36,7, pp.2890-2899, 2012
