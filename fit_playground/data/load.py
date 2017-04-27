from __future__ import absolute_import, division, print_function, unicode_literals
import yaml
import gzip
import os
import math

data_dir = os.path.dirname(__file__)


def loaddata(basename):
    """
    Helper function to load gzipped yaml file.
    File *.yaml.gz must contain a dictionary with the following keys:
    (1) Qdomain
    (2) profile
    (3) errors
    (4) resolution_settings, a list where each item is a dictionary with these keys:
        (1) range: a list with Qmin and Qmax
        (2) theta
        (3) dtheta
        (4) dlambda
    :param filename:
    :return: object contained in the file
    """

    extension = '.yaml.gz'
    data_file = os.path.join(data_dir, basename+extension)
    if os.path.isfile(data_file):
        with gzip.open(data_file, 'r') as handle:
            alldata = yaml.load(handle)

    # Substitute nan in the low and high ranges with the the experimental Qmin and Qmax
    low_range = alldata["resolution_settings"][0]["range"]
    if math.isnan(low_range[0]):
        low_range[0] = alldata["Qdomain"][0]  # Qmin
    high_range = alldata["resolution_settings"][-1]["range"]  # Qmax
    if math.isnan(high_range[-1]):
        high_range[-1] = alldata["Qdomain"][-1]

    return alldata
