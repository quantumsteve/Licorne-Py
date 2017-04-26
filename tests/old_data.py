import unittest
from licorne import reflection
import numpy as np

class Layer:
    pass


class TestReflectionClass(unittest.TestCase):
    def test_reference_results(self):
        paramfile = open('data/refl_par.dat','r')
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

        q = []
        dq = []
        with open('data/refl_q_dq.dat','r') as qfile:
            for line in qfile:
                tmp = [float(value) for value in line.split()]
                q.append(tmp[0])
                dq.append(tmp[1])
        qfile.close()
        q = np.array(q)
        dq = np.array(dq)
        inc_moment = q / 2.0
        pol_eff = np.ones(len(q), dtype=np.complex128)
        an_eff = np.ones(len(q), dtype=np.complex128)

        R = reflection.reflection(inc_moment, layers, substrate)
        for k in range(n_of_outputs):
            RR = reflection.spin_av(R, pol_vecs[k], an_vecs[k], pol_eff, an_eff)
            RRr = reflection.resolut(RR, q, dq)
            RRr = RRr * norm_factor[k] + background

            reference_values = []
            with open('data/refl'+str(k+1)+'.dat', 'r') as reflfile:
                for line in reflfile:
                    reference_values.append(float(line))
            reflfile.close()

            self.assertEqual(len(reference_values),len(RRr))
            for value, reference in zip(RRr, reference_values):
                self.assertAlmostEqual(value,reference)

if __name__ == '__main__':
    unittest.main()

