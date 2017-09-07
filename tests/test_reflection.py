from licorne import reflection
import numpy as np
from numpy.testing import assert_array_almost_equal
import os,copy
import unittest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Layer(object):
    pass

class TestReflectionClass(unittest.TestCase):
    def test_reference_results(self):
        paramfile = open(os.path.join(os.path.dirname(__file__),'data/refl_par.dat'),'r')
        n_monte_carlo = int(paramfile.readline())
        formalism = int(paramfile.readline())
        res_mode = int(paramfile.readline())
        n_of_outputs = int(paramfile.readline())
        pol_vecs = np.array([float(value) for value in paramfile.readline().strip().split()]).reshape(6,3)
        an_vecs = np.array([float(value) for value in paramfile.readline().strip().split()]).reshape(6,3)
        pol_fun = [int(value) for value in paramfile.readline().split()]
        norm_factor = [int(value) for value in paramfile.readline().split()]
        maxwell = int(paramfile.readline())
        glance_angle = int(paramfile.readline())
        background = float(paramfile.readline())
        percentage = float(paramfile.readline())
        nlayers1 = int(paramfile.readline())
        substrate_tmp = [float(value) for value in paramfile.readline().split()]
        substrate = complex(substrate_tmp[0],substrate_tmp[1])
        NC = float(paramfile.readline())
        layers = []
        for i in range(nlayers1):
            l = Layer()
            l.thickness = float(paramfile.readline())
            nsld_tmp = [float(value) for value in paramfile.readline().split()]
            l.nsld = complex(nsld_tmp[0], nsld_tmp[1])
            l.msld = [float(value) for value in paramfile.readline().split()]
            l.NC = float(paramfile.readline())
            layers.append(l)

        paramfile.close()

        q, dq = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/refl_q_dq.dat'),unpack=True)
        inc_moment = q / 2.0

        pol_eff = np.ones(len(q), dtype=np.complex128)
        an_eff = np.ones(len(q), dtype=np.complex128)

        R = reflection.reflection(inc_moment, layers, substrate)
        for k in range(n_of_outputs):
            RR = reflection.spin_av(R, pol_vecs[k], an_vecs[k], pol_eff, an_eff)
            RR = np.real(RR)
            for res_mode in range(1,3):
                RRr = reflection.resolut(RR, q, dq, res_mode)
                RRr = RRr * norm_factor[k] + background
                reference_values = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/res_mode'+str(res_mode)+'refl'+str(k+1)+'.dat'), unpack=True)
                assert_array_almost_equal(reference_values, RRr)

class resolution:
    def __init__(self):
        self.Theta1 = 0.0068
        self.Theta2 = 0.01
        self.Theta3 = 0.017
        self.DTheta1 = 0.0003
        self.DTheta2 = 0.0005
        self.DTheta3 = 0.0009
        self.Q1 = 0.03
        self.Q2 = 0.045
        self.DLambda = 0.005
    
    def LambdaQP1(self, Q):
        return 4.0 * np.pi * np.sin(self.Theta1) / Q
    def LambdaQP2(self, Q):
        return 4.0 * np.pi * np.sin(self.Theta2) / Q
    def LambdaQP3(self, Q):
        return 4.0 * np.pi * np.sin(self.Theta3) / Q
    def Lambda(self, Q):
        if Q < self.Q1:
            return self.LambdaQP1(Q)
        elif Q < self.Q2:
            return self.LambdaQP2(Q)
        else:
            return self.LambdaQP3(Q)

    def SigmaQP1(self, Q):
        return Q * np.sqrt(np.power(self.DTheta1 / self.Theta1, 2) + np.power(self.DLambda / self.LambdaQP1(Q), 2))

    def SigmaQP2(self, Q):
        return Q * np.sqrt(np.power(self.DTheta2 / self.Theta2, 2) + np.power(self.DLambda / self.LambdaQP2(Q), 2))

    def SigmaQP3(self, Q):
        return Q * np.sqrt(np.power(self.DTheta3 / self.Theta3, 2) + np.power(self.DLambda / self.LambdaQP3(Q), 2))

    def Sigma(self, Q):
        if(Q < self.Q1):
            return self.SigmaQP1(Q)
        elif (Q < self.Q2):
            return self.SigmaQP2(Q)
        else:
            return self.SigmaQP3(Q)

class Testchi3_137(unittest.TestCase):
    q = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/chi3_137/q.dat'),unpack=True)
    inc_moment = q / 2.0

    res = resolution()
    sigma = []
    for value in q:
        sigma.append(res.Sigma(value))

    sigma = np.array(sigma)

    substrate = complex(3.6214e-006, 0.0)
    layer_info = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data/chi3_137/profile_sublayers.dat'))
    layer_info = layer_info[:-1]
    layers = []
    for line in layer_info:
        l = Layer()
        l.thickness = line[1]
        l.nsld = complex(line[2], line[3])
        msld = [line[4], np.deg2rad(line[5]), np.deg2rad(line[6])]
        l.msld = [msld[0]*np.sin(msld[2])*np.cos(msld[1]), msld[0]*np.sin(msld[2])*np.sin(msld[1]), msld[0]*np.cos(msld[2])]
        l.NC = 0.0
        layers.append(l)

    R = reflection.reflection(inc_moment, layers, substrate)
    pol_vecs = [[0.98,0.0,0.0], [-0.98,0.0,0.0], [0.98,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0]]
    an_vecs = [[0.98,0.0,0.0], [-0.98,0.0,0.0], [-0.98,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0]]
    norm_factor=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    background=1.2e-05;

    pol_eff = np.ones(len(q), dtype = np.complex128)
    an_eff = np.ones(len(q), dtype = np.complex128)

    n_of_outputs = 3
    for k in range(n_of_outputs):
        RR = reflection.spin_av(R, pol_vecs[k], an_vecs[k], pol_eff, an_eff)
        RR = np.real(RR)
        RRr = reflection.resolut(RR, q, sigma, 3)
        RRr = RRr * norm_factor[k] + background
        fig,ax = plt.subplots()
        ax.semilogy(q,RRr,label='calculation')
        #plt.xlim([0.0,0.06])
        #plt.ylim([1.0e-4,10.0])
        reference_values = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/chi3_137/rtheory'+str(k+1)+'.dat'), unpack=True)
        assert_array_almost_equal(RRr,reference_values,2)
        ax.semilogy(q, reference_values, label='reference')
        ax.set_xlabel('Momentum Transfer $\AA^{-1}$')
        ax.set_ylabel('Reflectivity')
        ax.set_title('Polarization ({},{},{}), Analysis({},{},{})'.format(pol_vecs[k][0],pol_vecs[k][1],pol_vecs[k][2],an_vecs[k][0],an_vecs[k][1],an_vecs[k][2]))
        ax.legend()
        fig.savefig('chi3_137_'+str(k+1)+'.pdf')
        plt.close()        

class Testr2_6_508(unittest.TestCase):
    q = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/r2_6_508/q.dat'),unpack=True)
    inc_moment = q / 2.0

    res = resolution()
    sigma = []
    for value in q:
        sigma.append(res.Sigma(value))
    sigma = np.array(sigma)

    substrate = complex(3.533e-006, 0.0)
    layer_info = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data/r2_6_508/profile_sublayers.dat'))
    layer_info = layer_info[:-1]
    layers = []
    for line in layer_info:
        l = Layer()
        l.thickness = line[1]
        l.nsld = complex(line[2], line[3])
        msld = [line[4], np.deg2rad(line[5]), np.deg2rad(line[6])]
        l.msld = [msld[0]*np.sin(msld[2])*np.cos(msld[1]), msld[0]*np.sin(msld[2])*np.sin(msld[1]), msld[0]*np.cos(msld[2])]
        l.NC = 0.0
        layers.append(l)

    R = reflection.reflection(inc_moment, layers, substrate)
    pol_vecs = [[0.98,0.0,0.0], [-0.98,0.0,0.0], [0.98,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0]]
    an_vecs = [[0.98,0.0,0.0], [-0.98,0.0,0.0], [-0.98,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0]]
    norm_factor=[1.05, 1.05, 1.05, 1.05, 1.05, 1.05]
    background=1.e-06;

    pol_eff = np.ones(len(q), dtype = np.complex128)
    an_eff = np.ones(len(q), dtype = np.complex128)

    n_of_outputs = 3
    for k in range(n_of_outputs):
        RR = reflection.spin_av(R, pol_vecs[k], an_vecs[k], pol_eff, an_eff)
        RR = np.real(RR)
        RRr = reflection.resolut(RR, q, sigma, 3)
        RRr = RRr * norm_factor[k] + background
        fig,ax = plt.subplots()
        ax.semilogy(q, RRr, label='calculation')
        reference_values = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/r2_6_508/rtheory'+str(k+1)+'.dat'), unpack=True)
        assert_array_almost_equal(RRr,reference_values,5)
        ax.semilogy(q, reference_values, label='reference')
        ax.set_xlabel('Momentum Transfer $\AA^{-1}$')
        ax.set_ylabel('Reflectivity')
        ax.set_title('Polarization ({},{},{}), Analysis({},{},{})'.format(pol_vecs[k][0],pol_vecs[k][1],pol_vecs[k][2],an_vecs[k][0],an_vecs[k][1],an_vecs[k][2]))
        ax.legend()
        fig.savefig('r2_6_508_'+str(k+1)+'.pdf')
        plt.close()

class resolution2:
    def __init__(self):
        self.DTheta1 = 0.0
        self.DTheta2 = 0.0007
        self.Q1 = 0.0
        self.Lambda = 5.0
        self.DLambda = 0.01

    def SigmaQP1(self, Q):
        Theta = np.arcsin(Q*self.Lambda/(4.0*np.pi));
        return Q * np.sqrt(np.power(self.DTheta1 / Theta, 2) + np.power(self.DLambda / self.Lambda, 2))

    def SigmaQP2(self, Q):
        Theta = np.arcsin(Q*self.Lambda/(4.0*np.pi));
        return Q * np.sqrt(np.power(self.DTheta2 / Theta, 2) + np.power(self.DLambda / self.Lambda, 2))

    def Sigma(self, Q):
        if(Q < self.Q1):
            return self.SigmaQP1(Q)
        else:
            return self.SigmaQP2(Q)

class Testhelix100(unittest.TestCase):
    q = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/helix100/q.dat'),unpack=True)
    inc_moment = q / 2.0

    res = resolution2()
    sigma = []
    for value in q:
        sigma.append(res.Sigma(value))
    sigma = np.array(sigma)

    substrate = complex(6.0e-6, 0.0)
    layer_info = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data/helix100/profile_sublayers.dat'))
    layer_info = layer_info[:-1]
    layers = []
    for line in layer_info:
        l = Layer()
        l.thickness = line[1] # +0.05 # fit improved by adding 0.05?
        l.nsld = complex(line[2], line[3])
        msld = [line[4], np.deg2rad(line[5]), np.deg2rad(line[6])]
        l.msld = [msld[0]*np.sin(msld[2])*np.cos(msld[1]), msld[0]*np.sin(msld[2])*np.sin(msld[1]), msld[0]*np.cos(msld[2])]
        l.NC = 0.0
        layers.append(l)
    R = reflection.reflection(inc_moment, layers, substrate)

    pol_vecs = [[1,0,0],[-1,0,0],[-1,0,0],[0,0,0],[0,0,0],[0,0,0]]
    an_vecs = [[1,0,0],[-1,0,0],[1,0,0],[0,0,0],[0,0,0],[0,0,0]]

    norm_factor=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    background=1.e-06

    pol_eff = np.ones(len(q), dtype = np.complex128)
    an_eff = np.ones(len(q), dtype = np.complex128)

    n_of_outputs = 3
    for k in range(n_of_outputs):
        RR = reflection.spin_av(R, pol_vecs[k], an_vecs[k], pol_eff, an_eff)
        RR = np.real(RR)
        RRr = reflection.resolut(RR, q, sigma, 3)
        RRr = RRr * norm_factor[k] + background
        fig,ax = plt.subplots()
        ax.semilogy(q,RRr,label='calculation')
        reference_values = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/helix100/rtheory'+str(k+1)+'.dat'), unpack=True)
        assert_array_almost_equal(RRr,reference_values,5)
        ax.semilogy(q, reference_values, label='reference')
        ax.set_xlabel('Momentum Transfer $\AA^{-1}$')
        ax.set_ylabel('Reflectivity')
        ax.set_title('Polarization ({},{},{}), Analysis({},{},{})'.format(pol_vecs[k][0],pol_vecs[k][1],pol_vecs[k][2],an_vecs[k][0],an_vecs[k][1],an_vecs[k][2]))
        ax.legend()
        fig.savefig('helix100_'+str(k+1)+'.pdf')
        plt.close()

if __name__ == '__main__':
    unittest.main()

