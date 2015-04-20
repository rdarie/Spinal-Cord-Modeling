close all;

for a = 1:length(AMPS)
    
    pop_name = sprintf('pop_test2_mn_el_%4.4f.mat',AMPS(a));
    load([tempdata_address pop_name]);
	rasters_population(pop_name, 0.025, 15000);
    plot_population(pop_name, 0.025, 15000);

    rasters_pf_motoneurons(pop_name, 0.025, 15000);
    plot_pf_motoneurons(pop_name, 0.025, 15000);
end