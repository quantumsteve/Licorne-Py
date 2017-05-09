from .NumericParameter import NumericParameter, to_iterable
import operator
import numpy as np
from enum import Enum

class RoughnessModel(Enum):
    NONE=1
    ERFC=2
    TANH=3
    NEVOT_CROCE=4


class MSLD(object):
    """
    Class that stores information about the magnetic scattering length density
    """
    def __init__(self,rho=0.,theta=0., phi=0.):
        '''
        Parameters
        ----------
        rho : float
        theta : float
        phi : float
            The polar components of the magnetic density vector
        '''
        self.rho=rho
        self.theta=theta
        self.phi=phi

    def __repr__(self):
        s="msld:"
        for x in (self.rho, self.theta, self.phi):
            s+='\n  '+x.__repr__()
        return s

    rho = property(operator.attrgetter('_rho'))
    @rho.setter
    def rho(self,r):
        self._rho = NumericParameter('rho',*to_iterable(r))

    theta = property(operator.attrgetter('_theta'))
    @theta.setter
    def theta(self,t):
        self._theta = NumericParameter('theta',t)

    phi = property(operator.attrgetter('_phi'))
    @phi.setter
    def phi(self,p):
        self._phi = NumericParameter('phi',p)


class Layer(object):
    """
    A Layer object is a container for properties (including fitting)
    for a single layer
    """
    def __init__(self,thickness=0.,
                 nsld_real=0.,
                 nsld_imaginary=0.,
                 msld_rho=0.,
                 msld_theta=0.,
                 msld_phi=0.,
                 roughness=0.,
                 roughness_model=RoughnessModel.NONE,
                 name=None):
        """
        Create a layer with the following parameters:
        - thickness: thickness
        - nsld_real: nuclear scattering length density (real part)
        - nsld_imaginary: nuclear scattering length density (imaginary part)
        - msld_rho: magnetic scattering length density magnitude
        - msld_theta: magnetic scattering length density magnitude
        - msld_phi: magnetic scattering length density magnitude
        - roughness: roughness
        - roughess_model: model for the roughness, one of RoughnessModel types
        - name: an optional string to use as the name of the layer
        Numerical parameters have minimum/maximum values that are going
        to be used for fitting. To input just the value, just enter a single number.
        To input the value, minimum and maximum, you should enter a 
        triplet (list,set, numpy array, etc)
        """
        self.thickness=thickness
        self.nsld_real=nsld_real
        self.nsld_imaginary=nsld_imaginary
        self.msld=(msld_rho,msld_theta, msld_phi)
        self.roughness=roughness
        self.roughness_model=roughness_model
        self.name=name

    def __repr__(self):
        s=[]
        s.append("name: {0}".format(self.name))
        for x in [self.thickness,self.nsld_real,self.nsld_imaginary,self.msld, self.roughness]:
            s.append(x.__repr__())
        s.append("roughness_model: {0}".format(self.roughness_model))
        return '\n '.join(s)

    name = property(operator.attrgetter('_name'))
    @name.setter
    def name(self,n):
        if n is not None:
            self._name = str(n)
        else:
            self._name = ''

    thickness = property(operator.attrgetter('_thickness'))
    @thickness.setter
    def thickness(self,v):
        self._thickness = NumericParameter('thickness',v)

    nsld_real = property(operator.attrgetter('_nsld_real'))
    @nsld_real.setter
    def nsld_real(self,v):
        self._nsld_real = NumericParameter('nsld_real',v)

    nsld_imaginary = property(operator.attrgetter('_nsld_imaginary'))
    @nsld_imaginary.setter
    def nsld_imaginary(self,v):
        self._nsld_imaginary = NumericParameter('nsld_imaginary',v)

    @property
    def nsld(self):
        return np.complex(self.nsld_real.value,self.nsld_imaginary.value)
    @nsld.setter
    def nsld(self,v):
        v=np.complex(*to_iterable(v,dtype=np.complex))
        self.nsld_real.value=v.real
        self.nsld_imaginary.value=v.imag

    msld = property(operator.attrgetter('_msld'))
    @msld.setter
    def msld(self,v):
        self._msld = MSLD(v)

    roughness = property(operator.attrgetter('_roughness'))
    @roughness.setter
    def roughness(self,v):
        self._roughness = NumericParameter('roughness',v)

    roughness_model = property(operator.attrgetter('_roughness_model'))
    @roughness_model.setter
    def roughness_model(self,v):
        if not isinstance(v,RoughnessModel):
            raise ValueError('roughness_model is not the corect type')
        self._roughness_model = v

