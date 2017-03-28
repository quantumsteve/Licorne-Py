from collections import namedtuple

MSLD=namedtuple('MSLD',['rho','theta','phi'])

class Layer(object):
    def __init__(self,thickness=1.,nsld=1.,msld=MSLD(rho=0.,theta=0.,phi=0.)):
        self.thickness=thickness
        self.nsld=nsld
        self.msld=msld
    def __str__(self):
        strrep  = '  - thickness={0}\n'.format(self.thickness)
        strrep += '  - nsld={0}\n'.format(self.nsld)
        strrep += '  - msld rho={0} theta={1} phi={2}'.format(self.msld.rho, self.msld.theta, self.msld.phi)
        return strrep


if __name__=='__main__':
    sample=[Layer(),Layer(thickness=2.),Layer(nsld=2.)]
    for i,l in enumerate(sample):
        print('Layer {0}'.format(i))
        print(l)

