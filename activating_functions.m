clear;clc;close all;
system_id_old;
dependencies;
load([tempdata_address 'sel_names_pieces.mat']);
filelist = {'comsol_solution_pieces',...
    'comsol_solution_pieces_no_root',...
    };

tags = {...
    'Root present'...  
    'Root not present'...
};
f1 = rfig();
    hold on;
f2 = rfig();
    hold on;
    
for a = 1:length(filelist)
    
    load([tempdata_address filelist{a}]);
    if a == 1
        what_in = ismember(domain{a},tiss_dom.entities)+...
            2*ismember(domain{a},csf_dom.entities)+...
            3*ismember(domain{a},wmc_dom.entities)+...
            4*ismember(domain{a},wmr_dom.entities)+...
            5*ismember(domain{a},gm_dom.entities)...
            ;
    end
%     for b = 1:length(V_extra)
%         al = arc_lengths(coords{b});
%         af = del2(V_extra{b},al);
%         
%         figure(f1);
%         h1(a) = plot(100.*al./max(al),af...
%         , 'DisplayName', tags{a});
%         h1(a).Color = plot_colors{a};
%         figure(f2);
%         h2(a) = plot(100.*al./max(al),V_extra{b}...
%         , 'DisplayName', tags{a});
%         h2(a).Color = plot_colors{a};
%     end
    
end

% figure(f1);
% legend(h1,'Location','southwest');
% 
% ylabel('Activating function');
% xlabel('Percentage along length of fiber');
% print('-dpng', 'Activating_Function');
% figure(f2);
% legend(h2,'Location','southwest');
% 
% ylabel('Extracellular voltage');
% xlabel('Percentage along length of fiber');
% print('-dpng', 'Voltage_Function');