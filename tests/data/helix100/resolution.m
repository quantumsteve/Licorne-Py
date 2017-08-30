Lambda=5;
DLambda=0.01;
Theta=asin(Q*Lambda/(4*pi));
DTheta=Q*0;
DTheta(Q>0)=0.0007;
Sigma=Q.*sqrt((DTheta./Theta).^2+(DLambda/Lambda)^2);
