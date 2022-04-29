import numpy as np
from fracture_model_1 import *
from save_avalanches import *
from numpy import array
from parameters import *
import time

def main_function(N, lbda, lbda_J, lbda_f, rho, rep, filename):

    data = []

    for i in range(rep):
        if i%1==0: print(i)
        fracture = Fracture_Model_1(N, lbda, lbda_J, lbda_f, rho)
        thresholds = np.random.weibull(rho, N)
        aav = fracture.get_avalanches(thresholds)
    #     print(aav)
        data = np.append(data,Data(aav))


    save_avalanches(data,output_dir+filename+'.obj')
    end = time.time()
    print("total time: ", end - start)

start = time.time()

if __name__ == '__main__':
    main_function(N, lbda, lbda_J, lbda_f, rho, rep, filename)
