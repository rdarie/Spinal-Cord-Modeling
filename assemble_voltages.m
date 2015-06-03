clear;clc;close all;

inl = 100;
% how many times longer is a paranode than a node?

comsol_file = 'Z:\Spinal Cord Model\COMSOL\roots_of_passage\just_cord';
fem = mphload([comsol_file '.mph']);
geom = 'geom1';

system_id_old;

n_diam = 1;
points_per_node = 21;
diams = zeros(1,n_diam);

for a = 1:n_diam
    [temp_V, temp_domain, temp_coords, n_nodes, diam] = ...
        get_spline_voltages(fem,tempdata_address, inl, points_per_node);
    diams(a) = diam;
    coords{a} = temp_coords;
    V_extra{a,:} = temp_V;
    domain{a,:} = temp_domain;
end
%save to matlab variables
save([tempdata_address 'comsol_solution.mat'], 'V_extra', 'domain', 'coords', 'diams', 'n_nodes', 'inl', 'points_per_node');
fprintf('Done!');