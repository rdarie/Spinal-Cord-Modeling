function activating_function_plot(fnames)

system_id;

plot_colors = parula(16);
f1 = rfig();
hold on;
f2 = rfig();
hold on;
f3 = rfig();
hold on;

ybounds = [0 0; 0 0; 0 0];

for a = 1:length(fnames)
    load([tempdata_address fnames{a} '.mat']);
    for b = 1:size(simulation,1)
        for c = 1:size(simulation,2)
            % arclen = total arc length of this axon
            % seglen = length of each segment
            [arclen,seglen] = arclength(simulation{b,c}.coords(1,:),...
                simulation{b,c}.coords(2,:),simulation{b,c}.coords(3,:),'spline');
            
            tang = zeros(size(simulation{b,c}.coords)); % tangent to each point
            for d = 1:size(simulation{b,c}.coords,2)-1
                tang(:,d) = simulation{b,c}.coords(:,d+1) - simulation{b,c}.coords(:,d);
                tang(:,d) = tang(:,d) ./ norm(tang(:,d));
            end
            tang(:,size(simulation{b,c}.coords,2)) = tang(:,c);
            
            % cathodic stimulus?
            cathodic = -1;
            
            % dot product between second derivative of voltage and tangents
            % to the axon
            af = cathodic .* dot(tang,simulation{b,c}.d2V_ds2);
            
            distance_along_arc = cumsum([0; seglen]);
            normalized_al = 100.*distance_along_arc./max(distance_along_arc);
            
            cl = plot_colors(b+c,:); % plot colors
            %% Non Normalized Activating function
            figure(f1);
            
            h1(a) = plot(normalized_al,af,'k-'...
                , 'DisplayName', simulation{b,c}.tag,'LineWidth',3);
            h1(a).Color = cl;
            a1 = plot(normalized_al(find(af == max(af),1)), af(find(af == max(af),1)),'r*','MarkerSize',10);
            a1.Color = cl;
            ybounds(1,:) = [min(min(af),ybounds(1,1)),max(max(af),ybounds(1,2))];
            %% X Component of Gradient
            figure(f2);
            h2(a) = plot(normalized_al,simulation{b,c}.d2V_ds2(1,:),'k-'...
                , 'DisplayName', simulation{b,c}.tag,'LineWidth',1);
            h2(a).Color = cl;
            
            ybounds(2,:) = [min(min(simulation{b,c}.d2V_ds2(1,:)),ybounds(2,1)),max(max(simulation{b,c}.d2V_ds2(1,:)),ybounds(2,2))];
            %% Normalized AF
            figure(f3);
            normalized_af = af./max(af);
            h3(a) = plot(normalized_al,normalized_af,'k-'...
                , 'DisplayName', simulation{b,c}.tag,'LineWidth',3);
            
            h3(a).Color = cl;
            
            ybounds(3,:) = [min(min(normalized_af),ybounds(3,1)),max(max(normalized_af),ybounds(3,2))];
        end
    end
end

figure(f1);
ax = gca;
axis tight
set(ax,'Fontsize',24);
legend([h1(1)],'Location','southwest');
ylim(ybounds(1,:));

ylabel('Activating Function (V/m^{2})');
xlabel('Percentage along length of fiber (%)');
print('-dpng', [tempdata_address 'figures\' fnames{1} '_AF']);
savefig([tempdata_address 'figures\' fnames{1} '_AF']);

figure(f2);
ax = gca;
axis tight
set(ax,'Fontsize',24);
legend([h2(1)],'Location','southwest');
ylim(ybounds(2,:));
ylabel('Activating Function x component (V/m^{2})');
xlabel('Percentage along length of fiber (%)');
print('-dpng',  [tempdata_address 'figures\' fnames{1} '_d2Vdx2']);
savefig([tempdata_address 'figures\' fnames{1} '_d2Vdx2']);

figure(f3);
ax = gca;
axis tight
set(ax,'Fontsize',24);
legend([h3(1)],'Location','southwest');
ylim(ybounds(3,:));
ylabel('Normalized Activating Function (unitless)');
xlabel('Percentage along length of fiber (%)');
print('-dpng', [tempdata_address 'figures\' fnames{1} '_AFnorm']);
savefig([tempdata_address 'figures\' fnames{1} '_AFnorm']);
end