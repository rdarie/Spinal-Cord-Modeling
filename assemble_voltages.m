function assemble_voltages(fname, tag, pointlist, diam, start_offset,...
    inl, points_per_node, debugging)

system_id; %loads path location names

comsol_file = [comsol_folder fname];
fullpointlist = [comsol_folder pointlist];
fem = mphload([comsol_file '.mph']);
geom = 'geom1';

simulation = cell(length(diam), length(start_offset));

for a = 1:length(diam)
    for b = 1:length(start_offset)
        
        [temp_V, temp_d2V_ds2, temp_domain, temp_sigma, temp_coords] = ...
            get_spline_voltages(fem, 1, 1, geom, fullpointlist, tempdata_address,...
             debugging, inl, points_per_node, diam(a), start_offset(b));
        
        simulation{a,b} = struct('diam', diam(a), 'coords', temp_coords,...
            'V_extra', temp_V, 'd2V_ds2', temp_d2V_ds2, 'domain',...
            temp_domain, 'sigma', temp_sigma, 'pointlist', pointlist, 'tag', tag);
    end
end
%save to matlab variables

save([tempdata_address fname '_' pointlist(1:end-4) '_cs.mat'], 'simulation');

fprintf('Done!');
end