clear;clc;close all;

inl = 100;
% how many times longer is a paranode than a node?

comsol_file = 'A:\CSN - Corticospinal Neuroprosthetics\CSP Model\Spinal cord models\No root\no_root';
fem = mphload([comsol_file '.mph']);
geom = 'geom1';

system_id_old;

n_diam = 50;
diams = zeros(1,n_diam);

for a = 1:n_diam
    [temp_V, temp_coords, n_nodes, diam] = ...
        get_spline_voltages(fem,tempdata_address, inl);
    diams(a) = diam;
    coords{a} = temp_coords;
    V_extra{a,:} = temp_V;
end
%save to matlab variables
save([tempdata_address 'comsol_solution.mat'], 'V_extra', 'coords', 'diams', 'n_nodes', 'inl');
fprintf('Done!');