import os,copy
import numpy as np

R_reference = []
with open(os.path.join(os.path.dirname(__file__), '../helix100_reflection_result.txt'), 'r') as f:
    for line in f:
        tmp = []
        for value in line.strip().split('\t'):
            number = value.split(' ')
            #print(number)
            if 'E' not in number[0]:
                real = float(number[0])
            else:
                meow = number[0].split('E')
                real = float(meow[0]) * 10 ** int(meow[1])
            if number[1] == '-':
                if 'E' not in number[2]:
                    imaginary = -1.0*float(copy.deepcopy(number[2])[0:-2])
                else:
                    meow = number[2].split('E')
                    print(number[2],meow)
                    imaginary = -1.0*float(meow[0])*10**float(copy.deepcopy(meow[1])[0:-2])
            else:
                if 'E' not in number[2]:
                    imaginary = float(copy.deepcopy(number[2])[0:-2])
                else:
                    meow = number[2][0:-2].split('E')
                    imaginary = float(meow[0])*10**float(meow[1])
            tmp.append(complex(real,imaginary))
        R_reference.append(tmp)
R_reference = np.array(R_reference)
np.savetxt('meow.txt',R_reference)
