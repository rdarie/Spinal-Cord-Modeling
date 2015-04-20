function plot_population(pop_name,dt,tstop)
system_id;
load([tempdata_address pop_name]);
dec_factor = 100;
t = (0:dt*dec_factor:tstop).'.*1e-3;
rfig();

for a = 1:length(RG_E_v)
    subplot(2,1,1);
    h = plot(t,RG_E_v{a}(1:dec_factor:length(RG_E_v{a})),'b-');
    hold on;
    h.Color(4) = 0.1;
    h = plot(t,RG_F_v{a}(1:dec_factor:length(RG_F_v{a})),'g-');
    h.Color(4) = 0.1;
    title('RG');
    
xlim([20 30]);
    subplot(2,1,2);
    h = plot(t,INRG_E_v{a}(1:dec_factor:length(INRG_E_v{a})),'b-');
    hold on;
    h.Color(4) = 0.1;
    h = plot(t,INRG_F_v{a}(1:dec_factor:length(RG_E_v{a})),'g-');
    h.Color(4) = 0.1;
    title('INRG');
    
xlim([20 30]);
end

xlabel('Time(s)');
print('-dpng', [pop_name(1:end-4) '_traces.png']);
close all;
end