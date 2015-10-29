clear;clc;close all;

system_id_old;

plot_colors = parula(16);
f1 = rfig();
hold on;
f2 = rfig();
hold on;
% 
% load([tempdata_address 'sel_names_pieces.mat']);

tags = {...
    'Root present'...
    'Root not present'...
    };
% 
% comsol_files = {...
%     'pieces_B4_mono', ...
%     'pieces_B7_mono', ...
%     'pieces_B10_mono', ...
%     'pieces_A4_mono', ...
%     'pieces_A7_mono', ...
%     'pieces_A10_mono', ...
%     'pieces_no_root_B4_mono', ...
%     'pieces_no_root_B7_mono', ...
%     'pieces_no_root_B10_mono', ...
%     'pieces_no_root_A4_mono', ...
%     'pieces_no_root_A7_mono', ...
%     'pieces_no_root_A10_mono', ...
%     'pieces_A10PB4N', ...
%     'pieces_A10PB7N', ...
%     'pieces_A10PB10N', ...
%     'pieces_no_root_A10PB4N', ...
%     'pieces_no_root_A10PB7N', ...
%     'pieces_no_root_A10PB10N', ...
%     };

comsol_files = {...
    'pieces_A10PB4N', ...
    'pieces_no_root_A10PB4N' ...
    };

has_roots = [1 0];
diam = [9];
start_offset = 0:20:100;

for a = 1:length(comsol_files)
    for b = 1:length(diam)
        
        af = [];
        V = [];
        for c = 1:length(start_offset)
            
        fprintf('a=%d out of %d, b=%d out of %d, c=%d out of %d\n',...
            a,length(comsol_files),b,length(diam),c,length(start_offset));
        
            assemble_voltages(comsol_files{a},diam(b),start_offset(c));
            load([tempdata_address 'comsol_solution.mat']);
            
            V_extra{1} = - V_extra{1};
            
            al = arc_lengths(coords{1});
            af = [af; del2(V_extra{1},al)];
            V = [V; V_extra{1}];
            
        end
        
            if has_roots(a)
                d_name = tags{1};
                cl = plot_colors(1+a,:);
            else
                d_name = tags{2};
                cl = plot_colors(8+a,:);
            end
            
            af_bar = mean(af);
            af_sig = std(af);
            
            V_bar = mean(V);
            V_sig = std(V);
%             af_bar = af;
%             af_sig = 0;
%             
%             V_bar = V;
%             V_sig = 0;
            normalized_al = 100.*al./max(al);
            
            figure(f1);
            h1(a) = patch([normalized_al, fliplr(normalized_al)],...
                [(af_bar+af_sig)./max(af_bar) fliplr((af_bar-af_sig)./max(af_bar))],...
                 cl, 'FaceAlpha', 0.5, 'DisplayName', [d_name ' Standard Deviation']...
                 ,'EdgeColor','none');
             hold on;
             
            h2(a) = plot(normalized_al,af_bar./max(af_bar),'k-'...
                , 'DisplayName', d_name,'LineWidth',1);
            h2(a).Color = cl;
            
            figure(f2);
            h3(a) = patch([normalized_al, fliplr(normalized_al)],...
                [V_bar+V_sig fliplr(V_bar-V_sig)],...
                 cl, 'FaceAlpha', 0.5...
                 ,'EdgeColor','none');
            hold on;%, 'DisplayName', [d_name ' Standard Deviation']
            h4(a) = plot(normalized_al,V_bar,'k-'...
                , 'DisplayName', d_name,'LineWidth',1);
            h4(a).Color = cl;
    end
end

figure(f1);
ax = gca;
axis tight
set(ax,'Fontsize',24);
legend(h2,'Location','southwest');

%ylabel('Activating Function (V/m^{2})');
ylabel('Normalized Activating Function (unitless)');
xlabel('Percentage along length of fiber (%)');
print('-dpng', [tempdata_address comsol_files{1} '_AF']);
savefig([tempdata_address comsol_files{1} '_AF']);

figure(f2);
ax = gca;
axis tight
set(ax,'Fontsize',24);
legend(h4,'Location','southwest');

ylabel('Extracellular voltage (V)');
xlabel('Percentage along length of fiber (%)');
print('-dpng',  [tempdata_address comsol_files{1} '_V']);
savefig([tempdata_address comsol_files{1} '_AF']);