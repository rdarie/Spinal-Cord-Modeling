%% activating_functions_assemble
clear;clc;close all;

system_id_old;

comsol_files = {'5M mesh\move_root_um_altel','5M mesh\one_root_um_altel'};

axon_files = {'moved_axon_centers.csv','axon_centers.csv'};

diam = [9];
start_offset = 0;

for a = 1:length(comsol_files)
    for b = 1:length(diam)
        
        assemble_voltage_laplacians(comsol_files{a},axon_files{a},diam(b),start_offset);
        
    end
end