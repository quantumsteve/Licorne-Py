import unittest
import numpy as np
from licorne.layer import Layer,RoughnessModel
from licorne.generateSublayers import generateSublayers

class TestGenerateSublayers(unittest.TestCase):

    def test_sublayers(self):
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
                       roughness_model=RoughnessModel.NONE,
                       sublayers=10)
        layers=[Incoming,Layer1,Layer2,Layer3,Substrate]
        sublayers,corresponding=generateSublayers(layers)
        for s in sublayers:
            print(s.thickness.value,s.nsld_real.value)


if __name__ == '__main__':
    unittest.main()
