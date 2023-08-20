import numpy as np
from fracture_model_1 import *
from save_avalanches import *
from parameters import *
import time

def main_function(N, lbda, lbda_J, lbda_f, rho, rep, filename):

    # data = []
    myFile = open(output_dir+filename+'.csv', 'w')


    for i in range(rep):
        if i%1==0: print(i)
        thresholds = np.random.weibull(rho, N)
        # print(np.sort(thresholds))
        fracture = Fracture_Model_1(N, lbda, lbda_J, lbda_f, rho, thresholds)
        aav = fracture.get_avalanches()
        # print(aav)
        # data = np.append(data,Data(aav))
        data_to_save = np.append(aav,np.zeros(N-len(aav)))
        save_avalanches_csv(data_to_save,output_dir+filename+'.csv')

    # save_avalanches(data,output_dir+filename+'.obj')
    # save_avalanches_csv(aav,output_dir+myFile)
    end = time.time()
    print("total time: ", end - start)
    # print(aav)
    print(sum(aav))

start = time.time()

if __name__ == '__main__':
    main_function(N, lbda, lbda_J, lbda_f, rho, rep, filename)
