function assemble_voltages(fname,pointlist,diam,start_offset)

inl = 100;
% how many times longer is a paranode than a node?

comsol_file = ['E:\Google Drive\CSP\COMSOL V2\' fname];
fem = mphload([comsol_file '.mph']);
geom = 'geom1';

system_id_old;

points_per_node = 1e2+1;

[temp_V, temp_domain, temp_sigma, temp_coords, n_nodes] = ...
	get_spline_voltages(fem,pointlist,tempdata_address, inl,...
    points_per_node,diam,start_offset);
diams(1) = diam;
coords{1} = temp_coords;
V_extra{1,:} = temp_V;
domain{1,:} = temp_domain;
sigma{1,:} = temp_sigma;

%save to matlab variables

save([tempdata_address 'comsol_solution.mat'], 'V_extra', 'domain',...
    'sigma', 'coords', 'diams', 'n_nodes', 'inl', 'points_per_node');

fprintf('Done!');
end