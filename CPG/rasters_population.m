function rasters_population(pop_name, dt, tstop)
system_id;
load([tempdata_address pop_name]);
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
        'g-', 'DisplayName', 'Flexor');
    RG_E_short{a} = RG_E_v{a}(1:dec_factor:length(RG_E_v{a}));
    [~, RG_E_raster{a}] = findpeaks(RG_E_short{a},'minpeakheight',-20);
    RG_E_raster{a} = t(RG_E_raster{a});
    %plot(RG_E_short{a});
    hold on;
    h2 = plot([RG_E_raster{a}; RG_E_raster{a}],...
        [a.*RG_E_raster{a}.^0;(a+1).*RG_E_raster{a}.^0],...
        'b-', 'DisplayName', 'Extensor');
    INRG_E_short{a} = INRG_E_v{a}(1:dec_factor:length(INRG_E_v{a}));
   
    INRG_F_short{a} = INRG_F_v{a}(1:dec_factor:length(RG_E_v{a}));
    
end


xlabel('Time(s)');
xlim([10 15]);
ylim([1 a]);
print('-dpng', [pop_name(1:end-4), '.png']);

close all;
end