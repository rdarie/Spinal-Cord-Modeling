%% activating_functions_3, no mean and std

clear;clc;close all;

system_id_old;

plot_colors = parula(16);
f1 = rfig();
hold on;
f2 = rfig();
hold on;

tags = {...
    'Root present'...
    'Root not present'...
    };

comsol_files = {'no_root_um'};

axon_files = {'axon_centers.csv','axon_centers.csv'};
%  comsol_files = {...
%      'move_root_um', ...
%      'no_root_um'...
%      };
%
%  axon_files = {...
%      'moved_axon_centers.csv', ...
%      'moved_axon_centers.csv' ...
%      };

has_roots = [1 0];
diam = [9];
start_offset = 0;

filter_len = 100;
smoother = ones(1,filter_len);
smoother = smoother./length(smoother);

for a = 1:length(comsol_files)
    for b = 1:length(diam)
        
        assemble_voltage_laplacians(comsol_files{a},axon_files{a},diam(b),start_offset);
%         load([tempdata_address 'comsol_solution.mat']);
%         
%         d2Vds = cell2mat(d2Vds);
%         d2Vds_smooth(1,:) = conv(d2Vds(1,:), smoother, 'same');
%         d2Vds_smooth(2,:) = conv(d2Vds(2,:), smoother, 'same');
%         d2Vds_smooth(3,:) = conv(d2Vds(3,:), smoother, 'same');
%         grad_mag = sqrt(d2Vds_smooth(1,:).^2+d2Vds_smooth(2,:).^2+d2Vds_smooth(3,:).^2);
%         
%         [arclen,seglen] = arclength(coords{1}(1,:),...
%             coords{1}(2,:),coords{1}(3,:),'spline');
%         al = mean(seglen);
%         
%          mat_sig = sigma{1};
%          spl = coords{1};
%          tang = zeros(size(spl));
%          for c = 1:size(spl,2)-1
%              tang(:,c) = spl(:,c+1) - spl(:,c);
%              tang(:,c) = tang(:,c) ./ norm(tang(:,c));
%          end
%          tang(:,size(spl,2)) = tang(:,c);
%          af = dot(tang,d2Vds_smooth);
% %         af = del2(V_smooth,al);
% %         V = V_smooth;
%         
%         
%         if has_roots(a)
%             d_name = tags{1};
%             cl = plot_colors(1+a,:);
%         else
%             d_name = tags{2};
%             cl = plot_colors(8+a,:);
%         end
%         
%         distance_along_arc = cumsum([0; seglen]);
%         normalized_al = 100.*distance_along_arc./max(distance_along_arc);
%         
%         figure(f1);
%         
%         h1(a) = plot(normalized_al,af./max(af),'k-'...
%             , 'DisplayName', d_name,'LineWidth',3);
%         hold on;
%         plot(normalized_al, mat_sig./max(mat_sig),'g-',...
%             'LineWidth',2, 'DisplayName', 'sigma');
%         plot(normalized_al, domain{1}./max(domain{1}),'r-',...
%             'LineWidth',2, 'DisplayName', 'domain');
%         h1(a).Color = cl;
%         
%         figure(f2);
%         h2(a) = plot(normalized_al,d2Vds_smooth(1,:)./max(d2Vds_smooth(1,:)),'k-'...
%             , 'DisplayName', d_name,'LineWidth',1);
%         hold on;
%         plot(normalized_al, mat_sig./max(mat_sig),'g-');
%         plot(normalized_al, domain{1}./max(domain{1}),'r-');
%         plot(normalized_al,d2Vds(1,:)./max(d2Vds(1,:)),'r--')
%         h2(a).Color = cl;
%         
%         figure(f1);
%         ax = gca;
%         axis tight
%         set(ax,'Fontsize',24);
%         legend(h1,'Location','southwest');
%         
%         %ylabel('Activating Function (V/m^{2})');
%         ylabel('Normalized Activating Function (unitless)');
%         xlabel('Percentage along length of fiber (%)');
%         print('-dpng', [tempdata_address comsol_files{1} '_AF']);
%         savefig([tempdata_address comsol_files{1} '_AF']);
%         
%         figure(f2);
%         ax = gca;
%         axis tight
%         set(ax,'Fontsize',24);
%         legend(h2,'Location','southwest');
%         
%         ylabel('Extracellular voltage (V)');
%         xlabel('Percentage along length of fiber (%)');
%         print('-dpng',  [tempdata_address comsol_files{1} '_V']);
%         savefig([tempdata_address comsol_files{1} '_AF']);
%         clf(f1)
%         clf(f2)
    end
end
