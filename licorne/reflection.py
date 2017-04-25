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

def p_sin(A, B1, B2, B3, th, inc_moment2):
    Bmod = np.sqrt(np.square(B1) + np.square(B2) + np.square(B3))
    Out = Mat(len(inc_moment2))
    if Bmod > 0.0:
        Arg_plus = A + Bmod
        Arg_minus = A - Bmod
        F_plus = (s_sin(Arg_plus, th, inc_moment2) + s_sin(Arg_minus, th, inc_moment2)) / 2.0
        F_minus = (s_sin(Arg_plus, th, inc_moment2) - s_sin(Arg_minus, th, inc_moment2)) / (2.0 * Bmod)
        Out.oneone = F_plus + B3 * F_minus
        Out.onetwo = complex(B1, -B2) * F_minus
        Out.twoone = complex(B1, B2) * F_minus
        Out.twotwo = F_plus - B3 * F_minus
    else:
        T = s_sin(A, th, inc_moment2)
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

def mult_nm(A, B):
    Out = Mat(len(B))
    Out.oneone = A * B.oneone
    Out.onetwo = A * B.onetwo
    Out.twoone = A * B.oneone
    Out.twotwo = A * B.onetwo
    return Out

def s_invmoment(A, inc_moment2):
    T = inc_moment2 - A
    T.sqrt()
    T.reciprocal()
    return T

def p_moment(A, B1, B2, B3, inc_moment2):
    Bmod = np.sqrt(np.square(B1) + np.square(B2) + np.square(B3))
    Out = Mat(len(inc_moment2))
    if Bmod > 0.0:
        Arg_plus = A + Bmod
        Arg_minus = A - Bmod
        F_plus = (s_moment(Arg_plus, inc_moment2) + s_moment(Arg_minus, inc_moment2)) / 2.0
        F_minus = (s_moment(Arg_plus, inc_moment2) - s_moment(Arg_minus, inc_moment2)) / (2.0 * Bmod)
        Out.oneone = F_plus + B3 * F_minus
        Out.onetwo = complex(B1, -B2) * F_minus
        Out.twoone = complex(B1, B2) * F_minus
        Out.twotwo = F_plus - B3 * F_minus
    else:
        T = s_moment(A, inc_moment2)
        Out.oneone = T
        Out.onetwo.fill(0.0)
        Out.twoone.fill(0.0)
        Out.twotwo = T
    return Out

def p_invmoment(A, B1, B2, B3, inc_moment2):
    Bmod = np.sqrt(np.square(B1) + np.square(B2) + np.square(B3))
    Out = Mat(len(inc_moment2))
    if Bmod > 0.0:
        Arg_plus = A + Bmod
        Arg_minus = A - Bmod
        F_plus = (s_invmoment(Arg_plus, inc_moment2) + s_invmoment(Arg_minus, inc_moment2)) / 2.0
        F_minus = (s_invmoment(Arg_plus, inc_moment2) - s_invmoment(Arg_minus, inc_moment2)) / (2.0 * Bmod)
        Out.oneone = F_plus + B3 * F_minus
        Out.onetwo = complex(B1, -B2) * F_minus
        Out.twoone = complex(B1, B2) * F_minus
        Out.twotwo = F_plus - B3 * F_minus
    else:
        T = s_invmoment(A, inc_moment2)
        Out.oneone = T
        Out.onetwo.fill(0.0)
        Out.twoone.fill(0.0)
        Out.twotwo = T
    return Out


def plus_mm(A, B):
    Out = Mat(len(A))
    Out.oneone = A.oneone + B.oneone
    Out.onetwo = A.onetwo + B.onetwo
    Out.twoone = A.twoone + B.twoone
    Out.twotwo = A.twotwo + B.twotwo
    return Out

def mult_s(A, B):
    Out = SMat(len(A))
    Out.M11 = plus_mm(mult_mm(A.M11, B.M11), mult_mm(A.M12, B.M21))
    Out.M12 = plus_mm(mult_mm(A.M11, B.M12), mult_mm(A.M12, B.M22))
    Out.M21 = plus_mm(mult_mm(A.M21, B.M11), mult_mm(A.M22, B.M21))
    Out.M22 = plus_mm(mult_mm(A.M21, B.M12), mult_mm(A.M22, B.M22))
    return Out

def mult_vm(A, B):
    Out = Mat(len(B))
    Out.oneone = A * B.oneone
    Out.onetwo = A * B.onetwo
    Out.twoone = A * B.twoone
    Out.twotwo = A * B.twotwo

def inv(A)
    Out = Mat(len(A))
    D = A.oneone * A.twotwo - A.onetwo * A.twone
    Out.oneone = A.twotwo / D
    Out.onetwo = -1.0 * A.onetwo / D
    Out.twoone = -1.0 * A.twoone / D
    Out.twotwo = A.oneone / D
    return Out



def reflection(inc_moment, parl, sub):
    inc_moment2 = np.square(inc_moment)
    T = inc_moment2 - 4.0 * np.pi * sub
    sub_moment = np.sqrt(T)
    S = SMat(len(T))
    S.M11.oneone.fill(1.0)
    S.M11.twotwo.fill(1.0)
    S.M22.oneone.fill(1.0)
    S.M22.twotwo.fill(1.0)
    for cur_layer in parl:
        A = 4.0 * np.pi * cur_layer.nsld
        th = cur_layer.thickness
        B1 = 4.0 * np.pi * cur_layer.msld[0]
        B2 = 4.0 * np.pi * cur_layer.msld[1]
        B3 = 4.0 * np.pi * cur_layer.msld[2]
        M = SMat(len(inc_moment2))
        M.M11 = p_cos(A, B1, B2, B3, th, inc_moment2)
        Msin = p_sin(A, B1, B2, B3, th, inc_moment2)
        M.M12 = mult_mm(p_invmoment(A, B1, B2, B3, inc_moment2), Msin)
        M.M21 = mult_mm(mult_nm(complex(-1.0,0.0), p_moment(A, B1, B2, B3, inc_moment2)), Msin)
        M.M22 = np.copy(M.M11)
        S = mult_s(M, S)
    Down11 = mult_vm(complex(0.0,1.0) * sub_moment, S.M11)
    Down12 = mult_vm(inc_moment * sub_moment, S.M12)
    Down21 = mult_nm(complex(-1.0,0.0), S.M21)
    Down22 = mult_vm(complex(0.0,1.0)*inc_moment, S.M22)
    D_1 = inv(plus_mm(plus_mm(plus_mm(Down11, Down12), Down21), Down22))
    Up11 = mult_vm(complex(0.0,-1.0) * sub_moment, S.M11)
    Up12 = np.copy(Down12)
    Up21 = np.copy(S.M21)
    Up22 = np.copy(Down22)
    R = mult_mm(D_1, plus_mm(plus_mm(plus_mm(Up11, Up12), Up21), Up22))
    return R

def spin_av(R, n1, n2, pol_eff, an_eff):
    I = complex(0.0, 1.0)
    Spin_dens1 = Mat(len(pol_eff))
    Spin_dens1.oneone = 1.0 + n1[2] * pol_eff
    Spin_dens1.onetwo = (n1[0] - I * n1[1]) * pol_eff
    Spin_dens1.twoone = (n1[0] + I * n1[1]) * pol_eff
    Spin_dens1.twotwo = 1.0 - n1[2] * pol_eff
    Spin_dens2 = Mat(len(an_eff))
    Spin_dens2.oneone = 1.0 + n2[2] * an_eff
    Spin_dens2.onetwo = (n2[0] - I * n2[1]) * an_eff
    Spin_dens2.twoone = (n2[0] + I * n2[1]) * an_eff
    Spin_dens2.twotwo = 1.0 - n2[2] * an_eff

    Rch = Mat(len(R))
    Rch.oneone = np.conj(R.oneone)
    Rch.twotwo = np.conj(R.twotwo)
    Rch.onetwo = np.conj(R.twoone)
    Rch.twoone = np.conj(R.onetwo)
    RRt = mult_mm(Spin_dens1, mult_mm(Rch, mult_mm(Spin_dens2, R)))
    Out = (RRt.oneone + RRt.twotwo) / 4.0
    return Out

def resolut(RR, q, dq):
    N = len(q)
    Nm1 = N - 1
    denominator = np.zeros(N)
    RRr = np.zeros(N)
    pi_s = np.sqrt(2.0 * np.pi)

    for i in range(1, Nm1):
        dqc = np.abs(q[i + 1] - q[i - 1]) / 2.0
        if dq[i] < dqc / 2.0:
            RRr[i] = RR[i].real
        else:
            sigma_pi = dq[i] * pi_s
            sigma_sq = 2.0 * np.square(dq[i])
            # central part
            RRr[i] = RR[i].real * dqc / sigma_pi
            # left part
            k = 1
            qq = np.abs(q[i] - q[i - 1])
            deltaq = qq
            Rk = RR[i - k].real
            three_sigma = 3.0 * dq[i]
            while qq <= three_sigma:
                RRr[i] = RRr[i] + Rk * np.exp(-1.0 * np.square(qq * qq) / sigma_sq) * deltaq / sigma_pi
                k = k + 1
                if i - k < 0:
                    #left tail
                    deltaq = abs(q[1] - q[0])
                    qq = qq + deltaq
                    Rk = RR[0].real
                else:
                    qq = abs(q[i] - q[i - k])
                    deltaq = abs(q[i - k + 1] - q[i - k])
                    Rk = RR[i - k].real
            # right part
            k = 1
            qq = np.abs(q[i + 1] - q[i])
            deltaq = qq
            Rk = RR[i + k].real
            while qq <= three_sigma:
                RRr[i] = RRr[i] + Rk * np.exp(-1.0 * np.square(qq) / sigma_sq) * deltaq / sigma_pi
                k = k + 1
                if i + k > Nm1:
                    # right tail
                    deltaq = abs(q[Nm1] - q[Nm1 - 1])
                    qq = qq + deltaq
                    Rk = RR[Nm1].real
                else:
                    qq = np.abs(q[i + k] - q[i])
                    deltaq = np.abs(q[i + k] - q[i + k - 1])
                    Rk = RR[i + k].real

    # first point
    dqc = np.abs(q[1] - q[0])
    if dq[0] < dqc / 2.0:
        RRr[0] = RR[0].real
    else:
        sigma_pi = dq[0] * pi_s
        sigma_sq = 2.0 * dq[0] * dq[0]
        # central part
        RRr[0] = RR[0].real * dqc / (sigma_pi)
        # right part
        k = 1
        qq = abs(q[1] - q[0])
        three_sigma = 3.0 * dq[0]
        while qq <= three_sigma:
            RRr[0] = RRr[0] + RR[k].real * np.exp(-qq * qq / sigma_sq) * np.abs(q[k] - q[k - 1]) / sigma_pi
            k = k + 1
            if k > Nm1:
                break
            qq = np.abs(q[k] - q[0])
        qq = abs(q[1] - q[0])
        deltaq = qq
        while qq <= three_sigma:
            RRr[0] = RRr[0] + RR[0].real * np.exp(-1.0 * np.square(qq) / sigma_sq) * deltaq / sigma_pi
            qq = qq + deltaq

    # last point
    dqc = abs(q[Nm1] - q[N - 2])
    if dq[Nm1] < dqc / 2.0:
        RRr[Nm1] = RR[Nm1].real
    else:
        sigma_pi = dq[Nm1] * pi_s
        sigma_sq = 2.0 * dq[Nm1] * dq[Nm1]
        # central part
        RRr[Nm1] = RR[Nm1].real * dqc / sigma_pi
        # left part
        k = 1
        qq = abs(q[Nm1] - q[N - 2])
        three_sigma = 3.0 * dq[Nm1]
        while qq <= three_sigma:
            RRr[Nm1] = RRr[Nm1] + RR[Nm1 - k].real * np.exp(-qq * qq / sigma_sq) * np.abs(q[Nm1 - k + 1] - q[Nm1 - k]) / sigma_pi
            k = k + 1
            if Nm1 - k < 0:
                break
            qq = np.abs(q[Nm1] - q[Nm1 - k])
        qq = abs(q[Nm1] - q[N - 2])
        deltaq = qq
        while qq <= three_sigma:
            RRr[Nm1] = RRr[Nm1] + RR[Nm1].real * np.exp(-1.0 * np.square(qq) / sigma_sq) * deltaq / sigma_pi
            qq = qq + deltaq
    return RRr
