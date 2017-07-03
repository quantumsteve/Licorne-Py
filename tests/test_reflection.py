from licorne import reflection
import numpy as np
from numpy.testing import assert_array_almost_equal
import os
import unittest

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
            RRr = reflection.resolut(RR, q, dq, 2)
            RRr = RRr * norm_factor[k] + background

            reference_values = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/res_mode2refl'+str(k+1)+'.dat'), unpack=True)
            assert_array_almost_equal(reference_values, RRr)

        for k in range(n_of_outputs):
            RR = reflection.spin_av(R, pol_vecs[k], an_vecs[k], pol_eff, an_eff)
            RRr = reflection.resolut(RR, q, dq, 1)
            RRr = RRr * norm_factor[k] + background

            reference_values = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/res_mode1refl'+str(k+1)+'.dat'), unpack=True)
            assert_array_almost_equal(reference_values, RRr)

        for k in range(n_of_outputs):
            RR = reflection.spin_av(R, pol_vecs[k], an_vecs[k], pol_eff, an_eff)
            RRr = reflection.resolut(RR, q, dq, 3)
            RRr = RRr * norm_factor[k] + background

            reference_values = np.loadtxt(os.path.join(os.path.dirname(__file__),'data/res_mode3refl'+str(k+1)+'.dat'), unpack=True)
            assert_array_almost_equal(reference_values, RRr)

if __name__ == '__main__':
    unittest.main()

