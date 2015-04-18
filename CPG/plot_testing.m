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

%amplitudes = [25e-4];
amplitudes = linspace(1e-4, 100e-4,100);

for a = 1:length(amplitudes)
    nrncommand = [nrniv_dir...
        ' -nobanner -c AMP=' sprintf('%4.4f', amplitudes(a))...
        ' testing.hoc -c quit()'];
    system(nrncommand);
    
    run_plotting;
    print('-dpng', sprintf('amplitude%d.png', a));
    save(sprintf('amplitude%d.mat', a));
    close all; clc;
end