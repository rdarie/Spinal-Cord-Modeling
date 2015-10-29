clear;clc;close all;
load('matlab.mat');

f3 = rfig;

v_prime = gradient(V_extra{1},distance_along_arc);
h3(a) = plot(normalized_al,v_prime./(max(abs(v_prime))),'k-'...
                , 'DisplayName', d_name,'LineWidth',3);
            hold on;
            plot(normalized_al, mat_sig./max(mat_sig),'g-');
            plot(normalized_al, domain{1}./max(domain{1}),'r-');
            h1(a).Color = cl;