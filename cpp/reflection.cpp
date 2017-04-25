
#include "mersenne.cpp"

#include <cmath>
#include <complex>
#include <iostream>
#include <stdio.h>
#include <string>
#include <ctime>
#include <valarray>
#include <vector>

using namespace std;
const complex<double> I(0.0, 1.0);
double pi = M_PI;
typedef complex<double> CD;
typedef valarray<CD> VCD;
typedef long long LLONG;
struct Layer {
  double thickness;
  complex<double> nsld;
  double nsld_per;
  double msld[3];
  double msld_per[3];
  double NC;
} l;
struct PP {
  double an_vec[3];
  double pol_vec[3];
} pp;
struct Parameters {
  int mode;
  double inc_moment_lims[2];
  int inc_moment_n;
  double lambda_lims[2];
  int lambda_n;
  double out_angle_lims[2];
  int out_angle_n;
  double glance_angle;
  double maxwell;
  LLONG n_monte_carlo;
  int formalism;
  int n_of_outputs;
  int res_mode;
  vector<PP> pp;
  int pol_fun[2];
  double depth_lims[2];
  int depth_n;
  double initial_spinor[2];
  complex<double> substrate;
  complex<double> substrate2;
  double NC;
  double NC2;
  double lateral;
  double diffuse_mult;
  double norm_factor[6];
  double background;
  double percentage;
  vector<Layer> layers;
  vector<Layer> layers2;
} par;
struct Mat {
  VCD oneone;
  VCD onetwo;
  VCD twoone;
  VCD twotwo;
};
struct SMat {
  Mat M11;
  Mat M12;
  Mat M21;
  Mat M22;
};
CD sqr(CD v) { return pow(v, 2); };
CD invsqrt(CD v) { return pow(v, -0.5); };
VCD s_moment(CD A, VCD *inc_moment2) {
  VCD T = *inc_moment2 - A;
  return T.apply(sqrt);
};
VCD s_invmoment(CD A, VCD *inc_moment2) {
  VCD T = *inc_moment2 - A;
  return T.apply(invsqrt);
};
VCD s_sin(CD A, CD thickness, VCD *inc_moment2) {
  VCD T = s_moment(A, inc_moment2) * thickness;
  return T.apply(sin);
};
VCD s_cos(CD A, CD thickness, VCD *inc_moment2) {
  VCD T = s_moment(A, inc_moment2) * thickness;
  return T.apply(cos);
};
Mat p_moment(CD A, double B1, double B2, double B3, VCD *inc_moment2) {
  double Bmod = sqrt(B1 * B1 + B2 * B2 + B3 * B3);
  Mat Out;
  if (Bmod != 0) {
    CD Arg_plus = A + Bmod;
    CD Arg_minus = A - Bmod;
    VCD F_plus =
        (s_moment(Arg_plus, inc_moment2) + s_moment(Arg_minus, inc_moment2)) /
        CD(2.0);
    VCD F_minus =
        (s_moment(Arg_plus, inc_moment2) - s_moment(Arg_minus, inc_moment2)) /
        CD(2.0 * Bmod);
    Out.oneone = F_plus + CD(B3) * F_minus;
    Out.onetwo = CD(B1 - I * B2) * F_minus;
    Out.twoone = CD(B1 + I * B2) * F_minus;
    Out.twotwo = F_plus - CD(B3) * F_minus;
  } else {
    VCD T = s_moment(A, inc_moment2);
    VCD vzero(T.size());
    Out.oneone = T;
    Out.onetwo = vzero;
    Out.twoone = vzero;
    Out.twotwo = T;
  }
  return Out;
};
Mat p_invmoment(CD A, double B1, double B2, double B3, VCD *inc_moment2) {
  double Bmod = sqrt(B1 * B1 + B2 * B2 + B3 * B3);
  Mat Out;
  if (Bmod != 0) {
    CD Arg_plus = A + Bmod;
    CD Arg_minus = A - Bmod;
    VCD F_plus = (s_invmoment(Arg_plus, inc_moment2) +
                  s_invmoment(Arg_minus, inc_moment2)) /
                 CD(2.0);
    VCD F_minus = (s_invmoment(Arg_plus, inc_moment2) -
                   s_invmoment(Arg_minus, inc_moment2)) /
                  CD(2.0 * Bmod);
    Out.oneone = F_plus + CD(B3) * F_minus;
    Out.onetwo = CD(B1 - I * B2) * F_minus;
    Out.twoone = CD(B1 + I * B2) * F_minus;
    Out.twotwo = F_plus - CD(B3) * F_minus;
  } else {
    VCD T = s_invmoment(A, inc_moment2);
    VCD vzero(T.size());
    Out.oneone = T;
    Out.onetwo = vzero;
    Out.twoone = vzero;
    Out.twotwo = T;
  }
  return Out;
};
Mat p_sin(CD A, double B1, double B2, double B3, CD th, VCD *inc_moment2) {
  double Bmod = sqrt(B1 * B1 + B2 * B2 + B3 * B3);
  Mat Out;
  if (Bmod != 0) {
    CD Arg_plus = A + Bmod;
    CD Arg_minus = A - Bmod;
    VCD F_plus =
        (s_sin(Arg_plus, th, inc_moment2) + s_sin(Arg_minus, th, inc_moment2)) /
        CD(2.0);
    VCD F_minus =
        (s_sin(Arg_plus, th, inc_moment2) - s_sin(Arg_minus, th, inc_moment2)) /
        CD(2.0 * Bmod);
    Out.oneone = F_plus + CD(B3) * F_minus;
    Out.onetwo = CD(B1 - I * B2) * F_minus;
    Out.twoone = CD(B1 + I * B2) * F_minus;
    Out.twotwo = F_plus - CD(B3) * F_minus;
  } else {
    VCD T = s_sin(A, th, inc_moment2);
    VCD vzero(T.size());
    Out.oneone = T;
    Out.onetwo = vzero;
    Out.twoone = vzero;
    Out.twotwo = T;
  }
  return Out;
};
Mat p_cos(CD A, double B1, double B2, double B3, CD th, VCD *inc_moment2) {
  double Bmod = sqrt(B1 * B1 + B2 * B2 + B3 * B3);
  Mat Out;
  if (Bmod != 0) {
    CD Arg_plus = A + Bmod;
    CD Arg_minus = A - Bmod;
    VCD F_plus =
        (s_cos(Arg_plus, th, inc_moment2) + s_cos(Arg_minus, th, inc_moment2)) /
        CD(2.0);
    VCD F_minus =
        (s_cos(Arg_plus, th, inc_moment2) - s_cos(Arg_minus, th, inc_moment2)) /
        CD(2.0 * Bmod);
    Out.oneone = F_plus + CD(B3) * F_minus;
    Out.onetwo = CD(B1 - I * B2) * F_minus;
    Out.twoone = CD(B1 + I * B2) * F_minus;
    Out.twotwo = F_plus - CD(B3) * F_minus;
  } else {
    VCD T = s_cos(A, th, inc_moment2);
    VCD vzero(T.size());
    Out.oneone = T;
    Out.onetwo = vzero;
    Out.twoone = vzero;
    Out.twotwo = T;
  }
  return Out;
};
Mat mult_mm(Mat A, Mat B) {
  Mat Out;
  Out.oneone = A.oneone * B.oneone + A.onetwo * B.twoone;
  Out.onetwo = A.oneone * B.onetwo + A.onetwo * B.twotwo;
  Out.twoone = A.twoone * B.oneone + A.twotwo * B.twoone;
  Out.twotwo = A.twoone * B.onetwo + A.twotwo * B.twotwo;
  return Out;
};
Mat mult_nm(CD A, Mat B) {
  Mat Out;
  Out.oneone = A * B.oneone;
  Out.onetwo = A * B.onetwo;
  Out.twoone = A * B.twoone;
  Out.twotwo = A * B.twotwo;
  return Out;
};
Mat mult_vm(VCD A, Mat B) {
  Mat Out;
  Out.oneone = A * B.oneone;
  Out.onetwo = A * B.onetwo;
  Out.twoone = A * B.twoone;
  Out.twotwo = A * B.twotwo;
  return Out;
};
Mat plus_mm(Mat A, Mat B) {
  Mat Out;
  Out.oneone = A.oneone + B.oneone;
  Out.onetwo = A.onetwo + B.onetwo;
  Out.twoone = A.twoone + B.twoone;
  Out.twotwo = A.twotwo + B.twotwo;
  return Out;
};
Mat plus_nm(CD A, Mat B) {
  Mat Out;
  Out.oneone = A + B.oneone;
  Out.onetwo = B.onetwo;
  Out.twoone = B.twoone;
  Out.twotwo = A + B.twotwo;
  return Out;
};
Mat inv(Mat A) {
  Mat Out;
  VCD D = A.oneone * A.twotwo - A.onetwo * A.twoone;
  Out.oneone = A.twotwo / D;
  Out.onetwo = -A.onetwo / D;
  Out.twoone = -A.twoone / D;
  Out.twotwo = A.oneone / D;
  return Out;
};
SMat mult_s(SMat A, SMat B) {
  SMat Out;
  Out.M11 = plus_mm(mult_mm(A.M11, B.M11), mult_mm(A.M12, B.M21));
  Out.M12 = plus_mm(mult_mm(A.M11, B.M12), mult_mm(A.M12, B.M22));
  Out.M21 = plus_mm(mult_mm(A.M21, B.M11), mult_mm(A.M22, B.M21));
  Out.M22 = plus_mm(mult_mm(A.M21, B.M12), mult_mm(A.M22, B.M22));
  return Out;
};
VCD spin_av(Mat R, double n1[3], double n2[3], VCD pol_eff, VCD an_eff) {
  Mat Spin_dens1, Spin_dens2;
  Spin_dens1.oneone = CD(1.0) + CD(n1[2]) * pol_eff;
  Spin_dens1.onetwo = (CD(n1[0]) - I * CD(n1[1])) * pol_eff;
  Spin_dens1.twoone = (CD(n1[0]) + I * CD(n1[1])) * pol_eff;
  Spin_dens1.twotwo = CD(1.0) - CD(n1[2]) * pol_eff;
  Spin_dens2.oneone = CD(1.0) + CD(n2[2]) * an_eff;
  Spin_dens2.onetwo = (CD(n2[0]) - I * CD(n2[1])) * an_eff;
  Spin_dens2.twoone = (CD(n2[0]) + I * CD(n2[1])) * an_eff;
  Spin_dens2.twotwo = CD(1.0) - CD(n2[2]) * an_eff;
  Mat Rch, RRt;
  Rch.oneone = R.oneone.apply(conj);
  Rch.twotwo = R.twotwo.apply(conj);
  Rch.onetwo = R.twoone.apply(conj);
  Rch.twoone = R.onetwo.apply(conj);
  RRt = mult_mm(Spin_dens1, mult_mm(Rch, mult_mm(Spin_dens2, R)));
  VCD Out = (RRt.oneone + RRt.twotwo) / CD(4.0);
  return Out;
};
void reflection(Mat *R, VCD inc_moment, vector<Layer> parl, CD sub) {
  VCD inc_moment2 = inc_moment.apply(sqr);
  VCD T = inc_moment2 - 4.0 * pi * sub;
  VCD exp_arg, exp_nc;
  VCD vzero(T.size());
  VCD vone(T.size());
  vone = vzero + CD(1.0);
  VCD sub_moment = T.apply(sqrt);
  SMat S;
  S.M11.oneone = vone;
  S.M11.onetwo = vzero;
  S.M11.twoone = vzero;
  S.M11.twotwo = vone;
  S.M12.oneone = vzero;
  S.M12.onetwo = vzero;
  S.M12.twoone = vzero;
  S.M12.twotwo = vzero;
  S.M21.oneone = vzero;
  S.M21.onetwo = vzero;
  S.M21.twoone = vzero;
  S.M21.twotwo = vzero;
  S.M22.oneone = vone;
  S.M22.onetwo = vzero;
  S.M22.twoone = vzero;
  S.M22.twotwo = vone;
  CD A, A1, th;
  int psize = int(parl.size());
  SMat M;
  Mat Msin;
  double B1, B2, B3;
  for (int cur_layer = 0; cur_layer < psize; cur_layer++) {
    A = 4.0 * pi * parl[cur_layer].nsld;
    th = CD(parl[cur_layer].thickness);
    B1 = 4.0 * pi * parl[cur_layer].msld[0];
    B2 = 4.0 * pi * parl[cur_layer].msld[1];
    B3 = 4.0 * pi * parl[cur_layer].msld[2];
    M.M11 = p_cos(A, B1, B2, B3, th, &inc_moment2);
    Msin = p_sin(A, B1, B2, B3, th, &inc_moment2);
    M.M12 = mult_mm(p_invmoment(A, B1, B2, B3, &inc_moment2), Msin);
    M.M21 =
        mult_mm(mult_nm(-CD(1.0), p_moment(A, B1, B2, B3, &inc_moment2)), Msin);
    M.M22 = M.M11;
    S = mult_s(M, S);
  };
  Mat Down11 = mult_vm(I * sub_moment, S.M11);
  Mat Down12 = mult_vm(inc_moment * sub_moment, S.M12);
  Mat Down21 = mult_nm(-CD(1.0), S.M21);
  Mat Down22 = mult_vm(I * inc_moment, S.M22);
  Mat D_1 = inv(plus_mm(plus_mm(plus_mm(Down11, Down12), Down21), Down22));
  Mat Up11 = mult_vm(-I * sub_moment, S.M11);
  Mat Up12 = Down12;
  Mat Up21 = S.M21;
  Mat Up22 = Down22;
  *R = mult_mm(D_1, plus_mm(plus_mm(plus_mm(Up11, Up12), Up21), Up22));
};
void reflection_p(VCD *rpout, VCD *rmout, VCD inc_moment, vector<Layer> parl,
                  CD sub, double NCsub) {
  VCD rp(inc_moment.size());
  VCD rm(inc_moment.size());
  VCD Tp(inc_moment.size());
  VCD Tm(inc_moment.size());
  VCD Rp(inc_moment.size());
  VCD Rm(inc_moment.size());
  VCD NC(inc_moment.size());
  VCD NCp(inc_moment.size());
  VCD NCm(inc_moment.size());
  VCD p(inc_moment.size());
  VCD p1(inc_moment.size());
  VCD pp(inc_moment.size());
  VCD pm(inc_moment.size());
  VCD p1p(inc_moment.size());
  VCD p1m(inc_moment.size());
  int N = int(parl.size());
  VCD inc_moment2 = inc_moment.apply(sqr);
  VCD T = inc_moment2 - 4.0 * pi * sub;
  VCD sub_moment = T.apply(sqrt);
  if (parl[N - 1].msld[2] == 0) {
    T = inc_moment2 - 4.0 * pi * parl[N - 1].nsld;
    p1 = T.apply(sqrt);
    if (NCsub == 0.0) {
      rp = (p1 - sub_moment) / (p1 + sub_moment);
    } else {
      NC = CD(-2.0 * NCsub * NCsub) * p1 * sub_moment;
      NC = NC.apply(exp);
      rp = NC * (p1 - sub_moment) / (p1 + sub_moment);
    }
    rm = rp;
  } else {
    Tp = inc_moment2 - 4.0 * pi * (parl[N - 1].nsld + parl[N - 1].msld[2]);
    Tm = inc_moment2 - 4.0 * pi * (parl[N - 1].nsld - parl[N - 1].msld[2]);
    p1p = Tp.apply(sqrt);
    p1m = Tm.apply(sqrt);
    if (NCsub == 0.0) {
      rp = (p1p - sub_moment) / (p1p + sub_moment);
      rm = (p1m - sub_moment) / (p1m + sub_moment);
    } else {
      NCp = CD(-2.0 * NCsub * NCsub) * p1p * sub_moment;
      NCm = CD(-2.0 * NCsub * NCsub) * p1m * sub_moment;
      NCp = NCp.apply(exp);
      NCm = NCm.apply(exp);
      rp = NCp * (p1p - sub_moment) / (p1p + sub_moment);
      rm = NCp * (p1m - sub_moment) / (p1m + sub_moment);
    }
  }
  for (int cur_layer = N - 1; cur_layer >= 0; cur_layer--) {
    if (parl[cur_layer].msld[2] == 0) {
      if (cur_layer == 0) {
        T = inc_moment2 - 4.0 * pi * parl[0].nsld;
        p1 = T.apply(sqrt);
        if (parl[0].NC == 0.0) {
          Rp = (inc_moment - p1) / (inc_moment + p1);
        } else {
          NC = CD(-2.0 * parl[0].NC * parl[0].NC) * p1 * inc_moment;
          NC = NC.apply(exp);
          Rp = NC * (inc_moment - p1) / (inc_moment + p1);
        }
        Rm = Rp;
      } else {
        T = inc_moment2 - 4.0 * pi * parl[cur_layer].nsld;
        p1 = T.apply(sqrt);
        if (parl[cur_layer - 1].msld[2] == 0) {
          T = inc_moment2 - 4.0 * pi * parl[cur_layer - 1].nsld;
          p = T.apply(sqrt);
        } else {
          Tp = inc_moment2 -
               4.0 * pi *
                   (parl[cur_layer - 1].nsld + parl[cur_layer - 1].msld[2]);
          Tm = inc_moment2 -
               4.0 * pi *
                   (parl[cur_layer - 1].nsld - parl[cur_layer - 1].msld[2]);
          pp = Tp.apply(sqrt);
          pm = Tm.apply(sqrt);
        }
        if (parl[cur_layer].NC == 0.0) {
          if (parl[cur_layer - 1].msld[2] == 0) {
            Rp = (p - p1) / (p + p1);
            Rm = Rp;
          } else {
            Rp = (pp - p1) / (pp + p1);
            Rm = (pm - p1) / (pm + p1);
          }
        } else {
          if (parl[cur_layer - 1].msld[2] == 0) {
            NC = CD(-2.0 * parl[cur_layer].NC * parl[cur_layer].NC) * p1 * p;
            NC = NC.apply(exp);
            Rp = NC * (p - p1) / (p + p1);
            Rm = Rp;
          } else {
            NCp = CD(-2.0 * parl[cur_layer].NC * parl[cur_layer].NC) * p1 * pp;
            NCm = CD(-2.0 * parl[cur_layer].NC * parl[cur_layer].NC) * p1 * pm;
            NCp = NCp.apply(exp);
            NCm = NCm.apply(exp);
            Rp = NCp * (pp - p1) / (pp + p1);
            Rm = NCm * (pm - p1) / (pm + p1);
          }
        }
      }
      T = 2.0 * I * p1 * CD(parl[cur_layer].thickness);
      T = T.apply(exp);
      rp = (Rp + rp * T) / (CD(1.0) + Rp * rp * T);
      rm = (Rm + rm * T) / (CD(1.0) + Rm * rm * T);
    } else {
      if (cur_layer == 0) {
        Tp = inc_moment2 - 4.0 * pi * (parl[0].nsld + parl[0].msld[2]);
        Tm = inc_moment2 - 4.0 * pi * (parl[0].nsld - parl[0].msld[2]);
        p1p = Tp.apply(sqrt);
        p1m = Tm.apply(sqrt);
        if (parl[0].NC == 0.0) {
          Rp = (inc_moment - p1p) / (inc_moment + p1p);
          Rm = (inc_moment - p1m) / (inc_moment + p1m);
        } else {
          NCp = CD(-2.0 * parl[0].NC * parl[0].NC) * p1p * inc_moment;
          NCm = CD(-2.0 * parl[0].NC * parl[0].NC) * p1m * inc_moment;
          NCp = NCp.apply(exp);
          NCm = NCm.apply(exp);
          Rp = NCp * (inc_moment - p1p) / (inc_moment + p1p);
          Rm = NCm * (inc_moment - p1m) / (inc_moment + p1m);
        }
      } else {
        Tp = inc_moment2 -
             4.0 * pi * (parl[cur_layer].nsld + parl[cur_layer].msld[2]);
        Tm = inc_moment2 -
             4.0 * pi * (parl[cur_layer].nsld - parl[cur_layer].msld[2]);
        p1p = Tp.apply(sqrt);
        p1m = Tm.apply(sqrt);
        Tp =
            inc_moment2 -
            4.0 * pi * (parl[cur_layer - 1].nsld + parl[cur_layer - 1].msld[2]);
        Tm =
            inc_moment2 -
            4.0 * pi * (parl[cur_layer - 1].nsld - parl[cur_layer - 1].msld[2]);
        pp = Tp.apply(sqrt);
        pm = Tm.apply(sqrt);
        if (parl[cur_layer].NC == 0.0) {
          Rp = (pp - p1p) / (pp + p1p);
          Rm = (pm - p1m) / (pm + p1m);
        } else {
          NCp = CD(-2.0 * parl[cur_layer].NC * parl[cur_layer].NC) * p1p * pp;
          NCm = CD(-2.0 * parl[cur_layer].NC * parl[cur_layer].NC) * p1m * pm;
          NCp = NCp.apply(exp);
          NCm = NCm.apply(exp);
          Rp = NCp * (pp - p1p) / (pp + p1p);
          Rm = NCm * (pm - p1m) / (pm + p1m);
        }
      }
      Tp = 2.0 * I * p1p * CD(parl[cur_layer].thickness);
      Tm = 2.0 * I * p1m * CD(parl[cur_layer].thickness);
      Tp = Tp.apply(exp);
      Tm = Tm.apply(exp);
      rp = (Rp + rp * Tp) / (CD(1.0) + Rp * rp * Tp);
      rm = (Rm + rm * Tm) / (CD(1.0) + Rm * rm * Tm);
    }
  }; // end for
  *rpout = rp;
  *rmout = rm;
};
valarray<double> resolut(VCD RR, valarray<double> q, valarray<double> dq,
                         int res_mode) {
  int i, N, Nm1, k, ik;
  N = int(q.size());
  Nm1 = N - 1;
  valarray<double> denominator(N);
  valarray<double> RRr(N);
  if (res_mode == 1) {
    // left neighbours
    denominator[0] = 0.0;
    RRr[0] = 0.0;
    for (i = 1; i < N; i++) {
      denominator[i] = 0.0;
      k = 1;
      RRr[i] = 0.0;
      while (q[i] - q[i - k] <= dq[i] / 2.0) {
        denominator[i] = denominator[i] + 1;
        RRr[i] = RRr[i] + RR[i - k].real();
        k = k + 1;
        if (i - k < 0)
          break;
      }
    }
    // right neighbours and center
    denominator[N - 1] = denominator[N - 1] + 1;
    RRr[N - 1] = (RRr[N - 1] + RR[N - 1].real()) / denominator[N - 1];
    for (i = 0; i < N - 1; i++) {
      k = 1;
      denominator[i] = denominator[i] + 1;
      RRr[i] = RRr[i] + RR[i].real();
      while (q[i + k] - q[i] <= dq[i] / 2.0) {
        denominator[i] = denominator[i] + 1;
        RRr[i] = RRr[i] + RR[i + k].real();
        k = k + 1;
        if (i + k > N - 1)
          break;
      }
      RRr[i] = RRr[i] / denominator[i];
    }
  }

  if (res_mode == 2) {
    double pi_s = sqrt(2.0 * pi);
    double qq, deltaq, Rk, dqc, three_sigma, sigma_pi, sigma_sq;
    for (i = 1; i < Nm1; i++) {
      dqc = abs(q[i + 1] - q[i - 1]) / 2.0;
      if (dq[i] < dqc / 2.0)
        RRr[i] = RR[i].real();
      else {
        sigma_pi = dq[i] * pi_s;
        sigma_sq = 2.0 * dq[i] * dq[i];
        // central part
        RRr[i] = RR[i].real() * dqc / (sigma_pi);
        // left part
        k = 1;
        qq = abs(q[i] - q[i - 1]);
        deltaq = qq;
        Rk = RR[i - k].real();
        three_sigma = 3.0 * dq[i];
        while (qq <= three_sigma) {
          RRr[i] = RRr[i] + Rk * exp(-qq * qq / sigma_sq) * deltaq / sigma_pi;

          k = k + 1;
          if (i - k < 0) {
            // left tail
            deltaq = abs(q[1] - q[0]);
            qq = qq + deltaq;
            Rk = RR[0].real();
          } else {
            qq = abs(q[i] - q[i - k]);
            deltaq = abs(q[i - k + 1] - q[i - k]);
            Rk = RR[i - k].real();
          }
        }
        // right part
        k = 1;
        qq = abs(q[i + 1] - q[i]);
        deltaq = qq;
        Rk = RR[i + k].real();
        while (qq <= three_sigma) {
          RRr[i] = RRr[i] + Rk * exp(-qq * qq / sigma_sq) * deltaq / sigma_pi;
          k = k + 1;
          if (i + k > Nm1) {
            // right tail
            deltaq = abs(q[Nm1] - q[Nm1 - 1]);
            qq = qq + deltaq;
            Rk = RR[Nm1].real();
          } else {
            qq = abs(q[i + k] - q[i]);
            deltaq = abs(q[i + k] - q[i + k - 1]);
            Rk = RR[i + k].real();
          }
        }
      }
    } // end of for
    // first point
    dqc = abs(q[1] - q[0]);
    if (dq[0] < dqc / 2.0)
      RRr[0] = RR[0].real();
    else {
      sigma_pi = dq[0] * pi_s;
      sigma_sq = 2.0 * dq[0] * dq[0];
      // central part
      RRr[0] = RR[0].real() * dqc / (sigma_pi);
      // right part
      k = 1;
      qq = abs(q[1] - q[0]);
      three_sigma = 3.0 * dq[0];
      while (qq <= three_sigma) {
        RRr[0] = RRr[0] + RR[k].real() * exp(-qq * qq / sigma_sq) *
                              abs(q[k] - q[k - 1]) / sigma_pi;
        k = k + 1;
        if (k > Nm1)
          break;
        qq = abs(q[k] - q[0]);
      }
      qq = abs(q[1] - q[0]);
      deltaq = qq;
      while (qq <= three_sigma) {
        RRr[0] = RRr[0] +
                 RR[0].real() * exp(-qq * qq / sigma_sq) * deltaq / sigma_pi;
        qq = qq + deltaq;
      }
    }
    // last point
    dqc = abs(q[Nm1] - q[N - 2]);
    if (dq[Nm1] < dqc / 2.0)
      RRr[Nm1] = RR[Nm1].real();
    else {
      sigma_pi = dq[Nm1] * pi_s;
      sigma_sq = 2.0 * dq[Nm1] * dq[Nm1];
      // central part
      RRr[Nm1] = RR[Nm1].real() * dqc / (sigma_pi);
      // left part
      k = 1;
      qq = abs(q[Nm1] - q[N - 2]);
      three_sigma = 3.0 * dq[Nm1];
      while (qq <= three_sigma) {
        RRr[Nm1] = RRr[Nm1] + RR[Nm1 - k].real() * exp(-qq * qq / sigma_sq) *
                                  abs(q[Nm1 - k + 1] - q[Nm1 - k]) / sigma_pi;
        k = k + 1;
        if (Nm1 - k < 0)
          break;
        qq = abs(q[Nm1] - q[Nm1 - k]);
      }
      qq = abs(q[Nm1] - q[N - 2]);
      deltaq = qq;
      while (qq <= three_sigma) {
        RRr[Nm1] = RRr[Nm1] + RR[Nm1].real() * exp(-qq * qq / sigma_sq) *
                                  deltaq / sigma_pi;
        qq = qq + deltaq;
      }
    }
  }
  if (res_mode == 3) {
    double pi_s = sqrt(2.0 * pi);
    double qq, deltaq, Rk, dqc, three_sigma, sigma_pi, sigma_sq;
    for (i = 2; i < Nm1 - 1; i++) {
      dqc = abs(q[i + 1] - q[i - 1]) / 2.0;
      if (dq[i] < dqc / 2.0)
        RRr[i] = RR[i].real();
      else {
        sigma_pi = dq[i] * pi_s;
        sigma_sq = 2.0 * dq[i] * dq[i];
        // central part
        RRr[i] = RR[i].real() * dqc;
        // left part
        k = 1;
        qq = abs(q[i] - q[i - 1]);
        deltaq = abs(q[i] - q[i - 2]) / 2.0;
        Rk = RR[i - k].real();
        three_sigma = 3.0 * dq[i];
        while (qq <= three_sigma) {
          RRr[i] = RRr[i] + Rk * exp(-qq * qq / sigma_sq) * deltaq;
          k = k + 1;
          ik = i - k;
          if (ik < 1) {
            // left tail
            deltaq = abs(q[1] - q[0]);
            qq = qq + deltaq;
            Rk = RR[0].real();
          } else {
            qq = abs(q[i] - q[ik]);
            deltaq = abs(q[ik + 1] - q[ik - 1]) / 2.0;
            Rk = RR[i - k].real();
          }
        }
        // right part
        k = 1;
        qq = abs(q[i + 1] - q[i]);
        deltaq = abs(q[i + 2] - q[i]) / 2.0;
        Rk = RR[i + k].real();
        while (qq <= three_sigma) {
          RRr[i] = RRr[i] + Rk * exp(-qq * qq / sigma_sq) * deltaq;
          k = k + 1;
          ik = i + k;
          if (ik > Nm1 - 1) {
            // right tail
            deltaq = abs(q[Nm1] - q[Nm1 - 1]);
            qq = qq + deltaq;
            Rk = RR[Nm1].real();
          } else {
            qq = abs(q[ik] - q[i]);
            deltaq = abs(q[ik + 1] - q[ik - 1]) / 2.0;
            Rk = RR[ik].real();
          }
        }
        RRr[i] = RRr[i] / sigma_pi;
      }
    } // end of for
    // first point
    dqc = abs(q[1] - q[0]);
    if (dq[0] < dqc / 2.0)
      RRr[0] = RR[0].real();
    else {
      sigma_pi = dq[0] * pi_s;
      sigma_sq = 2.0 * dq[0] * dq[0];
      // central part
      RRr[0] = RR[0].real() * dqc / (sigma_pi);
      // right part
      k = 1;
      qq = abs(q[1] - q[0]);
      three_sigma = 3.0 * dq[0];
      while (qq <= three_sigma) {
        RRr[0] = RRr[0] + RR[k].real() * exp(-qq * qq / sigma_sq) *
                              abs(q[k + 1] - q[k - 1]) / (2.0 * sigma_pi);
        k = k + 1;
        if (k > Nm1 - 1)
          break;
        qq = abs(q[k] - q[0]);
      }
      qq = abs(q[1] - q[0]);
      deltaq = qq;
      while (qq <= three_sigma) {
        RRr[0] = RRr[0] +
                 RR[0].real() * exp(-qq * qq / sigma_sq) * deltaq / sigma_pi;
        qq = qq + deltaq;
      }
    }
    // second point
    dqc = abs(q[2] - q[0]) / 2;
    if (dq[0] < dqc / 2.0)
      RRr[0] = RR[0].real();
    else {
      sigma_pi = dq[1] * pi_s;
      sigma_sq = 2.0 * dq[1] * dq[1];
      // central part
      RRr[1] = RR[1].real() * dqc / (sigma_pi);
      // right part
      k = 2;
      qq = abs(q[2] - q[1]);
      three_sigma = 3.0 * dq[1];
      while (qq <= three_sigma) {
        RRr[1] = RRr[1] + RR[k].real() * exp(-qq * qq / sigma_sq) *
                              abs(q[k + 1] - q[k - 1]) / (2.0 * sigma_pi);
        k = k + 1;
        if (k > Nm1 - 1)
          break;
        qq = abs(q[k] - q[1]);
      }
      qq = abs(q[1] - q[0]);
      deltaq = abs(q[2] - q[0]) / 2.0;
      while (qq <= three_sigma) {
        RRr[1] = RRr[1] +
                 RR[0].real() * exp(-qq * qq / sigma_sq) * deltaq / sigma_pi;
        qq = qq + deltaq;
      }
    }
    // point before last
    dqc = abs(q[Nm1] - q[Nm1 - 2]) / 2.0;
    if (dq[Nm1 - 1] < dqc / 2.0)
      RRr[Nm1 - 1] = RR[Nm1 - 1].real();
    else {
      sigma_pi = dq[Nm1 - 1] * pi_s;
      sigma_sq = 2.0 * dq[Nm1 - 1] * dq[Nm1 - 1];
      // central part
      RRr[Nm1 - 1] = RR[Nm1 - 1].real() * dqc / (sigma_pi);
      // left part
      k = 2;
      qq = abs(q[Nm1 - 1] - q[Nm1 - 2]);
      three_sigma = 3.0 * dq[Nm1 - 1];
      while (qq <= three_sigma) {
        RRr[Nm1 - 1] = RRr[Nm1 - 1] + RR[Nm1 - k].real() *
                                          exp(-qq * qq / sigma_sq) *
                                          abs(q[Nm1 - k + 1] - q[Nm1 - k - 1]) /
                                          (2.0 * sigma_pi);
        k = k + 1;
        if (Nm1 - k < 1)
          break;
        qq = abs(q[Nm1 - 1] - q[Nm1 - k]);
      }
      qq = abs(q[Nm1] - q[Nm1 - 1]);
      deltaq = abs(q[Nm1] - q[Nm1 - 2]) / 2.0;
      while (qq <= three_sigma) {
        RRr[Nm1 - 1] = RRr[Nm1 - 1] + RR[Nm1].real() *
                                          exp(-qq * qq / sigma_sq) * deltaq /
                                          sigma_pi;
        qq = qq + deltaq;
      }
    }
    // last point
    dqc = abs(q[Nm1] - q[Nm1 - 1]);
    if (dq[Nm1] < dqc / 2.0)
      RRr[Nm1] = RR[Nm1].real();
    else {
      sigma_pi = dq[Nm1] * pi_s;
      sigma_sq = 2.0 * dq[Nm1] * dq[Nm1];
      // central part
      RRr[Nm1] = RR[Nm1].real() * dqc / (sigma_pi);
      // left part
      k = 1;
      qq = abs(q[Nm1] - q[Nm1 - 1]);
      three_sigma = 3.0 * dq[Nm1];
      while (qq <= three_sigma) {
        RRr[Nm1] = RRr[Nm1] + RR[Nm1 - k].real() * exp(-qq * qq / sigma_sq) *
                                  abs(q[Nm1 - k + 1] - q[Nm1 - k - 1]) /
                                  (2.0 * sigma_pi);
        k = k + 1;
        if (Nm1 - k < 1)
          break;
        qq = abs(q[Nm1] - q[Nm1 - k]);
      }
      qq = abs(q[Nm1] - q[Nm1 - 1]);
      deltaq = qq;
      while (qq <= three_sigma) {
        RRr[Nm1] = RRr[Nm1] + RR[Nm1].real() * exp(-qq * qq / sigma_sq) *
                                  deltaq / sigma_pi;
        qq = qq + deltaq;
      }
    }
  } // end of if res_mode
  return RRr;
};

valarray<int> monte_carlo(valarray<double> RRr, VCD inc_moment) {
  int i, N = int(RRr.size());
  LLONG LL;
  valarray<int> RRrm(N);
  RRrm = 0;
  int32 seed = (int32)time(0);
  CRandomMersenne rg(seed);
  int32 randQ;
  double randR, R_MAX;
  double twopisin = 2.0 * pi * sin(par.glance_angle);
  double maxw_sq = 2.0 * par.maxwell * par.maxwell;
  double Lambda, Lambda_sq;
  R_MAX = 1.0;
  if (par.glance_angle != 0.0) {
    valarray<double> Maxw(N);
    for (i = 0; i < N; i++) {
      Lambda = twopisin / inc_moment[i].real();
      Lambda_sq = Lambda * Lambda;
      Maxw[i] = Lambda_sq * exp(-Lambda_sq / maxw_sq);
    };
    R_MAX = Maxw.max();
    RRr = RRr * Maxw;
  }
  for (LL = 0; LL < par.n_monte_carlo; LL++) {
    randQ = rg.IRandom(0, N - 1);
    randR = rg.Random() * R_MAX;
    if (RRr[randQ] > randR) {
      RRrm[randQ] = RRrm[randQ] + 1;
    }
  };
  return RRrm;
};

int main()
// int _tmain(int argc, _TCHAR* argv[])
{
  int i, nlayers1, nlayers2;
  double dparam;
  vector<double> input;
  FILE *paramfile, *reflfile, *qfile, *reflsimfile, *polfile, *anfile;
  //struct _timeb tstruct;
  //time_t start, finish;
  //unsigned short millitm1;
  if ((paramfile = fopen("refl_par.dat", "r")) == 0)
    printf("The file 'refl_par.dat' was not opened\n");
  par.pp.push_back(pp);
  par.pp.push_back(pp);
  par.pp.push_back(pp);
  par.pp.push_back(pp);
  par.pp.push_back(pp);
  par.pp.push_back(pp);
  fscanf(paramfile, "%lg", &dparam);
  par.n_monte_carlo = LLONG(dparam);
  cout << par.n_monte_carlo;
  fscanf(paramfile, "%d", &par.formalism);
  fscanf(paramfile, "%d", &par.res_mode);
  fscanf(paramfile, "%d", &par.n_of_outputs);
  fscanf(
      paramfile,
      "%lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg",
      &par.pp[0].pol_vec[0], &par.pp[0].pol_vec[1], &par.pp[0].pol_vec[2],
      &par.pp[1].pol_vec[0], &par.pp[1].pol_vec[1], &par.pp[1].pol_vec[2],
      &par.pp[2].pol_vec[0], &par.pp[2].pol_vec[1], &par.pp[2].pol_vec[2],
      &par.pp[3].pol_vec[0], &par.pp[3].pol_vec[1], &par.pp[3].pol_vec[2],
      &par.pp[4].pol_vec[0], &par.pp[4].pol_vec[1], &par.pp[4].pol_vec[2],
      &par.pp[5].pol_vec[0], &par.pp[5].pol_vec[1], &par.pp[5].pol_vec[2]);
  fscanf(
      paramfile,
      "%lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg %lg",
      &par.pp[0].an_vec[0], &par.pp[0].an_vec[1], &par.pp[0].an_vec[2],
      &par.pp[1].an_vec[0], &par.pp[1].an_vec[1], &par.pp[1].an_vec[2],
      &par.pp[2].an_vec[0], &par.pp[2].an_vec[1], &par.pp[2].an_vec[2],
      &par.pp[3].an_vec[0], &par.pp[3].an_vec[1], &par.pp[3].an_vec[2],
      &par.pp[4].an_vec[0], &par.pp[4].an_vec[1], &par.pp[4].an_vec[2],
      &par.pp[5].an_vec[0], &par.pp[5].an_vec[1], &par.pp[5].an_vec[2]);
  fscanf(paramfile, "%d %d", &par.pol_fun[0], &par.pol_fun[1]);
  fscanf(paramfile, "%lg %lg %lg %lg %lg %lg", &par.norm_factor[0],
         &par.norm_factor[1], &par.norm_factor[2], &par.norm_factor[3],
         &par.norm_factor[4], &par.norm_factor[5]);
  fscanf(paramfile, "%lg", &par.maxwell);
  fscanf(paramfile, "%lg", &par.glance_angle);
  fscanf(paramfile, "%lg", &par.background);
  fscanf(paramfile, "%lg", &par.percentage);
  fscanf(paramfile, "%d", &nlayers1);
  fscanf(paramfile, "%lg", &dparam);
  par.substrate.real(dparam);
  fscanf(paramfile, "%lg", &dparam);
  par.substrate.imag(dparam);
  fscanf(paramfile, "%lg", &par.NC);
  for (i = 0; i < nlayers1; i++) {
    fscanf(paramfile, "%lg", &dparam);
    l.thickness = dparam;
    fscanf(paramfile, "%lg", &dparam);
    l.nsld.real(dparam);
    fscanf(paramfile, "%lg", &dparam);
    l.nsld.imag(dparam);
    //	fscanf(paramfile,"%lg",&l.nsld_per);
    fscanf(paramfile, "%lg", &l.msld[0]);
    fscanf(paramfile, "%lg", &l.msld[1]);
    fscanf(paramfile, "%lg", &l.msld[2]);
    //	fscanf(paramfile,"%lg",&l.msld_per[0]);fscanf(paramfile,"%lg",&l.msld_per[1]);fscanf(paramfile,"%lg",&l.msld_per[2]);
    fscanf(paramfile, "%lg", &dparam);
    l.NC = dparam;
    par.layers.push_back(l);
  }
  if ((par.percentage < 100.0) & (par.percentage > 0.0)) {
    fscanf(paramfile, "%d", &nlayers2);
    fscanf(paramfile, "%lg", &dparam);
    par.substrate2.real(dparam);
    fscanf(paramfile, "%lg", &dparam);
    par.substrate2.imag(dparam);
    fscanf(paramfile, "%lg", &par.NC2);
    for (i = 0; i < nlayers2; i++) {
      fscanf(paramfile, "%lg", &dparam);
      l.thickness = dparam;
      fscanf(paramfile, "%lg", &dparam);
      l.nsld.real(dparam);
      fscanf(paramfile, "%lg", &dparam);
      l.nsld.imag(dparam);
      //	fscanf(paramfile,"%lg",&l.nsld_per);
      fscanf(paramfile, "%lg", &l.msld[0]);
      fscanf(paramfile, "%lg", &l.msld[1]);
      fscanf(paramfile, "%lg", &l.msld[2]);
      //	fscanf(paramfile,"%lg",&l.msld_per[0]);fscanf(paramfile,"%lg",&l.msld_per[1]);fscanf(paramfile,"%lg",&l.msld_per[2]);
      fscanf(paramfile, "%lg", &dparam);
      l.NC = dparam;
      par.layers2.push_back(l);
    }
  }
  if (paramfile)
    fclose(paramfile);
  if ((qfile = fopen("refl_q_dq.dat", "r")) == NULL)
    printf("The file 'refl_q_dq.dat' was not opened\n");
  vector<double> q_vec, dq_vec;
  double qinput;
  while ((fscanf(qfile, "%lg", &qinput)) != EOF) {
    q_vec.push_back(qinput);
    fscanf(qfile, "%lg", &qinput);
    dq_vec.push_back(qinput);
  }
  if (qfile)
    fclose(qfile);
  VCD pol_eff(q_vec.size()), an_eff(q_vec.size());
  if (par.pol_fun[0] == 1) {
    if ((polfile = fopen("pol.dat", "r")) == NULL)
      printf("The file 'pol.dat' was not opened\n");
    double pol_input;
    int k1 = 0;
    while ((fscanf(polfile, "%lg", &pol_input)) != EOF) {
      pol_eff[k1] = CD(pol_input);
      k1 = k1 + 1;
    }
    if (polfile)
      fclose(polfile);
  } else {
    pol_eff = CD(1.0);
  }
  if (par.pol_fun[1] == 1) {
    if ((anfile = fopen("an.dat", "r")) == NULL)
      printf("The file 'an.dat' was not opened\n");
    double an_input;
    int k2 = 0;
    while ((fscanf(anfile, "%lg", &an_input)) != EOF) {
      an_eff[k2] = CD(an_input);
      k2 = k2 + 1;
    }
    if (anfile)
      fclose(anfile);
  } else {
    an_eff = CD(1.0);
  }
  valarray<double> q(q_vec.size()), dq(dq_vec.size());
  VCD inc_moment(q_vec.size());
  VCD vzero(q_vec.size());
  for (i = 0; i < int(q_vec.size()); i++) {
    q[i] = q_vec[i];
    dq[i] = dq_vec[i];
    inc_moment[i] = CD(q[i] / 2.0);
  }
  //time(&start);
  //_ftime64_s(&tstruct);
  //millitm1 = tstruct.millitm;
  Mat R, R2;
  VCD RparrP, RparrM, Rparr2P, Rparr2M;
  if (par.formalism == 1) {
    reflection(&R, inc_moment, par.layers, par.substrate);
    if ((par.percentage < 100.0) & (par.percentage > 0.0)) {
      reflection(&R2, inc_moment, par.layers2, par.substrate2);
    }
  } else {
    if (par.formalism == 0) {
      reflection_p(&RparrP, &RparrM, inc_moment, par.layers, par.substrate,
                   par.NC);
      R.oneone = RparrP;
      R.twotwo = RparrM;
      R.onetwo = vzero;
      R.twoone = vzero;
      if ((par.percentage < 100.0) & (par.percentage > 0.0)) {
        reflection_p(&Rparr2P, &Rparr2M, inc_moment, par.layers, par.substrate,
                     par.NC);
        R2.oneone = RparrP;
        R2.twotwo = RparrM;
        R2.onetwo = vzero;
        R2.twoone = vzero;
      }
    }
  }

  //_ftime64_s(&tstruct);
  //time(&finish);
  //cout << "elapsed time:" << difftime(finish, start) << "s"
  //     << tstruct.millitm - millitm1;
  VCD RR, RR2;
  valarray<double> RRr;
  valarray<int> RRrm;
  char s[10];
  char ss[14];
  for (int k = 0; k < par.n_of_outputs; k++) {
    RR = spin_av(R, par.pp[k].pol_vec, par.pp[k].an_vec, pol_eff, an_eff);
    if ((par.percentage < 100.0) & (par.percentage > 0.0)) {
      RR2 = spin_av(R2, par.pp[k].pol_vec, par.pp[k].an_vec, pol_eff, an_eff);
      RR = CD(par.percentage / 100.0) * RR +
           CD(1.0 - par.percentage / 100.0) * RR2;
    }
    RRr = resolut(RR, q, dq, par.res_mode);
    RRr = RRr * par.norm_factor[k] + par.background;
    s[0] = 'r';
    s[1] = 'e';
    s[2] = 'f';
    s[3] = 'l';
    s[4] = char(k + 49);
    s[5] = '.';
    s[6] = 'd';
    s[7] = 'a';
    s[8] = 't';
    s[9] = '\0';
    reflfile = fopen(s, "w");
    for (i = 0; i < int(RRr.size()); i++) {
      fprintf(reflfile, "%lg\n", RRr[i]);
    };
    fclose(reflfile);
    if (par.n_monte_carlo > 0) {
      RRrm = monte_carlo(RRr, inc_moment);
      ss[0] = 'r';
      ss[1] = 'e';
      ss[2] = 'f';
      ss[3] = 'l';
      ss[4] = '_';
      ss[5] = 's';
      ss[6] = 'i';
      ss[7] = 'm';
      ss[8] = char(k + 49);
      ss[9] = '.';
      ss[10] = 'd';
      ss[11] = 'a';
      ss[12] = 't';
      ss[13] = '\0';
      reflsimfile = fopen(ss, "w");
      for (i = 0; i < int(RRrm.size()); i++) {
        fprintf(reflsimfile, "%d\n", RRrm[i]);
      };
      fclose(reflsimfile);
    }
  }
};
