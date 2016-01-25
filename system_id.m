
comsol_folder = getenv('CSPCOMSOL');
git_folder = getenv('CSPGIT');
project_folder = [git_folder 'Spinal-Cord-Modeling\'];
%code for system agnosticism in opening directory
if ispc
    tempdata_address = [git_folder 'tempdata\'];
    vtraces_address = [tempdata_address 'vtraces\'];
    
    nrniv_dir = ['"' getenv('NEURONHOME') '\bin\nrniv.exe"'];
        
    mpi_dir = ['"' getenv('NEURONHOME') '\bin\mpiexec.exe"'];
    
elseif isunix
    % Currently not working
    tempdata_address = '../tempdata/';
    vtraces_address = [tempdata_address 'vtraces/'];
    %nrniv_dir = '/Applications/NEURON-7.3/nrn/x86_64/bin/nrniv';
    nrniv_dir = '/gpfs/runtime/opt/neuron/7.3/x86_64/bin/nrniv';
    nrncommand = [nrniv_dir ' mainparallel.hoc'];
end

