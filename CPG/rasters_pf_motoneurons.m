function rasters_pf_motoneurons(pop_name, dt, tstop)

system_id;

load([tempdata_address pop_name]);

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
        'g-', 'DisplayName', 'Flexor');
    MN_E_short{a} = MN_E_v{a}(1:dec_factor:length(MN_E_v{a}));
    [~, MN_E_raster{a}] = findpeaks(MN_E_short{a},'minpeakheight',-20);
    MN_E_raster{a} = t(MN_E_raster{a});
    
    hold on;
    h2 = plot([MN_E_raster{a}; MN_E_raster{a}],...
        [a.*MN_E_raster{a}.^0;(a+1).*MN_E_raster{a}.^0],...
        'b-', 'DisplayName', 'Extensor');
    
end

xlabel('Time(s)');
xlim([20 30]);
ylim([1 a]);
print('-dpng', [pop_name(1:end-4), '_MN.png']);

close all;
end