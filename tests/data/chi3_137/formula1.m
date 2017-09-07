%Enter your formula here; Input/Output variables are M, Q, Rexp, Err, Pol, An, UserData
%PARAM, dQ and Rth are only inputs. Use printout(x) function to output on the screen your variable x

%Example of Fe nuclear scattering length density (NSLD) calculation

Na=6.022e26; %Avogadro number
MolecularMass=55.85;
Density=7.874; %g/cm^3
%Coherent scattering length bc, fm:
bc=9.45;
%Absorption cross section sa, barn:
sa=2.56;
%Real part of NSLD:
ReNSLD=((Density*1e3/MolecularMass)*Na*bc*1e-15)*1e-20; %Angstrom^-2
%Imaginary part of NSLD:
ImNSLD=ReNSLD*1.27*sa*2200e-7/bc;
printout(ReNSLD);
printout(ImNSLD);
 
