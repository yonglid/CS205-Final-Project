from full_write_par import *
import time

start = time.time()
#Value in main is number of milliseconds to compute
main(60000)        #using 60000 gives 1 minute of simulation
print("Time: ", time.time()-start)
