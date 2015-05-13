function recruitment(data_file)
start_time = 0;
% when to start stimulation (ms)
dur_time = 1;
% how long is the stimulation on (ms)
interval_time = 100;

ampstart = 0.5;
ampmax = 10;
stepsize = 8;
% how long is the stimulation off (ms)
% together, these last two determine the waveform/duty cycle of the square
% wave that stimulates the fiber.

system_id_old;

comsol_file = strcat(tempdata_address, data_file);
v_file = strcat(tempdata_address, 'matlab_v_extra');
cellparam_file = strcat(tempdata_address, 'cell_params');
curr_apcount_file = strcat(tempdata_address, 'curr_ap_count.txt');

load(comsol_file);

n_cells = length(diams);
AMPS = ampstart:stepsize:ampmax;
rec_curve = zeros(n_cells, length(AMPS));


for a = 1:n_cells
    tic
    fprintf('cell %d\n', a);
    n_nodes = length(V_extra{a})./points_per_node;
    nrn_geom(coords{a}, diams(a), n_nodes, points_per_node,inl,1);
    
    dlmwrite(v_file, V_extra{a},' '); %v from comsol to text
    dlmwrite(cellparam_file,...
        [n_nodes start_time dur_time interval_time diams(a)...
        inl points_per_node  ampstart stepsize ampmax],...
            ' ');
        if os == 1
            %nrncommand = [nrniv_dir...
            %' -nobanner mainparallel.hoc -c quit()'];
            nrncommand = [mpi_dir ' -np 12 ' nrniv_dir...
            ' -mpi -nobanner mainparallel.hoc -c quit()'];
        else
            nrncommand = ['/Applications/NEURON-7.3/nrn/x86_64/bin/nrniv main.hoc'];
        end
        system(nrncommand);
        
        fID = fopen(curr_apcount_file);
        apcount = textscan(fID,'%f'); %reads apcount from neuron
        fclose(fID);
        
        apcount = apcount{1};
        
        amps = [];
        numap = [];
        
        b = 1;
        while b < length(apcount)
            amps = [amps apcount(b)];
            numap = [numap apcount(b+1)];
            b = b+2;
        end
        
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

print('-dpng', data_file);
