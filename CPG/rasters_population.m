function rasters_population(fold_name, pop_name, dt, tstop)


plot_colors = {...
    [0    0.4470    0.7410],...
    [0.8500    0.3250    0.0980],...
    [0.9290    0.6940    0.1250],...
    [0.4660    0.6740    0.1880],...
    [0.4940    0.1840    0.5560]
};

load([fold_name pop_name]);
dec_factor = 100;
t = (0:dt*dec_factor:tstop).*1e-3;
rfig();

for a = 1:length(RG_E_v)
    
    RG_F_short{a} = RG_F_v{a}(1:dec_factor:length(RG_F_v{a}));
    [~, RG_F_raster{a}] = findpeaks(RG_F_short{a},'minpeakheight',-20);
    RG_F_raster{a} = t(RG_F_raster{a});
    %plot(RG_E_short{a});
    hold on;
    h1 = plot([RG_F_raster{a}; RG_F_raster{a}],...
        [a.*RG_F_raster{a}.^0;(a+1).*RG_F_raster{a}.^0],...
        'Color',plot_colors{4}, 'DisplayName', 'Flexor');
    
    
    RG_E_short{a} = RG_E_v{a}(1:dec_factor:length(RG_E_v{a}));
    [~, RG_E_raster{a}] = findpeaks(RG_E_short{a},'minpeakheight',-20);
    RG_E_raster{a} = t(RG_E_raster{a});
    %plot(RG_E_short{a});
    hold on;
    h2 = plot([RG_E_raster{a}; RG_E_raster{a}],...
        [a.*RG_E_raster{a}.^0;(a+1).*RG_E_raster{a}.^0],...
        'Color',plot_colors{1}, 'DisplayName', 'Extensor');
    
end


xlabel('Time(s)');
xlim([10 15]);
ylim([1 a]);
print('-dpng', [fold_name pop_name(1:end-4), '.png']);

close all;
end