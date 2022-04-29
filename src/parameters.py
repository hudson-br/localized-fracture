import configreader
import os
import numpy as np

cwd = os.getcwd()


# Create config object
C = configreader.Config()
config = C.read("config.conf")


output_dir = "output/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)



print("hello")
N = int(float(config['parameters']['system_size']))

rep = int(config['simulation']['repetitions']) # Repetitions of the realization for the avalanche statistics

# vector defining the state of a bond 
# alpha[i] = 0: i'th bond is broken
# alpha[i] =1 : i'th bond is intact
# alpha = np.ones(N) 

# Dimensionless parameters 
lbda = float(config['parameters']['lambda'])              # internal elasticity in series to the bonds
lbda_J = float(config['parameters']['lambda_J'])            # short-range elasticity
lbda_f = float(config['parameters']['lambda_f'])            # external elastic element

# Definition of the thresholds
rho = float(config['parameters']['rho'])               # shape of the Weibull distribution
thresholds = np.random.weibull(rho, N)

filename = "N={}_lbda={}_lbdaf={}_lbdaJ={}_rho={}".format(N,lbda,lbda_f,round(lbda_J,2),rho)


output_dir = "output/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)