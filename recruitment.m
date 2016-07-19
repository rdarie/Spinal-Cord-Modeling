function recruitment(data_file, start_time, dur_time,...
    interval_time, ampstart, ampmax, stepsize, points_per_node, inl)

system_id;

comsol_filename = strcat(tempdata_address, data_file);

v_filename = strcat(tempdata_address, 'matlab_v_extra');
v_file = fopen(v_filename,'w');

cellparam_filename = strcat(tempdata_address, 'cell_params');
cellparam_file = fopen(cellparam_filename,'w');

curr_apcount_filename = strcat(tempdata_address, 'curr_ap_count.dat');

load(comsol_filename);

n_cells = size(simulation,1)*size(simulation,2);
AMPS = ampstart:stepsize:ampmax;
rec_curve = zeros(n_cells, length(AMPS));

for a = 1:size(simulation,1)
    for b= 1:size(simulation,2)
        
        tic
        fprintf('cell %d\n', a);
        n_nodes = length(simulation{a,b}.V_extra)./points_per_node;
        nrn_geom(simulation{a,b}.coords, simulation{a,b}.diam,...
            n_nodes, points_per_node,inl,0);
        
        fwrite(v_file, -simulation{a,b}.V_extra,'double'); %v from comsol to text
        fwrite(cellparam_file,...
            [n_nodes start_time dur_time interval_time simulation{a,b}.diam ...
            inl points_per_node ampstart stepsize ampmax...
            simulation{a,b}.coords(1,end)...
            simulation{a,b}.coords(2,end)...
            simulation{a,b}.coords(3,end)],...
            'double');
        
        curr_folder = pwd;
        cd(project_folder);
        nrncommand = [mpi_dir ' -np ' num2str(feature('numCores'))...
            ' ' nrniv_dir...
            ' -mpi -nobanner '  'main.hoc -c quit()'];
        
        system(nrncommand);
        
        [apcount,errmsg]=nrn_vread(curr_apcount_filename,'n');
        
        amps = apcount(1:2:end);
        numap = apcount(2:2:end);
        
        if sum(isnan(amps)) || sum(isnan(numap))
            keyboard;
        end
        
        rec_curve(a,:) = numap > 50;
        
        
        cd(curr_folder);
        toc
    end
end

rec_curve = sum(rec_curve, 1);
rec_curve = rec_curve./max(rec_curve).*100;
plot(AMPS, rec_curve);
title('Recruitment curve for 20 random diameters');
ylabel('Percent recruited');
xlabel('Stimulation amplitude (V)');
ylim([-10 110]);

print('-dpng', [tempdata_address, data_file]);
