import numpy as np

class SMat:
    def __init__(self, size):
        self.M11 = Mat(size)
        self.M12 = Mat(size)
        self.M21 = Mat(size)
        self.M22 = Mat(size)

    def __len__(self):
        return len(self.M11)

class Layer:
    self.thickness
    self.nsld
    self.msld
    self.NC

paramfile = open('refl_par.dat','r')
n_monte_carlo = int(paramfile.readline())
formalism = int(paramfile.readline())
res_mode = paramfile.readline()
n_of_outputs = float(paramfile.readline())

pol_vecs = np.array([float(value) for value in paramfile.readline().split()]).reshape(6,3)
an_vecs = np.array([float(value) for value in paramfile.readline().split()]).reshape(6,3)

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
with open('refl_q_dq.dat','r') as qfile:
    for line in qfile:
        tmp = [float(value) for value in line.split()]
        q.append(tmp[0])
        dq.append(tmp[1])
qfile.close()
inc_moment = q / 2.0

pol_eff = np.ones(len(q), dtype=np.complex128)
an_eff = np.ones(len(q), dtype=np.complex128)

reflection(R, inc_moment, par.layers, par.substrate)
for k in range(n_of_outputs):
    RR = spin_av(R, pol_vec[k], an_vec[k], pol_eff, an_eff)
    RRr = resolut(RR, q, dq, res_mode)
    RRr = RRr * norm_factor[k] + background

    reflfile = open('refl'+str(k+1)+'.dat', 'w')
    for value in RRr:
        reflfile.write(value)
    reflfile.close()
