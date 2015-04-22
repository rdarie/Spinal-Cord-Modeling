clear; clc; close all;
format long

system_id;

AMPS = [0 61e-4 61e-3];

for a = 1:length(AMPS)
    tic
    fprintf('cell %d',a);
    
        nrncommand = [nrniv_dir...
            ' -nobanner '...
            ' -c mat_Ia_fibE_stimval=' sprintf('%4.4f', AMPS(a))...
            ' -c mat_Ib_fibE_stimval=' sprintf('%4.4f', AMPS(a))...
            ' -c mat_Ia_fibF_stimval=' sprintf('%4.4f', AMPS(a))...
            ' -c mat_Ib_fibF_stimval=' sprintf('%4.4f', AMPS(a))...
            ' -c mat_d_rge=' sprintf('%4.4f', 0)...
            ' -c mat_d_rgf=' sprintf('%4.4f', 0)...
            ' -c mat_d_pf=' sprintf('%4.4f', 0)...
            ' Iab_stim_simult.hoc -c quit()'];
    system(nrncommand);
    
    RG_E_v = cell(1,20);
    RG_F_v = cell(1,20);
     
     PF_E_v = cell(1,20);
     PF_F_v = cell(1,20);
     
     MN_E_v = cell(1,20);
     MN_F_v = cell(1,20);
    
    INRG_E_v = cell(1,20);
    INRG_F_v = cell(1,20);
    
    Iab_E_v = cell(1,20);

    Ia_E_v = cell(1,20);
    Ia_F_v = cell(1,20);

    Ib_E_v = cell(1,20);
    Ib_F_v = cell(1,20);

    for c = 0:19
        RG_E_v{c+1} = textread(sprintf('RG_E_v_%d.txt',c),'%f');
        RG_F_v{c+1} = textread(sprintf('RG_F_v_%d.txt',c),'%f');
     
        MN_E_v{c+1} = textread(sprintf('MN_E_v_%d.txt',c),'%f');
        MN_F_v{c+1} = textread(sprintf('MN_F_v_%d.txt',c),'%f');
     
        PF_E_v{c+1} = textread(sprintf('PF_E_v_%d.txt',c),'%f');
        PF_F_v{c+1} = textread(sprintf('PF_F_v_%d.txt',c),'%f');
    
        INRG_E_v{c+1} = textread(sprintf('INRG_E_v_%d.txt',c),'%f');
        INRG_F_v{c+1} = textread(sprintf('INRG_F_v_%d.txt',c),'%f');

        Ib_E_v{c+1} = textread(sprintf('Ib_E_v_%d.txt',c),'%f');
        Ib_F_v{c+1} = textread(sprintf('Ib_F_v_%d.txt',c),'%f');

        Ia_E_v{c+1} = textread(sprintf('Ia_E_v_%d.txt',c),'%f');
        Ia_F_v{c+1} = textread(sprintf('Ia_F_v_%d.txt',c),'%f');

        Iab_E_v{c+1} = textread(sprintf('Iab_E_v_%d.txt',c),'%f');
    
    end
    
    pop_name = sprintf('pop_simult_IaE_%4.4f_IbE_%4.4f_IaF_%4.4f_IbF_%4.4f.mat',AMPS(a),AMPS(a),AMPS(a),AMPS(a));
    save([tempdata_address pop_name]);
	rasters_population(tempdata_address,pop_name, 0.025, 15000);
    plot_population(tempdata_address,pop_name, 0.025, 15000);

    rasters_pf_motoneurons(tempdata_address,pop_name, 0.025, 15000);
    plot_pf_motoneurons(tempdata_address,pop_name, 0.025, 15000);
	toc
end