clear;clc;close all;

C1 = 43e-9;
C2 = 5;
C3 = 2;
C4 = 1;

DD = @(t) C1.*exp(-t.^C2/C3).*t.^C4;

tau1 = 1/5;
tau2 = 1;
DAP = @(t) (exp(-t ./ tau2) - exp(-t ./ tau1));
taue = 0.5;
expsyn = @(t) exp(-t/taue);

alpha = 50;
tau = 10;
IW = @(t) (t./tau).*exp(-alpha.*t./tau);

t = linspace(0,50,1000);
delay = 0.25;
figure();
DDT = DD(t);
DAPT = DAP(t);
ET = expsyn(t);
IWT = IW(t);
plot(t,DDT./max(DDT),'b-');
hold on;
plot(t+delay,ET./max(ET),'r-');
xlim([0,15]);
plot(t,IWT./max(IWT),'g-');