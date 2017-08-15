import unittest,os
import numpy as np
from licorne.layer import Layer,RoughnessModel
from licorne.generateSublayers import generateSublayers


def layer_data_for_testing():
    Incoming=Layer(thickness=np.inf,
                   nsld_real=0,
                   nsld_imaginary=0,
                   msld_rho=0,
                   msld_phi=0,
                   msld_theta=0,
                   roughness=0,
                   roughness_model=RoughnessModel.NONE,
                   sublayers=16)
    Layer1=Layer(thickness=95.6772,
                   nsld_real=3.3458e-6,
                   nsld_imaginary=-3e-8,
                   msld_rho=0,
                   msld_phi=0,
                   msld_theta=90,
                   roughness=5.,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10)
    Layer2=Layer(thickness=40.6943,
                   nsld_real=3.5159e-6,
                   nsld_imaginary=-3e-8,
                   msld_rho=5.31171e-7,
                   msld_phi=11.1877,
                   msld_theta=90,
                   roughness=5.,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10)
    Layer3=Layer(thickness=78.5585,
                   nsld_real=2.3132e-006,
                   nsld_imaginary=-3e-8,
                   msld_rho=1.96841e-006,
                   msld_phi=10.8359,
                   msld_theta=90,
                   roughness=5,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10)
    Layer4=Layer(thickness=124.141,
                   nsld_real=2.4347e-006,
                   nsld_imaginary=-3e-8,
                   msld_rho=2.28882e-006,
                   msld_phi=9.48435,
                   msld_theta=90,
                   roughness=5,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10)
    Layer5=Layer(thickness=65.6139,
                   nsld_real=4.1353e-006,
                   nsld_imaginary=-3e-8,
                   msld_rho=-1.54978e-008,
                   msld_phi=-55.6648,
                   msld_theta=90,
                   roughness=5,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10)
    Layer6=Layer(thickness=254.437,
                   nsld_real=5.7216e-006,
                   nsld_imaginary=-2.5693e-021,
                   msld_rho=0,
                   msld_phi=0,
                   msld_theta=90,
                   roughness=5,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10) 
    Layer7=Layer(thickness=59.2843,
                   nsld_real=3.7163e-006,
                   nsld_imaginary=+3.3154e-020,
                   msld_rho=3.65952e-007,
                   msld_phi=-16.3845,
                   msld_theta=90,
                   roughness=5,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10)
    Layer8=Layer(thickness=165.617,
                   nsld_real=3.8014e-006,
                   nsld_imaginary=+4.2572e-020,
                   msld_rho=9.61537e-007,
                   msld_phi=-5.01155,
                   msld_theta=90,
                   roughness=5,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10)                      
    Substrate=Layer(thickness=np.inf,
                   nsld_real=3.533e-006,
                   nsld_imaginary=0,
                   msld_rho=0,
                   msld_phi=0,
                   msld_theta=0,
                   roughness=5.,
                   roughness_model=RoughnessModel.TANH,
                   sublayers=10)
    layers=[Incoming,Layer1,Layer2,Layer3,Layer4,Layer5,Layer6,Layer7,Layer8,Substrate]
    return layers

class TestGenerateSublayers(unittest.TestCase):

    def test_sublayers(self):
        layers=layer_data_for_testing()
        sublayers,corresponding=generateSublayers(layers)
        _, Thick, Re_NSLD, Im_NSLD, MSLD_rho, MSLD_phi, MSLD_theta=np.loadtxt(os.path.join(os.path.dirname(__file__),'data/profile_sublayers.dat'),unpack=True)
        Thick=Thick[1:-2]
        Re_NSLD=Re_NSLD[1:-2]
        Im_NSLD=Im_NSLD[1:-2]
        MSLD_rho=MSLD_rho[1:-2]
        sl_thick=np.array([s.thickness.value for s in sublayers[1:-1]])
        sl_nsld=np.array([s.nsld_real.value for s in sublayers[1:-1]])
        sl_nsldi=np.array([s.nsld_imaginary.value for s in sublayers[1:-1]])
        sl_msldr=np.array([s.msld.rho.value for s in sublayers[1:-1]])
        np.testing.assert_allclose(Thick,sl_thick,atol=1e-3)
        np.testing.assert_allclose(Re_NSLD,sl_nsld,atol=1e-10)
        np.testing.assert_allclose(Im_NSLD,sl_nsldi,atol=1e-13)
        np.testing.assert_allclose(MSLD_rho,sl_msldr,atol=1e-11)
        #Now test that msld.theta and msld.phi are constant in a layer
        sl_msldt=np.array([s.msld.theta.value for s in sublayers[1:-1]])
        sl_msldp=np.array([s.msld.phi.value for s in sublayers[1:-1]])
        corresponding=corresponding[1:-1]
        for t,p,l in zip(sl_msldt,sl_msldp,corresponding):
            self.assertAlmostEqual(t,layers[int(l)].msld.theta.value)
            self.assertAlmostEqual(p,layers[int(l)].msld.phi.value)

if __name__ == '__main__':
    unittest.main()
