from __future__ import absolute_import, division

import pytest
from tests.data.load import loaddata
import licorne.model as model
from licorne.resolution import Resolution
import numpy as np
import re
import mantid.simpleapi as smtdi


def find_range_indexes(qdomain, qmin, qmax):
    """
    Find first index in sequence qdomain corresponding to element bigger than qmin
    and last index corresponding to element smaller than qmax
    :param qdomain: array of momentum transfer values
    :param qmin: minimum momentum transfer
    :param qmax: maximum momentum transfer
    :return: pair of indexes
    """
    range_indexes = np.intersect1d(np.where(qdomain >= qmin), np.where(qdomain <= qmax))
    return range_indexes[0], range_indexes[-1]


def test_domain():
    fm = model.FitModel()
    fm.domain = range(2)
    assert fm._domain.dtype == np.dtype('float64')


def test_fstr():
    fm = model.FitModel(ftemplate='X=($X),Y=($Y)')
    fm.domain, fm.profile = range(2), range(3)
    with pytest.raises(ValueError):
        fm.fstr()
    fm.profile = range(2)
    output = ['0.00000000', '1.00000000', '0.00000000', '1.00000000']
    assert re.findall('\d+\.\d+', fm.fstr()) == output


def test_validateDomain():
    fm = model.FitModel()
    fm.domain = range(1, 3)
    for xdomain, valid in zip([range(1, 3), range(3), range(1, 4)], [True, False, False]):
        assert fm._valid_xdomain(xdomain) == valid


def test_fit():
    alldata = loaddata("SrTiO2")
    xdom, xprof, xerr = list(alldata[k] for k in ['Qdomain', 'profile', 'errors'])

    # Fit each chunk independently
    for rs in alldata['resolution_settings']:
        keys = ('range', 'theta', 'dtheta', 'dlambda')
        [qmin, qmax], th, dth, dl = list(rs[k] for k in keys)
        i_min, i_max = find_range_indexes(xdom, qmin, qmax)

        # Current chunk
        qs, pf, err = list(domain[i_min: i_max] for domain in (xdom, xprof, xerr))

        # Convolve with resolution, then rescale and add a linear background.
        # pfx will do as the experimental profile
        res = Resolution(th, dth, dl)
        pfx, err = list(10.0*x for x in (res.convolve_with(qs, pf), err))
        intercept, slope = 0.05*np.average(pfx), 0.05*np.std(pfx)/(qmax-qmin)
        pfx += slope*qs + intercept

        # Simulated profile is noisy pf. Convolve with resolution prior to fitting
        pfs = pf * np.random.uniform(low=0.9, high=1.1, size=len(pf))
        fm = model.FitModel()
        fm.domain, fm.profile = qs, res.convolve_with(qs, pfs)

        ws = smtdi.CreateWorkspace(qs, pfx, err, NSpec=1, UnitX='MomentumTransfer')
        fit_results = fm.doFit(ws, StartX=qs[1], EndX=qs[-2])  # avoid end-effects
        assert fit_results[1] < 1.0  # Chi2 smaller than one
        smtdi.DeleteWorkspace(ws)
