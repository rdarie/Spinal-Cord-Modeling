function plot_population(pop_name,dt,tstop)
system_id;

plot_colors = {...
    [0    0.4470    0.7410],...
    [0.8500    0.3250    0.0980],...
    [0.9290    0.6940    0.1250],...
    [0.4660    0.6740    0.1880],...
    [0.4940    0.1840    0.5560]
};

load([tempdata_address pop_name]);

dec_factor = 100;

t = (0:dt*dec_factor:tstop).'.*1e-3;
rfig();

for a = 1:length(RG_E_v)
    subplot(2,1,1);
    h = plot3(t,t.^0.*a,RG_E_v{a}(1:dec_factor:length(RG_E_v{a})),'b-');
    hold on;
    h.Color = plot_colors{1};
    h.Color(4) = 0.5;
    h = plot3(t,t.^0.*a,RG_F_v{a}(1:dec_factor:length(RG_F_v{a})),'g-');
    h.Color = plot_colors{4};
    h.Color(4) = 0.5;
    title('RG');
    xlabel('Time(s)');
    ylabel('Neuron #');
    zlabel('Membrane Voltage (MV)');
    
    xlim([10 15]);
    view([5 45]);
    subplot(2,1,2);
    h = plot3(t,t.^0.*a,INRG_E_v{a}(1:dec_factor:length(INRG_E_v{a})),'b-');
    hold on;
    h.Color = plot_colors{1};
    h.Color(4) = 0.5;
    h = plot3(t,t.^0.*a,INRG_F_v{a}(1:dec_factor:length(RG_E_v{a})),'g-');
    h.Color = plot_colors{4};
    h.Color(4) = 0.5;
    title('INRG');
    xlabel('Time(s)');
    ylabel('Neuron #');
    zlabel('Membrane Voltage (MV)');
    
    xlim([10 15]);
    view([5 45]);
end

xlabel('Time(s)');
print('-dpng', [pop_name(1:end-4) '_traces.png']);
close all;
end