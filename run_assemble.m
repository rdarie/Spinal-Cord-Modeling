clear;clc;close all;

%for start_offset = 0:100
    start_offset = 5;
    assemble_voltages('5M mesh\no_root_um','axon_centers.csv',9,start_offset);

%end