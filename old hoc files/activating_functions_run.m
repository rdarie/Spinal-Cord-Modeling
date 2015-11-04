%% activating_functions_3, no mean and std
%% DEPRECATED

clear;clc;close all;

system_id_old;

has_roots = [1 0];
diam = [9];
start_offset = 0;

filter_len = 1;
smoother = ones(1,filter_len);
smoother = smoother./length(smoother);
for a = 1:length(comsol_files)
    d2Vds_smooth = [];
    for b = 1:length(diam)
        
        %         assemble_voltage_laplacians(comsol_files{a},axon_files{a},diam(b),start_offset);
        load([tempdata_address comsol_files{a} axon_files{a}(1:end-4) '_cs.mat']);
        
        d2Vds = cell2mat(d2Vds);
        d2Vds_smooth(1,:) = conv(d2Vds(1,:), smoother, 'same');
        d2Vds_smooth(2,:) = conv(d2Vds(2,:), smoother, 'same');
        d2Vds_smooth(3,:) = conv(d2Vds(3,:), smoother, 'same');
        grad_mag = sqrt(d2Vds_smooth(1,:).^2+d2Vds_smooth(2,:).^2+d2Vds_smooth(3,:).^2);
        
        [arclen,seglen] = arclength(coords{1}(1,:),...
            coords{1}(2,:),coords{1}(3,:),'spline');
        al = mean(seglen);
        
        mat_sig = sigma{1};
        dom = domain{1};
        spl = coords{1};
        tang = zeros(size(spl));
        for c = 1:size(spl,2)-1
            tang(:,c) = spl(:,c+1) - spl(:,c);
            tang(:,c) = tang(:,c) ./ norm(tang(:,c));
        end
        tang(:,size(spl,2)) = tang(:,c);
        af = -dot(tang,d2Vds_smooth); % Cathodic stimulus
        
        
        if has_roots(a)
            d_name = tags{1};
            cl = plot_colors(1+a,:);
        else
            d_name = tags{2};
            cl = plot_colors(8+a,:);
        end
        
        distance_along_arc = cumsum([0; seglen]);
        normalized_al = 100.*distance_along_arc./max(distance_along_arc);
        
        %% Non Normalized AF
        figure(f1);
        
        h1(a) = plot(normalized_al,af,'k-'...
            , 'DisplayName', d_name,'LineWidth',3);
        h1(a).Color = cl;
        a1 = plot(normalized_al(find(af == max(af),1)), af(find(af == max(af),1)),'r*','MarkerSize',10);
        a1.Color = cl;
        ybounds1 = [min(min(af),ybounds1(1)),max(max(af),ybounds1(2))];
        %% X Component of Gradient
        figure(f2);
        h2(a) = plot(normalized_al,d2Vds_smooth(1,:),'k-'...
            , 'DisplayName', d_name,'LineWidth',1);
        plot(normalized_al,d2Vds(1,:),'r--');
        h2(a).Color = cl;
        
        ybounds2 = [min(min(d2Vds_smooth(1,:)),ybounds2(1)),max(max(d2Vds_smooth(1,:)),ybounds2(2))];
        %% Normalized AF
        figure(f3);
        normalized_af = af./max(af);
        h3(a) = plot(normalized_al,normalized_af,'k-'...
            , 'DisplayName', d_name,'LineWidth',3);
        
        h3(a).Color = cl;
        
        ybounds3 = [min(min(normalized_af),ybounds3(1)),max(max(normalized_af),ybounds3(2))];
        
    end
end

%% Plot domain extents
for a = 1:length(comsol_files)
    load([tempdata_address comsol_files{a} axon_files{a}(1:end-4) '_cs.mat']);
    
    [arclen,seglen] = arclength(coords{1}(1,:),...
        coords{1}(2,:),coords{1}(3,:),'spline');
    al = mean(seglen);
    
    mat_sig = sigma{1};
    dom = domain{1};
        
    distance_along_arc = cumsum([0; seglen]);
    normalized_al = 100.*distance_along_arc./max(distance_along_arc);
    %% Non Normalized AF
    figure(f1);
    
    sigma_transitions = find(abs(diff(mat_sig)) > 0);
    wheretoline_sig = normalized_al(sigma_transitions);
    
    s1 = plot([wheretoline_sig';wheretoline_sig'],...
        max(abs(ybounds1)).*[wheretoline_sig'.^0+0.1;wheretoline_sig'.^0-2.1],'g--',...
        'LineWidth',3, 'DisplayName','Conductivity Transitions');
    hold on;
    
    domain_transitions = find(abs(diff(dom))> 0);
    wheretoline_dom = normalized_al(domain_transitions);
    
    d1 = plot([wheretoline_dom';wheretoline_dom'],...
        max(abs(ybounds1)).*[wheretoline_dom'.^0+0.1;wheretoline_dom'.^0-2.1],'r-.',...
        'LineWidth',1, 'DisplayName', 'Domain Transitions');
    
    %% X Component of Gradient
    figure(f2);
    s2 = plot([wheretoline_sig';wheretoline_sig'],...
        max(abs(ybounds2)).*[wheretoline_sig'.^0+0.1;wheretoline_sig'.^0-2.1],'g--',...
        'LineWidth',3, 'DisplayName', 'Conductivity Transitions');
    hold on;
    
    d2 = plot([wheretoline_dom';wheretoline_dom'],...
        max(abs(ybounds2)).*[wheretoline_dom'.^0+0.1;wheretoline_dom'.^0-2.1],'r-.',...
        'LineWidth',1, 'DisplayName', 'Domain Transitions');
    
    %% Normalized AF
    figure(f3);
    
    s3 = plot([wheretoline_sig';wheretoline_sig'],...
        max(abs(ybounds3)).*[wheretoline_sig'.^0+0.1;wheretoline_sig'.^0-2.1],'g--',...
        'LineWidth',3, 'DisplayName', 'Conductivity Transitions');
    hold on;
    
    d3 = plot([wheretoline_dom';wheretoline_dom'],...
        max(abs(ybounds3)).*[wheretoline_dom'.^0+0.1;wheretoline_dom'.^0-2.1],'r-.',...
        'LineWidth',1, 'DisplayName', 'Domain Transitions');
    
end

figure(f1);
ax = gca;
axis tight
set(ax,'Fontsize',24);
legend([h1,s1(1),d1(1)],'Location','southwest');
ylim(ybounds1);
%ylabel('Activating Function (V/m^{2})');
ylabel('Activating Function (V/m^{2})');
xlabel('Percentage along length of fiber (%)');
print('-dpng', [tempdata_address comsol_files{1} '_AF']);
savefig([tempdata_address comsol_files{1} '_AF']);

figure(f2);
ax = gca;
axis tight
set(ax,'Fontsize',24);
legend([h2,s2(1),d2(1)],'Location','southwest');
ylim(ybounds2);
ylabel('Extracellular voltage (V)');
xlabel('Percentage along length of fiber (%)');
print('-dpng',  [tempdata_address comsol_files{1} '_V']);
savefig([tempdata_address comsol_files{1} '_AF']);

figure(f3);
ax = gca;
axis tight
set(ax,'Fontsize',24);
legend([h3,s3(1),d3(1)],'Location','southwest');
ylim(ybounds3);
ylabel('Normalized Activating Function (unitless)');
xlabel('Percentage along length of fiber (%)');
print('-dpng', [tempdata_address comsol_files{1} '_AF']);
savefig([tempdata_address comsol_files{1} '_AF']);
%         clf(f1)
%         clf(f2)