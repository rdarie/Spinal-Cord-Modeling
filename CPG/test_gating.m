clear;clc;close all;

v1 = linspace(-100, 100, 1e3);

hpinf  = 1 ./ ( 1 + exp( ( v1 + 59 ) ./ 8 ) );
hptau = 1200./ cosh(( v1 + 59 )./16);

ninf = 1 ./ (1 + exp(-(v1+28)./15));
ntau = 7 ./ (exp((v1+40)./40) + exp(-(v1+40)./50));

mpinf  = 1 ./ ( 1 + exp( - ( v1 + 47.1 ) ./ 3.1 ) );

hinf = 1 ./ (1 + exp((v1+55)./7));
htau = 30 ./ (exp((v1+50)./15) + exp(-(v1+50)./16));

minf = 1 ./ ( 1 + exp(-(v1+35)./7.8) );