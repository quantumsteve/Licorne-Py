import numpy as np

class Mat:
    def __init__(self, size):
        self.oneone = np.zeros(size, dtype=np.complex128)
        self.onetwo = np.zeros(size, dtype=np.complex128)
        self.twoone = np.zeros(size, dtype=np.complex128)
        self.twotwo = np.zeros(size, dtype=np.complex128)

    def __len__(self):
        return len(self.oneone)

class SMat:
    def __init__(self, size):
        self.M11 = Mat(size)
        self.M12 = Mat(size)
        self.M21 = Mat(size)
        self.M22 = Mat(size)

    def __len__(self):
        return len(self.M11)

def s_moment(A, inc_moment2)
    T = inc_moment2 - A
    return np.sqrt(T)

def s_cos(A, thickness, inc_moment2):
    T = s_moment(A, inc_moment2) * thickness
    return np.cos(T)

def s_sin(A, thickness, inc_moment2):
    T = s_moment(A, inc_moment2) * thickness
    return np.sin(T)

def p_cos(A, B1, B2, B3, th, inc_moment2):
    Bmod = np.sqrt(np.square(B1) + np.square(B2) + np.square(B3))
    Out = Mat(len(inc_moment2))
    if Bmod > 0.0:
        Arg_plus = A + Bmod
        Arg_minus = A - Bmod
        F_plus = (s_cos(Arg_plus, th, inc_moment2) + s_cos(Arg_minus, th, inc_moment2)) / 2.0
        F_minus = (s_cos(Arg_plus, th, inc_moment2) - s_cos(Arg_minus, th, inc_moment2)) / (2.0 * Bmod)
        Out.oneone = F_plus + B3 * F_minus
        Out.onetwo = complex(B1, -B2) * F_minus
        Out.twoone = complex(B1, B2) * F_minus
        Out.twotwo = F_plus - B3 * F_minus
    else:
        T = s_cos(A, th, inc_moment2)
        Out.oneone = T
        Out.onetwo.fill(0.0)
        Out.twoone.fill(0.0)
        Out.twotwo = T
    return Out

def mult_mm(A, B):
    Out = Mat(len(A))
    Out.oneone = A.oneone * B.oneone + A.oneone * B.twoone
    Out.onetwo = A.oneone * B.onetwo + A.onetwo * B.twotwo
    Out.twoone = A.twoone * B.oneone + A.twotwo * B.twotwo
    Out.twotwo = A.twoone * B.onetwo + A.twotwo * B.twotwo
    return Out

def reflection(R, inc_moment, parl, sub):
    inc_moment2 = np.square(inc_moment)
    T = inc_moment2 - 4.0 * np.pi * sub

    S = SMat(len(T))
    S.M11.oneone.fill(1.0)
    S.M11.twotwo.fill(1.0)
    S.M22.oneone.fill(1.0)
    S.M22.twotwo.fill(1.0)

    psize = len(parl)

    for cur_layer in parl:
        A = 4.0 * np.pi * cur_layer.nsld
        th = cur_layer.thickness
        B1 = 4.0 * np.pi * cur_layer.msld[0]
        B2 = 4.0 * np.pi * cur_layer.msld[1]
        B3 = 4.0 * np.pi * cur_layer.msld[2]
        M = SMat(len(inc_moment2))
        M.M11 = p_cos(A, B1, B2, B3, th, inc_moment2)
        Msin = p_sin(A, B1, B2, B3, th, inc_moment2)
        M.M12 = mult_mm(pinv_moment())





