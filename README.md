# CS205-Final-Project
Final Project
Current team: Peter Chang, Yong Li Dich, Alexander Wu, Anita Chandrahas 

Project research: Observe sea squirt that pumps blood in two directions to determine potential mathematical methods that govern the reversals within the heart, which would be tested through simulation.

Methods: random variation method and a controlled shifting method

Language: Current code in Python from Peter's research project - but might be re-coding in C or transforming with Cython 


Benchmarking:

Step = 10^-2, L=3.0, N=300

10ms, res=10: time=1.06

100ms, res=10: time=6.02

100ms, res=100: time=5.76

1000ms, res=600: time=52.2

10000ms, res=600: time=527.0

30000ms, res=600: time=1753.3


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