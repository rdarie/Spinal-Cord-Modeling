function recruitment(data_file)
start_time = 15;
% when to start stimulation (ms)
dur_time = 0.5;
% how long is the stimulation on (ms)
interval_time = 5;

ampstart = 0.5;
ampmax = 8;
stepsize = 0.5;
% how long is the stimulation off (ms)
% together, these last two determine the waveform/duty cycle of the square
% wave that stimulates the fiber.

system_id_old;

comsol_file = strcat(tempdata_address, data_file);
v_dir = strcat(tempdata_address, 'matlab_v_extra');
cellparam_dir = strcat(tempdata_address, 'cell_params');
curr_apcount_dir = strcat(tempdata_address, 'curr_ap_count.txt');


load(comsol_file);

n_cells = length(diams);
AMPS = ampstart:stepsize:ampmax;
rec_curve = zeros(n_cells, length(AMPS));


for a = 1:n_cells
    tic
    fprintf('cell %d\n', a);
    
    n_nodes = floor(length(V_extra{a})./2);
    
    points_per_node = 1;
    nrn_geom(coords{a}, diams(a), n_nodes, points_per_node);
    
    dlmwrite(v_dir, V_extra{a},' '); %v from comsol to text
    dlmwrite(cellparam_dir,...
        [n_nodes start_time dur_time interval_time diams(a) inl ampmax stepsize ampstart],...
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
        
        fID = fopen(curr_apcount_dir);
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
        
        rec_curve(a,:) = numap > 2;
        toc
end

rec_curve = sum(rec_curve, 1);
rec_curve = rec_curve./max(rec_curve).*100;
plot(AMPS, rec_curve);
title('Recruitment curve for 50 random diameters');
ylabel('Percent recruited');
xlabel('Stimulation amplitude (V)');
ylim([-10 110]);

print('-dpng', data_file);
