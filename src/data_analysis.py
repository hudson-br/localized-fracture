import pickle
import numpy as np

def save_avalanches(data, filename):

    with open(filename, 'wb') as fileObj:
        fileObj = open(filename, 'wb')
        pickle.dump(data,fileObj)
        

def avalanche_statistics(file):

    import pickle 

    fileObj = open(file, 'rb')
    Obj = pickle.load(fileObj)
    fileObj.close()

    max_avalanche = []
    average_avalanche = []
    average_length = []

    for i in range(len(Obj)):
        max_avalanche = np.append(max_avalanche, max(Obj[i].avalanches))
        ind = np.argmax(Obj[i].avalanches)
        average_length = np.append(average_length, len(Obj[i].avalanches[:ind]))
        average_avalanche = np.append(average_avalanche, sum(Obj[i].avalanches[:ind])/len(Obj[i].avalanches[:ind]))

    import statistics 
    
    return [statistics.mean(average_avalanche), statistics.stdev(average_avalanche), \
            statistics.mean(max_avalanche), statistics.stdev(max_avalanche),\
            statistics.mean(average_length), statistics.stdev(average_length)]

