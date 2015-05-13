os = ispc;
%code for system agnosticism in opening directory
if os == 1
    tempdata_address = '..\tempdata\' ;
    nrniv_dir = '"C:\nrn73w64\bin64\nrniv.exe"';
    %mpi_dir = '"C:\Program Files\MPICH2\bin\mpiexec.exe"';
    mpi_dir = '"C:\nrn73w64\bin64\mpiexec.exe"';
else
    tempdata_address = '../tempdata/' ;
    %nrniv_dir = '/Applications/NEURON-7.3/nrn/x86_64/bin/nrniv';
    nrniv_dir = '/Applications/NEURON-7.3/nrngui';
end