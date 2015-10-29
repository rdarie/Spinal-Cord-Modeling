function recruitment(data_file)
start_time = 2500;
% when to start stimulation (ms)
dur_time = 20;
% how long is the stimulation on (ms)
interval_time = 80;

ampstart = 1;
ampmax = 1;
stepsize = 1;
% how long is the stimulation off (ms)
% together, these last two determine the waveform/duty cycle of the square
% wave that stimulates the fiber.

system_id_old;

comsol_filename = strcat(tempdata_address, data_file);

v_filename = strcat(tempdata_address, 'matlab_v_extra');
v_file = fopen(v_filename,'w');

cellparam_filename = strcat(tempdata_address, 'cell_params');
cellparam_file = fopen(cellparam_filename,'w');

curr_apcount_filename = strcat(tempdata_address, 'curr_ap_count.dat');

load(comsol_filename);

n_cells = length(diams);
AMPS = ampstart:stepsize:ampmax;
rec_curve = zeros(n_cells, length(AMPS));


for a = 1:n_cells
    tic
    fprintf('cell %d\n', a);
    n_nodes = length(V_extra{a})./points_per_node;
    nrn_geom(coords{a}, diams(a), n_nodes, points_per_node,inl,0);
    
    fwrite(v_file, -V_extra{a},'double'); %v from comsol to text
    fwrite(cellparam_file,...
        [n_nodes start_time dur_time interval_time diams(a)...
        inl points_per_node ampstart stepsize ampmax coords{a}(1,end) coords{a}(2,end) coords{a}(3,end)],...
            'double');
        system(nrncommand);
        
        [apcount,errmsg]=nrn_vread(curr_apcount_filename,'n');
        
        amps = apcount(1:2:end);
        numap = apcount(2:2:end);
                
        if sum(isnan(amps)) || sum(isnan(numap))
            keyboard;
        end
        
        rec_curve(a,:) = numap > 50;
        toc
end

rec_curve = sum(rec_curve, 1);
rec_curve = rec_curve./max(rec_curve).*100;
plot(AMPS, rec_curve);
title('Recruitment curve for 20 random diameters');
ylabel('Percent recruited');
xlabel('Stimulation amplitude (V)');
ylim([-10 110]);

print('-dpng', [tempdata_address, data_file]);
