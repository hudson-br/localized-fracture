



def main_function(N, lbda, lbda_J, lbda_f, rho, rep, filename):

    start = time.time()


    # vector defining the state of a bond 
    # alpha[i] = 0: i'th bond is broken
    # alpha[i] = 1: i'th bond is intact
    alpha = np.ones(N)


    import random


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

import numpy as np
from fracture_model_1 import *
from save_avalanches import *
from numpy import array
from parameters import *

import time
# import csv
# import os
# import configreader



start = time.time()
if __name__ == '__main__':
    main_function(N, lbda, lbda_J, lbda_f, rho, rep, filename)
