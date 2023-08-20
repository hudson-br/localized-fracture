import pickle
import numpy as np
def save_avalanches(data, filename):

    with open(filename, 'wb') as fileObj:
        fileObj = open(filename, 'wb')
        pickle.dump(data,fileObj)
        

def save_avalanches_csv(data,filename):
    with open(filename,'a') as f:
        np.savetxt(f,data, delimiter=",")

def save_avalanches_txt(data,filename):

    with open(filename,'ab') as f:
        np.savetxt(f, data)
        f.write(b"\n")

class Data():
    def __init__ (self, avalanches):
#         self.thresholds = thresholds
        self.avalanches = avalanches