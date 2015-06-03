
%code for system agnosticism in opening directory
if ispc
    tempdata_address = '..\tempdata\' ;
    vtraces_address = [tempdata_address 'vtraces\'];
    nrniv_dir = '"C:\nrn73w64\bin64\nrniv.exe"';
    %mpi_dir = '"C:\Program Files\MPICH2\bin\mpiexec.exe"';
    mpi_dir = '"C:\nrn73w64\bin64\mpiexec.exe"';
    nrncommand = [mpi_dir ' -np 4 ' nrniv_dir...
        ' -mpi -nobanner mainparallel.hoc -c quit()'];
elseif isunix
    tempdata_address = '../tempdata/';
    vtraces_address = [tempdata_address 'vtraces/'];
    %nrniv_dir = '/Applications/NEURON-7.3/nrn/x86_64/bin/nrniv';
    nrniv_dir = '/gpfs/runtime/opt/neuron/7.3/x86_64/bin/nrniv';
    nrncommand = [nrniv_dir ' mainparallel.hoc'];
end