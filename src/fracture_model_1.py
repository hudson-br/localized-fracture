import numpy as np
from scipy import sparse
from scipy.sparse.linalg import lgmres
from scipy.sparse.linalg import cg

class Fracture_Model_1:
    def __init__ (self, system_size, lbda, lbda_J, lbda_f, rho, thresholds):
        self.N = system_size
        self.alpha = np.ones(system_size) 
        self.health = sum(self.alpha)
        self.health_temp = sum(self.alpha)
        self.damage = []
        self.lbda = lbda
        self.lbda_J = lbda_J
        self.lbda_f = lbda_f
        self.rho = rho
        self.thresholds = thresholds
        self.f = np.zeros(self.N + 1)
        self.x = np.zeros(self.N + 1)
        self.z = 0.01
        self.tol = 0#1/self.N**2
        self.rigidity_matrix()
        self.x = self.solve()
        # print(self.K.toarray())


    def rigidity_matrix(self):
        I = np.arange(self.N)
        J = np.arange(self.N)
        Diagonal = self.alpha + self.lbda + 2.*self.lbda_J
        self.K = sparse.coo_matrix((Diagonal,(I,J)),shape=(self.N+1,self.N+1)).tocsr()

        I_upper_diagonal = np.arange(self.N-1)
        J_upper_diagonal = np.arange(1,self.N)
        Upper_diagonal = - self.lbda_J*np.ones(self.N-1)

        I_lower_diagonal = np.arange(1,self.N)
        J_lower_diagonal = np.arange(self.N - 1)
        Lower_diagonal = - self.lbda_J*np.ones(self.N - 1)

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

    def update_rigidity_matrix(self):
        I = np.arange(self.N)
        J = np.arange(self.N)
        Diagonal_alpha = 1.- self.alpha
        K_update = sparse.coo_matrix((Diagonal_alpha,(I,J)),shape=(self.N+1,self.N+1)).tocsr()
        self.K = self.K - K_update
        
    def solve(self):
        self.f[self.N] = self.N*self.lbda_f*self.z
        x, exitcode = lgmres(self.K, self.f, x0 = self.x)#, atol = 1e-5)
        return x

    def break_weakest_link(self,aa):
        weakest = np.min(np.multiply(self.thresholds,aa)[np.nonzero(np.multiply(self.thresholds,aa))])
        ind = np.where(self.thresholds == weakest)[0]
        self.alpha[ind] = 0

        
    def check_stability(self):
        self.health_temp = sum(self.alpha)
        self.rigidity_matrix()
        self.x = self.solve()
        # print(self.x)
        # Solving the system
        # Looking for broken bonds
                # get all broken units
        a = 1*(self.x[0:self.N] < self.thresholds - self.tol)
        # remove the previously broken bonds
        aa = self.alpha - a

        while np.sum(aa)>0:
            self.break_weakest_link(aa)
            self.rigidity_matrix()
            self.x = self.solve()
            a = 1*(self.x[0:self.N] < self.thresholds)
            # remove the previously broken bonds
            aa = self.alpha - a

        # aa = (self.x[0:self.N] < self.thresholds - self.tol)  # It return boolean vector
        # # self.alpha = np.multiply(aa, 1)     # Need to multiply all term by 1 to get a vector of zeros and ones
        # # print(self.alpha)
        # while self.health_temp > sum(self.alpha):
        #     self.health_temp = sum(self.alpha)
        #     self.rigidity_matrix()
        #     self.x = self.solve()
        #     # Solving the system
        #     # Looking for broken bonds
        #     aa = (self.x[0:self.N] < self.thresholds - self.tol)  # It return boolean vector
        #     self.alpha = np.multiply(aa, 1)     # Need to multiply all term by 1 to get a vector of zeros and ones
        self.health = sum(self.alpha)
       
    def next_loading(self):
        # print(self.alpha)
        # print(self.alpha*(self.thresholds - self.x[0:self.N]))
        next_threshold = min(ii for ii in (self.alpha*(self.thresholds - self.x[0:self.N])) if ii > 0)
        # next_threshold = min(ii for ii in (self.alpha*(self.thresholds)) if ii > 0)
        # print("Next threshold,", next_threshold)
        ind = np.where(self.alpha*(self.thresholds - self.x[0:self.N]) == next_threshold)[0]
        # ind = np.where(self.alpha*(self.thresholds) == next_threshold)[0]
        # print(ind)
        next_threshold = next_threshold + self.x[ind]
        # next_threshold = next_threshold + self.x[ind]
        # print("Next threshold,", next_threshold)
        # print("x[ind]", self.x[ind])
        self.z = self.z*(next_threshold/self.x[ind]) + self.tol # Next loading
        # print("Next z ", self.z)
        self.alpha[ind] = 0
    
    def get_avalanches(self):
        i = 0
        self.damage = np.append(self.damage, self.health)
        # print(self.damage)
        while self.health > 0:  
            # print("health:",self.health)
            # print(self.K.toarray())
            try:
                self.next_loading()
                self.check_stability()
                self.damage = np.append(self.damage, self.health)
            except AssertionError as error:
                print(error)
                self.damage = np.append(self.damage, 0)
                break

            i+=1
            # if i% 1000 ==0: print(i, self.health_temp)
        aav = -np.diff(self.damage)
        aav = aav[np.nonzero(aav)]
        return aav
    
