from __future__ import (absolute_import, division)

import numpy as np
import mantid.simpleapi as smtdi
import string


class FitModel(object):
    """
    Thin wrapper of the fitting process between a simulated and an experimental profile.
    The simulated profile accepted is one already convolved with experimental resolution.
    """

    def __init__(self, ftemplate='name=TabulatedFunction,X=($X),Y=($Y),Scaling=1,' +
                                 'ties=(Shift=0,XScaling=1);name=LinearBackground,A0=0,A1=0'):
        """
        Default constructor
        :param ftemplate: Mantid representation of the fit model, string.Template.
        Default model is a simple scaling of the (already convolved) simulated
        profile plus a linear background.
        """
        self._domain = np.empty(0, dtype=np.float64)  # undefined Q-domain
        self._profile = np.empty(0, dtype=np.float64)  # undefined intensities
        self._fitresults = None  # store results of last fit
        self.ftemplate = ftemplate

    @property
    def ftemplate(self):
        return self._ftemplate

    @ftemplate.setter
    def ftemplate(self, ftemplate):
        """
        Set internal _ftemplate string with some validation
        """
        if isinstance(ftemplate, str):
            if 'X=($X)' in ftemplate and 'Y=($Y)' in ftemplate:
                self._ftemplate = ftemplate
        else:
            raise ValueError("Invalid template function string")

    def fstr(self, fmt=".8f"):
        """
        Return model string with domain and profile substituted with some validation
        :param fmt: optional formatting specification for domain and profile elements
        """
        if self.domain.any() and self.profile.any():
            if len(self._domain) != len(self._profile):
                raise ValueError("Domain and profile of different length")
            fs = '{:'+fmt+'}'
            xseq = ','.join(fs.format(a) for a in self.domain)
            yseq = ','.join(fs.format(a) for a in self.profile)
            return string.Template(self._ftemplate).safe_substitute(X=xseq, Y=yseq)
        else:
            raise ValueError("domain and/or profile not set")

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, qdomain):
        self._domain = np.array(qdomain, dtype=np.float64)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, sprofile):
        self._profile = np.array(sprofile, dtype=np.float64)

    def doFit(self, wprofile, **fitkwargs):
        """
        Thin wrapper to mantid.simpleapi.Fit
        :param wprofile: mantid workspace holding the experimental profile
        :param fitkwargs: optional arguments for algorithm mantid.simpleapi.Fit
        :return: (type namedtuple) results of evaluating algorithm mantid.simpleapi.Fit
        """
        if not self._valid_xdomain(wprofile.dataX(0)):
            raise ValueError("Experimental Q-domain not included within the simulated Q-domain")
        self._fitresults = smtdi.Fit(Function=self.fstr(), InputWorkspace=wprofile.name(),
                                     WorkspaceIndex=0, CreateOutput=True, **fitkwargs)
        return self._fitresults

    def _valid_xdomain(self, xdomain):
        """
        Check the simulated domain includes the experimental domain
        :param xdomain: experimental domain
        :return: true if valid
        """
        if self._domain.any():
            if self._domain[0] <= xdomain[0] and self._domain[-1] >= xdomain[-1]:
                return True
        return False
