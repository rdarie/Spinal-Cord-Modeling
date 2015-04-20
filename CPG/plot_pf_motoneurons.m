function plot_pf_motoneurons(pop_name,dt,tstop)

system_id;

load([tempdata_address pop_name]);

dec_factor = 5;

t = (0:dt*dec_factor:tstop).*1e-3;

rfig();

for a = 1:length(MN_E_v)
    subplot(2,1,1);
    h = plot(t,MN_E_v{a}(1:dec_factor:length(MN_E_v{a})),'b-');
    hold on;
    h.Color(4) = 0.1;
    h = plot(t,MN_F_v{a}(1:dec_factor:length(MN_F_v{a})),'g-');
    h.Color(4) = 0.1;
    title('MN');
    
xlim([10 15]);
    subplot(2,1,2);
    h = plot(t,PF_E_v{a}(1:dec_factor:length(PF_E_v{a})),'b-');
    hold on;
    h.Color(4) = 0.1;
    h = plot(t,PF_F_v{a}(1:dec_factor:length(PF_F_v{a})),'g-');
    h.Color(4) = 0.1;
    title('PF');
    
xlim([10 15]);
end

xlabel('Time(s)');
print('-dpng', [pop_name(1:end-4) '_traces_MN.png']);
close all;
end