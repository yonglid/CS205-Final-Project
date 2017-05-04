**Table of Contents** 

- [CS205-Final-Project](#)
- [Introduction](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#introduction)
  * [Background: Basic Physiological Equations](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#background-basic-physiological-equations)
  * [Potential Hypotheses for Blood Flow Reversal](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#potential-hypotheses-for-blood-flow-reversal)
  * [Problem to tackle](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#problem-to-tackle)
- [Technical description of parallel software solution](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#technical-description-of-parallel-software-solution)
- [Application scaling plots (benchmarking)](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#appliciable-scaling-plots-benchmarking)
- [Advanced Features](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#advanced-features)
  * [p100](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#p100)
  * [Lattice-Boltzmann](https://github.com/yonglid/CS205-Final-Project/blob/master/README.md#modeling-the-lattice-boltzmann-model-lbm)


# CS205-Final-Project

Final Project
Current team: Peter Chang, Yong Li Dich, Alexander Wu, Anita Chandrahas 

# Introduction

<p align="center"><img src="https://github.com/yonglid/CS205-Final-Project/blob/master/tunicate.jpg" width="400"></p>

The tunicate, commonly known as the sea squirt, exhibits the phenomenon of blood flow direction reversal. There are two main potential methods researched on how the tunicate carries out this nonpareil event: 1) two pacemakers with the same rates but with natural deviations 2) two pacemakers with different rates that change at every k where k is between 1 and infinity pumps. The math was initially coded out in Python to generate a video simulation of the blood flow in order to observe the two possible etiologies for the blood flow reversal.

One major issue with the research was the length of time associated with simulation generation. For each 30 second video modeling the blood reversal process, about 45 minutes of computations were needed, which is much too long when multiple parameters are needed to be tested. For this project, in order to assist in more efficient and productive research to test out more hypotheses on this phenomenon, the team implemented various parallelization methods in order to drastically speed up the simulations. The main goal of this approach was to reduce the simulation generation time, allowing for improved means of understanding the phenomenon of blood flow reversal, though the domain of blood flow simulation is also very interesting to explore (like the Lattice Boltzmann approach). 

# Background: Basic Physiological Equations

In order for a heart to pump blood, a pacemaker is required at the end of the heart fibers. This pacemaker creates electric jolts at a specific interval in order to send waves throughout the entire fiber. The heart of a sea squirt may be modeled as having two pacemakers, one at either end of the heart fiber (Krijgsman, Miller and Waldrop), which allows for blood to flow in both directions. A unique feature about wave mechanics within a heart fiber is that waves which collide do not pass through each other as most waves do. Rather, the nature of the mechanics causes the two waves to "collapse" upon collision. This allows only one of the directions to be dominant at any given moment.

Based on the Mitchell-Schaeffer model, there are two main components that govern the propagation of waves within the heart - the processes of individual heart cells and the diffusion between adjacent heart cells. When dealing with individual heart cells, there are two differential equations that govern how electric potential is stored. The first is the primary equation for voltage (Cain and Schaeffer):

<a href="https://www.codecogs.com/eqnedit.php?latex=dv/dt&space;=&space;inward&space;current-&space;outward&space;current" target="_blank"><img src="https://latex.codecogs.com/gif.latex?dv/dt&space;=&space;inward&space;current-&space;outward&space;current" title="dv/dt = inward current- outward current" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex==\frac{h}{t_{in}}&space;v^2&space;(1-v)&space;-&space;\frac{v}{t_{out}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=\frac{h}{t_{in}}&space;v^2&space;(1-v)&space;-&space;\frac{v}{t_{out}}" title="=\frac{h}{t_{in}} v^2 (1-v) - \frac{v}{t_{out}}" /></a>

Where *t~in~* and *t~out~* are physiological constants, *v* is voltage inside the cell, and *h* is a constant between 0 and 1 that represents how open or closed the cell door introducing external voltage is. The variable *h* is governed by the following piecewise ordinary differential equation:

<a href="https://www.codecogs.com/eqnedit.php?latex=dh/dt=&space;\begin{cases}&space;-h/t_{close}&space;&&space;\text{if&space;}&space;v>v_{crit}\&space;&&space;(1-h)/t_{open}&space;&&space;\text{if&space;}&space;v<v_{crit}&space;\end{cases}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?dh/dt=&space;\begin{cases}&space;-h/t_{close}&space;&&space;\text{if&space;}&space;v>v_{crit}\&space;&&space;(1-h)/t_{open}&space;&&space;\text{if&space;}&space;v<v_{crit}&space;\end{cases}" title="dh/dt= \begin{cases} -h/t_{close} & \text{if } v>v_{crit}\ & (1-h)/t_{open} & \text{if } v<v_{crit} \end{cases}" /></a>

where t~open~ and t~close~ are once again physiological constants and v~crit~ is a certain voltage level that determines how the cell will behave.  

The diffusion equation expressing voltage with respect to time is:

<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{du}{dt}&space;=&space;k&space;\frac{d^2u}{dx^2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{du}{dt}&space;=&space;k&space;\frac{d^2u}{dx^2}" title="\frac{du}{dt} = k \frac{d^2u}{dx^2}" /></a>

where *k* is another physiological constant. Diffusion will be an intrinsic factor of the cell and the cells immediately adjacent to it. We can estimate the change by diffusion using the standard Heat Equation:

<a href="https://www.codecogs.com/eqnedit.php?latex=K&space;(\frac{u_{k-1}^m&space;-&space;2u_{k}^m&space;&plus;&space;u_{k&plus;1}^m&space;}{(\Delta&space;x)^2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K&space;(\frac{u_{k-1}^m&space;-&space;2u_{k}^m&space;&plus;&space;u_{k&plus;1}^m&space;}{(\Delta&space;x)^2})" title="K (\frac{u_{k-1}^m - 2u_{k}^m + u_{k+1}^m }{(\Delta x)^2})" /></a>

where *K* is the diffusion coefficient (.001 for most biological cases), and *u* is the estimated voltage at time *m* and at location *k*. 

We also must consider boundary conditions on the cells at the beginning and ends of the fiber. By assuming the conditions under which no voltage passes through the ends, i.e. du/dx(0,t) = 0 and du/dx(L,t) = 0, we will observe an increased effect from the single adjacent cell:

<a href="https://www.codecogs.com/eqnedit.php?latex=K&space;(\frac{2u_{1}^m&space;-&space;2u_{0}^m&space;}{(\Delta&space;x)^2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K&space;(\frac{2u_{1}^m&space;-&space;2u_{0}^m&space;}{(\Delta&space;x)^2})" title="K (\frac{2u_{1}^m - 2u_{0}^m }{(\Delta x)^2})" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=K&space;(\frac{-2u_{N}^m&space;&plus;&space;2u_{N-1}^m&space;}{(\Delta&space;x)^2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K&space;(\frac{-2u_{N}^m&space;&plus;&space;2u_{N-1}^m&space;}{(\Delta&space;x)^2})" title="K (\frac{-2u_{N}^m + 2u_{N-1}^m }{(\Delta x)^2})" /></a>

where *N* is the number of cells within the heart fiber.

### Potential Hypotheses for Blood Flow Reversal

1) **Controlled Shifting Method:** In this hypothesis, the two pacemakers at the ends of the heart fiber do not have the same rate of heart pumping. At the beginning, one pacemaker will begin with a slow rate and the other begins with a fast rate. After each pump, the slow pacemaker will increase speed by a small amount and the fast pacemaker will decrease its speed. Naturally, the side with the faster rate will dominate initially, however they will eventually trade dominance and the blood flow will change. Intuitively, this hypothesis will clearly generate blood flow reversals, however the main goal was to see if the simulations generated were realistic.

2) **Random Variation Method:** In this method, the two pacemakers maintain the same average pacemaker rate but with some standard deviation between each pump. This hypothesis requires more testing in order to determine whether reversals can occur and with which parameters (such as diffusion rate, fiber length, number of cells, etc.) this model can be sustained to retain biological consistency. This parameter-heavy model is the reason why parallelising this code is important. Multiple tests must be run with different constants in order to determine whether this model can prove to be sufficient.

# Technical Description of Parallel Software Solution

In order to reduce the runtimes associated with generating simulations of blood flow, we implemented several different parallelization techniques. 

**SIMT Parallelization**   
We employed single instruction, multiple thread (SIMT) parallelization in two different ways. First, we converted the original Python implementation of the simulation to the Cython language. While the syntax of Cython mirrors that of Python, Cython importantly supports calling C functions and declaring C types on variables and class attributes. Thus, upon compilation of the Cython code, we were able to take advantage of the intrinsic efficiency of the C language relative to Python. More importantly, though, was the ability of the Cython language to readily support parallelization. In particular, we utilized the prange() function in the cython.parallel module to parallelize via multithreading the *for* loops that exist within the computationally intensive regions of our simulation. An example of the Cython implementation is included below. 

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/codeCython.png" width="550">

In addition, we manually converted the original Python version of the blood flow simulation to the C programming language. This task offered the opportunity to experience speedup due to the increased efficiency of C as well as with the integration of a number of C-compatible parallel programming models. The main SIMT parallel programming model that we selected to test was OpenACC. With OpenACC, we retained the translated C implementation of our simulation algorithm and included OpenACC directives to enable SIMT parallelization within the same highly parallelizable regions of code as in the Cython version. Specifically, we used parallel loop clauses to achieve parallelization in combination with gang, worker, and vector clauses to more explicitly specify the way in which parallelization is mapped across threadblocks, warps, and CUDA threads, respectively. 

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/codeACC.png" width="550">


**SPMD Parallelization**  
We also sought to use single program, multiple data (SPMD) parallelization models to achieve greater speedup in our simulation execution. In our implementation of this model, we designed a hybrid OpenACC + MPI program that enables multiple processors to simulateneously execute the same program while operating on different different subsets of the data. With regards to the implementation of this hybrid approach, we built upon the OpenACC version of the simluation by first initializing an MPI execution environment, called a communicator, prior to the bulk updating procedures in the simulation. We then broadcast the array storing voltage values to all other processes of the communicator via the MPI_Bcast() function. In doing so, we enable multiple copies of the OpenACC procedures to be run across a corresponding number of nodes by distributing the computation across these multiple nodes. We identified the voltage array as the optimal "message" to be broadcast due to the frequency of its use in the simulation process as well as the parallelizability of the procedures for updating voltage values across the various time points in the simulation. After the simulation is completed, the root node that initially distributed the data collects the results back and the algorithm is finished with its execution.

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/codeACCMPI.png" width="450">

# Benchmarking:

Since heart fibers range between 10 micrometers and 100 micrometers, we ran a few separate cases for benchmarking. L=3.0cm is a biologically reasonable fiber length for a tunicate. Consequently, an N of 300 will give a 100 micrometer fiber cell, N=600 gives a 50 micrometer fiber cell, and N=3000 gives a 10 micrometer fiber cell.

#### Python Serial 


| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 10  | 10 | 1.06 | - | 
| 100 | 10 | 6.02 | - |
| 100 | 100 | 5.76 | - |
| 1000 | 600 | 52.2 | - |
| 10000 | 600 | 527.0 |.016|
| 30000 | 600 | 1753.3 | .0144|

#### Cython

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 10000 | 600 | 463.6690833568573 |0.018|
| 30000 | 600 | 1553.7774078845978 |0.016|
| 60000 | 600 | 3242.5310328006744 | 0.016|

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/python_cython_throughput.png" width="512">
<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/python_speedup.png" width="512">

We can see that overall, the Python implementation has very poor performance and the Cython parallelisation does very little to actually improve the throughput. 

#### C Implementation

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 125.010000 |0.203|
| 60000 | 600 | 307.410000 | 0.165|
| 150000 | 600 | 856.340000 | 0.148|
| 500000 | 600 | 2986.510000 | 0.142|

#### OpenACC

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 61.090000 |0.415|
| 60000 | 600 | 123.010000 | 0.412|
| 150000 | 600 | 308.050000 | 0.412|
| 500000 | 600 | 1029.380000 | 0.411|

#### OpenACC + MPI [code](https://github.com/yonglid/CS205-Final-Project/blob/master/OpenACC%2BMPI/full_write_parMPI.c)

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 60.870000 |0.416|
| 60000 | 600 | 120.190000 | 0.422|
| 150000 | 600 | 299.800000 | 0.423|
| 500000 | 600 | 1001.020000 | 0.423|


<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/c300_throughput.png" width="512">

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/c300_speedup.png" width="512">

We can see that the C implementation already provides much faster simulation generation than the Python code does. Additionally, the parallelisation of the code produced much better speedups that the parallelisation of the Python code. Using OpenACC, OpenACC + MPI, and then OpenACC on the NVIDIA Tesla P100, our throughput drastically increased and the computation time was at worst, halved.

In order to better show the effects of the parallelisation, we doubled the value N, which would increase the computation in the areas that we had parallelised. An N of 600 works well and maintains good biological accuracy with the hearts cells now being 50 micrometers in length. We did not increase the N any more than this due to the necessity of numerical stability. If .001(cellsize)/(timestep^2) > 1/2, then the numerical approximations that we use will diverge in value and not provide accurate simulations. Using a value of N which is larger than 600 would necessitate a smaller timestep, which would drastically increase computation time and slow down the code more than the parallelisation would speed it up.

#### Python Serial 

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 10  | 10 | 1.02 | - | 
| 100 | 10 | 10.04 | - |
| 100 | 100 | 8.28 | - |
| 1000 | 600 | 87.96  | - |
| 10000 | 600 | 784.6  |.0215|
| 30000 | 600 | 2480.43 | .0203|


#### Cython Implementation

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 10000 | 600 | 832.72 |0.020|
| 30000 | 600 | 2601.1 |0.019|
| 60000 | 600 | 5411.19 | 0.019|


<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/p600_throughput.png" width="512">

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/p600_speedup.png" width="512">

When we increased the size of N, we actually saw a decrease in the benefits of parallelisation using Cython. In fact, the Cython code performed worse than the serial Python code. At the same time though, the throughput of the Python code was decreasing as we increased size while the Cython code stayed relatively constant. It would be plausible that for longer simulations, the Cython code would eventually overtake the Python code again. However at the objective speeds that this code was running at, running this experiment in Python/Cython is unfeasible anyway and the focus should be on doing simulations using C code.

#### C Implementation

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 501.390000 |0.101|
| 60000 | 600 | 999.530000 | 0.101|
| 150000 | 600 | 2532.830000 | 0.100|
| 500000 | 600 | 8472.320000 | 0.100|

#### OpenACC
| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 118.470000 |0.427|
| 60000 | 600 | 238.150000 | 0.425|
| 150000 | 600 | 599.230000 | 0.422|
| 500000 | 600 | 1989.600000 | 0.424|

#### OpenACC + MPI

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 110.920000 | 0.456|
| 60000 | 600 | 220.810000 | 0.459 |
| 150000 | 600 | 548.230000 | 0.461 |
| 500000 | 600 |  1830.490000 | 0.461 |

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/c600_throughput.png" width="512">

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/c600_speedup.png" width="512">

We can see that we get the best performance out of the parallelisation with the N=600. This is fantastic since an N of 600 is likely the most biologically accurate, but it also provides the scaling necessary to see an increase in the performance through parallelisation. The speedup observe from this implementation would easily allow biological hypotheses to be tested in a more reasonable amount of time, allowing for much faster scientific research to be performed.

# Advanced Features
### NVIDIA Tesla P100 GPU Accelerators

To further explore ways in which we can improve the execution of our simulation algorithm, we sought to assess the benefits of using NVIDIA Tesla P100 GPU accelerators. These GPUs are amongst the advanced available on the market and deliver the world's fastest compute node. In hopes of further expediting the blood flow simulation process, we evaluated the performance of our serial and OpenACC implementations on these P100 GPUs via the Bridges supercomputer. The results of our analysis are included below. 

#### C Serial (NVIDIA Tesla P100): N = 300

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 |  ||
| 60000 | 600 | 446.11  | |
| 150000 | 600 || |
| 500000 | 600 | | |

#### OpenACC (NVIDIA Tesla P100): N = 300

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 55.990000 |0.453|
| 60000 | 600 | 103.770000  | 0.489|
| 150000 | 600 | 271.700000 | 0.467|
| 500000 | 600 | 903.990000 | 0.467|

#### C Serial (NVIDIA Tesla P100): N = 600

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 |  ||
| 60000 | 600 | 446.11  | |
| 150000 | 600 || |
| 500000 | 600 | 1662.240000 | 0.507|


#### OpenACC (NVIDIA Tesla P100): N = 600

| ms | resolution | time | GFlops/s |
| ------------- | ------------- | ------------- | ------------- |
| 30000 | 600 | 99.860000 |0.506|
| 60000 | 600 | 200.110000  | 0.505|
| 150000 | 600 |501.820000| 0.504|
| 500000 | 600 | 1662.240000 | 0.507|

As can be seen from the data, the execution of both our serial and OpenACC paralellized models demonstrated noticeably more throughput with the P100 GPUs than with the GPUs available in Odyssey. 

### Modeling: The Lattice Boltzmann Model (LBM) [Click here to see the python code](https://github.com/yonglid/CS205-Final-Project/blob/master/Lattice_Boltzmann.py)

Our main research problem was to parallelize simulations to test the two major hyptheses for blood flow reversal, but we also wanted to explore blood flow simulation. We chose to use a 2D Lattice Boltzmann model with approximate values of tunicate blood density and velcocity.

The chosen lattice model combines the macroscopic Navier-stokes equation for fluid dynamics simulations and microscopic kinetics of individual molecules. This is especially useful since blood is a a multiphase non-Newtonian viscoelastic fluid. These fluid properties essentially mean the continuum approximations of Navier-stokes are too simple to accurately model blood flow. On the otherhand, modeling the kinetics of individual molecules with Boltzmann's theory has a large computational cost. Lattice-Boltzmann method is a simplification of Boltzmann’s original idea by restricting the number of particles and confining the velocity vectors to the nodes of a lattice. Therefore, LBM is an appropriate mesoscopic model where a fixed number of individual molecules are limited to two directional vector on a lattice.

Overall, there are a few advantages of using LBM to model blood flow. 

1)	It can be used to simulate multiphase flow
2)	It can more readily include complex boundary conditions
3)	It can easily be parallelized. 

<p align="center"><img src="https://github.com/yonglid/CS205-Final-Project/blob/master/LBM1.png" width="600"></p>

**_Lattice-Boltzman uses discrete particles on a lattice which can be summed to create a simplified 2D Navier-Stokes model._**

We focus on the two-dimensional blood flow simulation by using LBM to model Navier stokes.

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/LBM2.png" width="400">

**_Lattice scheme to model Navier-Stokes._**

The basic process of Lattice-Boltzmann is illustrated below:

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/LBM3.png" width="400">

**_Each point on the lattice has particles with discrete velocities._**

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/LBM4.png" width="400">

**_Transport phase: shift of data along each independent velocity vector._**

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/LBM5.png" width="400">

**_Relaxation phase: Determines the microscopic dynamics towards local equilibrium and macroscopic transport coefficients (tune to get desired dynamics)_**

<img src="https://github.com/yonglid/CS205-Final-Project/blob/master/LBM6.png" width="400">

**_Repeat transport and relaxation_**

**Results:** The Lattice Boltzmann model shows that at least for the approximate values for blood flow, the velocity does not converge to the expected values. Overall, this alludes to limitations with using a simple 2D LBM model. For multiphase fluids, Lattice-Boltzmann assumes that all components have the same viscocity. More accurate results have been shown with a bi-visocity model to simulate blood flow (Liu, 2012). An additional reason the D2Q9 LBM model does not match the expected curve could be the compressiblity error becomes dominant. To improve this model, one solution is to use incompressible boundary conditons.

<p align="center"><img src="https://github.com/yonglid/CS205-Final-Project/blob/master/figure_1.png" width="400"></p>


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
