from __future__ import absolute_import, division, print_function, unicode_literals

import yaml
import gzip
import shutil
import os
import numpy as np

qdatfile = '/SNS/CAMM/users/jbq/development/LDRDGINS/LDRDGINS/benchmark/q.dat'
qdomain = (float(q.strip()) for q in open(qdatfile, 'r').readlines()[1:])
expfile = '/SNS/CAMM/users/jbq/development/LDRDGINS/LDRDGINS/benchmark/rexp1.dat'
I = list(l.split() for l in open(expfile, 'r').readlines()[1:])
profile = (float(i[0]) for i in I)
errors = (float(i[1]) for i in I)

experimental_data = {"Qdomain": np.array(list(qdomain)),
                     "profile": np.array(list(profile)),
                     "errors": np.array(list(errors)),
                     "resolution_settings": [{"range": [float('nan'), 0.03], "theta": 0.0068,
                                              "dtheta": 0.0003, "dlambda": 0.005},
                                             {"range": [0.03, 0.045], "theta": 0.01,
                                              "dtheta": 0.0005, "dlambda": 0.005},
                                             {"range": [0.045, float('nan')], "theta": 0.017,
                                              "dtheta": 0.0009, "dlambda": 0.005}
                                             ]
                     }

# write yaml file
with open("./SrTiO2.yaml", 'w') as yaml_file:
    yaml_file.write(yaml.dump(experimental_data))

# compress yaml file
with open('./SrTiO2.yaml', 'rb') as f_in, gzip.open('./SrTiO2.yaml.gz', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
os.remove("./SrTiO2.yaml")
