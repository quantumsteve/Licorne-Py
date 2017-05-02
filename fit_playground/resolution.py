from __future__ import (absolute_import, division)

from collections import namedtuple
import numpy as np

"""
    Instrument settings defining a resolution function
    :param theta: scattering angle for the reflection
    :param dtheta: error in theta
    :param dlambda: width of incoming pulse
"""
rsetting = namedtuple('rsetting', ['theta', 'dtheta', 'dlambda'])


class Resolution(object):
    """
    A Gaussian with a Q-dependent standard deviation
    """
    def __init__(self, *args):
        """
        Overloaded constructor
        :param args: either an rsetting object or a 'theta', 'dtheta', 'dlambda' list,
        in this order
        """
        if len(args) == 1 and isinstance(args[0], rsetting):
            self._settings = args[0]
        elif len(args) == 3:
            settings = rsetting(*args)
            self._settings = settings

    def __getattr__(self, key):
        """ Getter for exposing attributes of self._settings """
        if key == '_settings':
            return self.__dict__[key]
        else:
            if hasattr(self._settings, key):
                return getattr(self._settings, key)
            else:
                return self.__dict__[key]

    def __setattr__(self, key, value):
        """ Setter for exposed attributes of self._settings """
        if key == '_settings':
            self.__dict__[key] = value
        else:
            if hasattr(self._settings, key):
                setattr(self._settings, key, value)
            else:
                self.__dict__[key] = value

    def lambdas(self, qs):
        """
        Wavelength of the reflected neutron for the input momemtun transfers
        :param qs: array of momentum transfer values
        :return: array of wavelengths, in Angstroms
        """
        return 4*np.pi*np.sin(self.theta) / qs

    def sigmas(self, qs):
        """
        Width of the resolution as a function of Q
        :param qs: array of Q values where to evaluate the width of the resolution
        :return: array of widths
        """
        return qs * np.sqrt((self.dtheta/self.theta) ** 2 + (self.dlambda/self.lambdas(qs))**2)

    def evaluate(self, qs, qdomain):
        """
        Evaluation of the resolution function in a Q-domain for different widths
        :param qs: array of Q values where to center the resolution and find their widths
        :param qdomain: integration range for the convolution
        :return: 2D-array with shape=(len(qs), len(qdomain)) containing evaluation of the
        resolution over the Q-domain centered at the different qs.
        """
        qq = np.add.outer(-qs, qdomain)/self.sigmas(qs)[:, None]
        return np.exp(-0.5*qq**2)

    def __call__(self, qs, qdomain):
        """Fancy make it a callable"""
        return self.evaluate(qs, qdomain)

    def convolve_with(self, qdomain, profile):
        """
        Convolves the resolution with a profile over a Q-domain.
        1. No normalization
        2. No treatment of edge effects
        3. No multiplication by bin widths of qdomain
        :param profile: array of specular intensities
        :param qdomain: array of Q values for the profile array
        :return: convolution evaluated at the Q-domain values
        """
        # Check that profile and qdomain have compatible sizes
        if len(qdomain)-len(profile) not in (0, 1):
            raise ValueError("Q-domain and Intensity profile have incompatible sizes")

        # Bins for Q-domain. Check if histogram or point data
        qbins = qdomain[1:] - qdomain[:-1]
        if len(qdomain) == len(profile):
            qbins = np.concatenate(([qbins[0]], (qbins[1:]+qbins[:-1])/2., [qbins[-1]]))

        # convolution creates a 1D array of size len(Qdomain)
        rev = self.evaluate(qdomain, qdomain)  # rev.shape = (len(qdomain), len(qdomain))
        return np.inner(rev, qbins*profile) / np.inner(rev, qbins)  # normalized
