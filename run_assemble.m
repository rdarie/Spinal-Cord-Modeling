clear;clc;close all;

ppn = 1e2+1;
inl = 100;% how many times longer is a paranode than a node?
%diam = log(random('logn', 9, 0.2, 1, 1));
diam = [9,5];

%for start_offset = 0:100
start_offset = 5;
    
assemble_voltages('5M mesh\no_root_um','straight, no root','axon_centers.csv',diam,start_offset, inl, ppn);
%end