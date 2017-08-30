N=100; % Number of layers
if p1>0.01
% Hyperbolic tangent
pN=p1*(N-1)/(2*(N+1));
for k=1:N
  M.Layers(k).msld(2)=180*(tanh(p2+p1*(k-(N+1)/2)/(N+1))-tanh(p2-pN))/(tanh(pN+p2)-tanh(p2-pN));
end
elseif (p1<=0.01)&(p1>=-0.01)
% Linear
for k=1:N
M.Layers(k).msld(2)=180*(k-1)/(N-1);
end
else
% Hyperbolic arctangent
x1=tanh(p1/2-p2)/2+0.5; x2=tanh(-p1/2-p2)/2+0.5;
for k=1:N
  M.Layers(k).msld(2)=(-180/(p1/2))*(atanh(2*(x1+(k-1)*(x2-x1)/(N-1))-1)+p2)/2+90;
end
end
