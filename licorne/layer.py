from collections import namedtuple, Iterable

NumericPar=namedtuple('NumericPar',['value','minimum','maximum'])
NumericPar.__new__.__defaults__=(0.,None,None)


# Magnetic scattering length density
MSLD=namedtuple('MSLD',['rho','theta','phi'])

class Layer(object):
    """
    A Layer object is a container for properties (including fitting)
    for a single layer
    """
    def __init__(self,thickness=0.,
                 nsld=0.,
                 nsldi=0.,
                 msld_rho=0.,
                 msld_theta=0.,
                 msld_phi=0.,
                 roughness=0.,
                 rougness_model='tanh',
                 name=None):
        """
        Create a layer with the following parameters:
        - thickness: thickness
        - nsld: nuclear scattering length density (real part)
        - nsldi: nuclear scattering length density (imaginary part)
        - msld_rho: magnetic scattering length density magnitude
        - msld_theta: magnetic scattering length density magnitude
        - msld_phi: magnetic scattering length density magnitude
        - roughness: roughness
        - roughess_model: model for the roughness, one of [None, 'erf', 'tanh', 'NC']
        - name: an optional string to use as the name of the layer
        Numerical parameters have minimum/maximum values that are going
        to be used for fitting. To input just the value, just enter a single number.
        To input the value, minimum and maximum, you should enter a 
        triplet (list,set, numpy array, etc)
        """
        self.thickness=self._to_NumericPar(thickness)
        self.nsld=self._to_NumericPar(nsld)
        self.nsldi=self._to_NumericPar(nsldi)    
        self.msld=MSLD(self._to_NumericPar(msld_rho),
                       self._to_NumericPar(msld_theta),
                       self._to_NumericPar(msld_phi))
        self.roughness=self._to_NumericPar(roughness)
        self.rougness_model=rougness_model
        if self.rougness_model not in ['erf', 'tanh', 'NC']:
            self.rougness_model=None
        self.name=name

    def _to_NumericPar(self, value):
        """
        Check if value can be converted to a NumericPar
        """
        if isinstance(value, Iterable):
            if len(value)<4:
                return_value=NumericPar(*value)
            else:
                raise ValueError("{0} cannot be converted to (value, min, max)".format(value))
        else:
            return_value=NumericPar(value)
        #The code below will raise ValueError if no floats
        return_value.value=float(return_value.value)
        if return_value.minimum!=None:
            return_value.minimum=float(return_value.minimum)
        if return_value.maximum!=None:
            return_value.maximum=float(return_value.maximum)
        return return_value     
