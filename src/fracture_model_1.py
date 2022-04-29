import numpy as np
from scipy import sparse
from scipy.sparse.linalg import lgmres

class Fracture_Model_1:
    def __init__ (self, system_size, lbda, lbda_J, lbda_f, rho):
        self.N = system_size
        self.alpha = np.ones(system_size) 
        self.lbda = lbda
        self.lbda_J = lbda_J
        self.lbda_f = lbda_f
        self.rho = rho
        self.number_of_avalanches = np.zeros(self.N-1)
        self.thresholds = np.random.weibull(self.rho, self.N)
        self.distance_to_failure = []
        self.f = np.zeros(self.N + 1)
        self.x = np.zeros(self.N + 1)
        self.zz = []
        self.force = []


    def rigidity_matrix(self, alpha):
        I = np.arange(self.N)
        J = np.arange(self.N)
        Diagonal = alpha + self.lbda + 2.*self.lbda_J
        self.K = sparse.coo_matrix((Diagonal,(I,J)),shape=(self.N+1,self.N+1)).tocsr()

        I_upper_diagonal = np.arange(self.N-1)
        J_upper_diagonal = np.arange(1,self.N)
        Upper_diagonal = - self.lbda_J*np.ones(self.N-1)

        I_lower_diagonal = np.arange(1,self.N)
        J_lower_diagonal = np.arange(self.N - 1)
        Lower_diagonal = -self.lbda_J*np.ones(self.N - 1)

        K_upper_diagonal = sparse.coo_matrix((Upper_diagonal,(I_upper_diagonal,J_upper_diagonal)),shape=(self.N+1,self.N+1)).tocsr()
        K_lower_diagonal = sparse.coo_matrix((Lower_diagonal,(I_lower_diagonal,J_lower_diagonal)),shape=(self.N+1,self.N+1)).tocsr()

        I_right_collumn = np.arange(self.N)
        J_right_collumn = self.N*np.ones(self.N)
        Right_collumn = -self.lbda*np.ones(self.N)
        K_right_collumn = sparse.coo_matrix((Right_collumn,(I_right_collumn,J_right_collumn)),shape=(self.N+1,self.N+1)).tocsr()

        I_lower_row = self.N*np.ones(self.N)
        J_lower_row = np.arange(self.N)
        Lower_row = -self.lbda*np.ones(self.N)
        K_lower_row = sparse.coo_matrix((Lower_row,(I_lower_row,J_lower_row)),shape=(self.N+1,self.N+1)).tocsr()

        KNN = self.N*(self.lbda + self.lbda_f)
        K_NN = sparse.coo_matrix(([KNN],([self.N],[self.N])),shape=(self.N + 1,self.N + 1)).tocsr()

        # Extra terms for periodic conditions
        K_periodic_bc = sparse.coo_matrix(([-self.lbda_J, -self.lbda_J],([0, self.N-1],[self.N-1, 0])),shape=(self.N+1,self.N+1)).tocsr()

        self.K =   self.K + K_upper_diagonal + K_lower_diagonal + K_right_collumn + K_lower_row + K_NN + K_periodic_bc

    def update_rigidity_matrix(self, alpha_):
        I = np.arange(self.N)
        J = np.arange(self.N)
        Diagonal_alpha = 1.- alpha_
        K_update = sparse.coo_matrix((Diagonal_alpha,(I,J)),shape=(self.N+1,self.N+1)).tocsr()
        self.K = self.K - K_update
        
    def solve(self, z):
        self.f[self.N] = self.N*self.lbda_f*z
        x, exitcode = lgmres(self.K, self.f, x0 = self.x, atol = 1e-6)
        return x
    
    def get_avalanches(self, thresholds):
        size_alpha = len(thresholds)
        size_alpha_temp = size_alpha
        i = 0
        alpha_ = np.ones(self.N) #Keeps track of broken units 
        damage = [ ]
        z = 0.01
        tol = 1/self.N**2
        while size_alpha > 0:
            damage = np.append(damage, size_alpha_temp)
            self.rigidity_matrix(alpha_)
            self.x = self.solve(z)
            # Solving the system
            # Looking for broken bonds
            aa = (self.x[0:self.N]<thresholds - tol)  # It return boolean vector
            alpha_ = np.multiply(aa, 1)     # Need to multiply all term by 1 to get a vector of zeros and ones
            # vector defining the state of a bond
            # alpha[i] = 0: i'th bond is broken
            # alpha[i] = 1: i'th bond is intact
            size_alpha_temp = sum(alpha_)
            while size_alpha_temp < size_alpha:
                size_alpha = size_alpha_temp
                #print(fracture.K.toarray())
                self.rigidity_matrix(alpha_)
                self.x = self.solve(z)
                # Looking for broken bonds
                aa = (self.x[0:self.N] < thresholds - tol)
                alpha_ = np.multiply(aa, 1)
                size_alpha_temp = sum(alpha_)
                
            try:    
                next_threshold = min(ii for ii in (alpha_*(thresholds - self.x[0:self.N])) if ii > 0)
                ind = np.where(alpha_*(thresholds - self.x[0:self.N]) == next_threshold)[0]
                next_threshold = next_threshold+self.x[ind]
                z = z*(next_threshold/self.x[ind]) # Next loading
                alpha_[ind] = 0
            except:
                damage = np.append(damage, 0)
                break
                
#             if i% 10 ==0: print(i, size_alpha_temp)
            i+=1
        aav = -np.diff(damage)
        aav = aav[np.nonzero(aav)]
        return aav
    
    def time_avalanches(self, damage):
        av_counter = []
        av_counter = np.append(av_counter, damage[0])
        for i in range(1, len(damage)):
            if damage[i-1] == damage[i]:
                pass
            else:
                av_counter = np.append(av_counter, damage[i])
        return (len(av_counter) - np.sum(av_counter))