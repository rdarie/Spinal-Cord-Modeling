clear;clc; close all;

vm = [10 0 -10 -20];
ina = [-1.41 -2.01 -2.78 -3.51];
ik = [1.52 1.08 0.6 0.25];

vna = vm - 50;
vk = vm + 77.5;

% Hodgkin Huxley parameters
vtrap = @(x,y) x./(exp(x./y) - 1);

% m parameters
alpha_m = @(v) .1 .* vtrap(-(v+40),10);
beta_m = @(v) 4 .* exp(-(v+65)./18);
sum_m = @(v) alpha_m(v) + beta_m(v);
minf = @(v) alpha_m(v)./sum_m(v);
% h parameters
alpha_h = @(v) .07 .* exp(-(v+65)./20);
beta_h = @(v) 1 ./ (exp(-(v+35)./10) + 1);
sum_h = @(v) alpha_h(v) + beta_h(v);
hinf = @(v) alpha_h(v)./sum_h(v);
% n parameters
alpha_n = @(v) .01 .* vtrap(-(v+55),10);
beta_n = @(v) .125 .* exp(-(v+65)./80);
sum_n = @(v) alpha_n(v) + beta_n(v);
ninf = @(v) alpha_n(v)./sum_n(v);

v = linspace(-100, 50, 100);
figure;
plot(v,minf(v),'k-');
hold on;
plot(v,ninf(v), 'b-');
plot(v,hinf(v), 'r-');

gk = ik ./(vk .* (ninf(vm).^4) );
gna = ina ./(vna .* (minf(vm).^3) );

gk_bar = mean(gk);
gna_bar = mean(gna);

l = 35;
d = 25;

area = l * d * pi;
gk_surf = 100.*gk_bar/area;
gna_surf = 100.*gna_bar/area;