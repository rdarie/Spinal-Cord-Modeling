function apcount = test_recruitment(data_file)
start_time = 0;
% when to start stimulation (ms)
dur_time = 1;
% how long is the stimulation on (ms)
interval_time = 100;

ampstart = 9;
ampmax = 10;
stepsize = 1;

n_amps = floor((ampmax - ampstart)/stepsize) + 1;
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

a = 1;
tic
fprintf('cell %d\n', a);
n_nodes = length(V_extra{a})./points_per_node;
nrn_geom(coords{a}, diams(a), n_nodes, points_per_node,inl,1);

fwrite(v_file, V_extra{a},'double'); %v from comsol to text
fwrite(cellparam_file,...
    [n_nodes start_time dur_time interval_time diams(a)...
    inl points_per_node ampstart stepsize ampmax],...
    'double');
if os == 1
    %nrncommand = [nrniv_dir...
    %' -nobanner mainparallel.hoc -c quit()'];
    nrncommand = [mpi_dir ' -np 2 ' nrniv_dir...
        ' -mpi -nobanner mainparallel.hoc -c quit()'];
else
    nrncommand = ['/Applications/NEURON-7.3/nrn/x86_64/bin/nrniv main.hoc'];
end
system(nrncommand);

[apcount,errmsg]=nrn_vread(curr_apcount_filename,'n');

end
