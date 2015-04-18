clear; clc; close all;
format long
os = ispc;
%code for system agnosticism in opening directory
if os == 1
    tempdata_address = '.\tempdata\' ;
    nrniv_dir = 'C:\nrn73w64\bin64\nrniv.exe' ;
else
    tempdata_address = 'tempdata/' ;
    nrniv_dir = '/Applications/NEURON-7.3/nrngui';
end

AMPS = 0.005:0.001:0.015;

for a = 1:length(AMPS)
    tic
    fprintf('cell %d',a);
    
        nrncommand = [nrniv_dir...
            ' -nobanner -c mat_exc_coupling=' sprintf('%4.4f', AMPS(a))...
            ' testing3.hoc -c quit()'];
    system(nrncommand);
    
    RG_E_v = cell(1,20);
    RG_F_v = cell(1,20);
%     
%     PF_E_v = cell(1,20);
%     PF_F_v = cell(1,20);
%     
%     MN_E_v = cell(1,20);
%     MN_F_v = cell(1,20);
    
    INRG_E_v = cell(1,20);
    INRG_F_v = cell(1,20);
    
    for b = 0:19
    RG_E_v{b+1} = textread(sprintf('RG_E_v_%d.txt',b),'%f');
    RG_F_v{b+1} = textread(sprintf('RG_F_v_%d.txt',b),'%f');
%     
%     MN_E_v{b+1} = textread(sprintf('MN_E_v_%d.txt',b),'%f');
%     MN_F_v{b+1} = textread(sprintf('MN_F_v_%d.txt',b),'%f');
%     
%     PF_E_v{b+1} = textread(sprintf('PF_E_v_%d.txt',b),'%f');
%     PF_F_v{b+1} = textread(sprintf('PF_F_v_%d.txt',b),'%f');
    
    INRG_E_v{b+1} = textread(sprintf('INRG_E_v_%d.txt',b),'%f');
    INRG_F_v{b+1} = textread(sprintf('INRG_F_v_%d.txt',b),'%f');
    
     end
    pop_name = sprintf('pop_test2_exc_coupling_%4.4f.mat',AMPS(a));
    save(pop_name);
	rasters_population(pop_name, 0.025, 30000);
    plot_population(pop_name, 0.025, 30000);
	toc
end