import pickle

def save_avalanches(data, filename):

    with open(filename, 'wb') as fileObj:
        fileObj = open(filename, 'wb')
        pickle.dump(data,fileObj)
        
class Data():
    def __init__ (self, avalanches):
#         self.thresholds = thresholds
        self.avalanches = avalanches