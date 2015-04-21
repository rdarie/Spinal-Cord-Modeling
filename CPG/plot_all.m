function plot_all(fold_name, pop_name, dt, tstop)

	rasters_population(fold_name, pop_name, dt, tstop);
    plot_population(fold_name, pop_name, dt, tstop);

    rasters_pf_motoneurons(fold_name, pop_name, dt, tstop);
    plot_pf_motoneurons(fold_name, pop_name, dt, tstop);

end