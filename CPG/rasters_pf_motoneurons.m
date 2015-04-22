function rasters_pf_motoneurons(fold_name, pop_name, dt, tstop)


plot_colors = {...
    [0    0.4470    0.7410],...
    [0.8500    0.3250    0.0980],...
    [0.9290    0.6940    0.1250],...
    [0.4660    0.6740    0.1880],...
    [0.4940    0.1840    0.5560]
};

load([fold_name pop_name]);

dec_factor = 5;

t = (0:dt*dec_factor:tstop).*1e-3;

rfig();

for a = 1:length(MN_E_v)
    
    MN_F_short{a} = MN_F_v{a}(1:dec_factor:length(MN_F_v{a}));
    [~, MN_F_raster{a}] = findpeaks(MN_F_short{a},'minpeakheight',-20);
    MN_F_raster{a} = t(MN_F_raster{a});
    
    hold on;
    h1 = plot([MN_F_raster{a}; MN_F_raster{a}],...
        [a.*MN_F_raster{a}.^0;(a+1).*MN_F_raster{a}.^0],...
        'Color',plot_colors{4}, 'DisplayName', 'Flexor');
    
    MN_E_short{a} = MN_E_v{a}(1:dec_factor:length(MN_E_v{a}));
    [~, MN_E_raster{a}] = findpeaks(MN_E_short{a},'minpeakheight',-20);
    MN_E_raster{a} = t(MN_E_raster{a});
    
    hold on;
    h2 = plot([MN_E_raster{a}; MN_E_raster{a}],...
        [a.*MN_E_raster{a}.^0;(a+1).*MN_E_raster{a}.^0],...
        'Color',plot_colors{1},  'DisplayName', 'Extensor');
    
    
end

xlabel('Time(s)');
xlim([tstop*1e-3-10 tstop*1e-3]);
ylim([1 a]);
print('-dpng', [fold_name pop_name(1:end-4), '_MN.png']);

close all;
end