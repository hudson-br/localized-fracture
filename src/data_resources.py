import pickle
import numpy as np
import powerlaw
import matplotlib.pyplot as plt

def save_avalanches(data, filename):

    with open(filename, 'wb') as fileObj:
        fileObj = open(filename, 'wb')
        pickle.dump(data,fileObj)
        
def avalanche_statistics_from_csv(file):

    fileObj = open(file, 'rb')
    Obj = pickle.load(fileObj, encoding="utf-8")
    fileObj.close()

    ff = np.genfromtxt(file, delimiter=',', unpack=True)

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

def avalanche_statistics_from_csv(file):

    import pickle 

    fileObj = open(file, 'rb')
    Obj = pickle.load(fileObj, encoding="utf-8")
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


def avalanche_statistics(file):

    import pickle 

    fileObj = open(file, 'rb')
    Obj = pickle.load(fileObj, encoding="utf-8")
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


def avalanche_distribution_from_obj(file):
    import pickle 
    import powerlaw
    fileObj = open(file, 'rb')
    # Obj = pickle.load(fileObj, encoding='latin1')
    Obj = pickle.load(fileObj)
    fileObj.close()

    N = sum(Obj[0].avalanches)
    number_of_avalanches = np.zeros(int(N-1))
    for i in range(len(Obj)):
        [number_of_avalanches_t, bins] = np.histogram(Obj[i].avalanches, bins = np.arange(0,N))
        number_of_avalanches = number_of_avalanches + number_of_avalanches_t
    data = np.repeat(bins[:-1].astype(int),number_of_avalanches.astype(int))
    results = powerlaw.Fit(data)#,xmin = 10, xmax = 1000,  fit_method='KS')
    alpha = results.power_law.alpha
    xmin = results.power_law.xmin
    sigma = results.power_law.sigma
    
    return [alpha, sigma, xmin]

def plot_avalanche_from_obj(file):
    fileObj = open(file, 'rb')
    Obj = pickle.load(fileObj,encoding="latin1")
    fileObj.close()

    N = sum(Obj[0].avalanches)

    number_of_avalanches = np.zeros(int(N-1))
    for i in range(len(Obj)):
        [number_of_avalanches_t, bins] = np.histogram(Obj[i].avalanches, bins = np.arange(0,N))
        number_of_avalanches = number_of_avalanches + number_of_avalanches_t
    index = np.nonzero(number_of_avalanches)
    plt.figure()
    plt.loglog(bins[index],number_of_avalanches[index]/sum(bins[index]*number_of_avalanches[index]),'.')
    return 0

def plot_avalanche_from_csv(file):
    left = 'N='
    right = '_lbda'
    N = int(file[file.index(left)+len(left):file.index(right)])
    ff = np.genfromtxt(file, delimiter=',', unpack=True)

    number_of_avalanches = np.zeros(int(N-1))

    # repetitions = len(ff)/N

    [number_of_avalanches, bins] = np.histogram(np.nonzero(ff), bins = np.logspace(0,N,20))
    index = np.nonzero(number_of_avalanches)
    plt.figure()
    plt.loglog(bins[index],number_of_avalanches[index]/sum(bins[index]*number_of_avalanches[index]),'.')
    return 0
