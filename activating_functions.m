clear;clc;close all;

filelist = {'comsol_solution_3100',...
    'comsol_solution_passage_3100',...
    'comsol_solution_3600',...
    'comsol_solution_passage_3600'};
tags = {...
    'Fiber of Interest, electrode at 3100'... 
    'Fiber of Passage, electrode at 3100'... 
    'Fiber of Interest, electrode at 3600'... 
    'Fiber of Passage, electrode at 3600'...    
};
plot_colors = {...
    [0    0.4470    0.7410],...
    [0.8500    0.3250    0.0980],...
    [0.9290    0.6940    0.1250],...
    [0.4940    0.1840    0.5560]
};
system_id_old;
f1 = rfig();
    hold on;
f2 = rfig();
    hold on;
for a = 1:length(filelist)
    
    load([tempdata_address filelist{a}]);
    for b = 1:length(V_extra)
        al = arc_lengths(coords{b});
        af = del2(V_extra{b},al);
        
        figure(f1);
        h1(a) = plot(100.*al./max(al),af...
        , 'DisplayName', tags{a});
        h1(a).Color = plot_colors{a};
        figure(f2);
        h2(a) = plot(100.*al./max(al),V_extra{b}...
        , 'DisplayName', tags{a});
        h2(a).Color = plot_colors{a};
    end
end

figure(f1);
legend(h1,'Location','southwest');

ylabel('Activating function');
xlabel('Percentage along length of fiber');
print('-dpng', 'Activating_Function');
figure(f2);
legend(h2,'Location','southwest');

ylabel('Extracellular voltage');
xlabel('Percentage along length of fiber');
print('-dpng', 'Voltage_Function');