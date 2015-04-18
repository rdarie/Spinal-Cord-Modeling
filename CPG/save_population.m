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

    nrncommand = [nrniv_dir...
        ' -nobanner'...
        ' testing2.hoc -c quit()'];
    system(nrncommand);
    
    RG_E_v = cell(1,20);
    RG_F_v = cell(1,20);
    
    PF_E_v = cell(1,20);
    PF_F_v = cell(1,20);
    
    MN_E_v = cell(1,20);
    MN_F_v = cell(1,20);
    
    INRG_E_v = cell(1,20);
    INRG_F_v = cell(1,20);
    
    for a = 0:19
    RG_E_v{a+1} = textread(sprintf('RG_E_v_%d.txt',a),'%f');
    RG_F_v{a+1} = textread(sprintf('RG_F_v_%d.txt',a),'%f');
    
    MN_E_v{a+1} = textread(sprintf('MN_E_v_%d.txt',a),'%f');
    MN_F_v{a+1} = textread(sprintf('MN_F_v_%d.txt',a),'%f');
    
    PF_E_v{a+1} = textread(sprintf('PF_E_v_%d.txt',a),'%f');
    PF_F_v{a+1} = textread(sprintf('PF_F_v_%d.txt',a),'%f');
    
    INRG_E_v{a+1} = textread(sprintf('INRG_E_v_%d.txt',a),'%f');
    INRG_F_v{a+1} = textread(sprintf('INRG_F_v_%d.txt',a),'%f');
%     
%     subplot(4,1,1);
%     plot(RG_E_v);
%     title('RG_E');
%     subplot(4,1,3);
%     plot(RG_F_v);
%     title('RG_F');
%     subplot(4,1,2);
%     plot(Inrg_E_v);
%     title('INRG_E');
%     subplot(4,1,4);
%     plot(Inrg_F_v);
%     title('INRG_F');
%     
%     rfig();
%     plot(RG_E_v);
%     hold on;
%     
%     plot(RG_F_v);
     end
%     print('-dpng', sprintf('pop_test.png'));
     save(sprintf('pop_test2_04505.mat'));
%     close all; clc;