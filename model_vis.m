%clear;clc;
close all;
set(0,'defaultAxesFontName', 'Microsoft Sans Serif')
fname = 'move_root_um';
system_id;
comsol_file = [comsol_folder fname];
%comsol_file = 'A:\CSN - Corticospinal Neuroprosthetics\CSP Model\Spinal cord models\No root\no_root_HiRes';
%fem = mphload([comsol_file '.mph']);
geom = 'geom1';

%system_id_old;
get_geom_names;
nice_colors = parula(21);
rfig();
hold on;
[tree, name, path] = load_tree([tempdata_address 'model_tree.neu']);

ax = gca;

% %Plot Electrode
% %edges
mphviewselection(fem,geom,el_edge, ...
    'entity', 'edge', ...
    'parent',ax, ...
    'facealpha', 0, ...
    'geommode', 'off', ...
    'edgemode', 'on', ...
    'edgecolorselected', [1 1 1], ...
    'edgecolor', [1 1 1] ...
    );

% %faces
% mphviewselection(fem,geom,el_dom, ...
%     'entity', 'domain', ...
%     'parent',ax, ...
%     'facealpha', 1, ...
%     'facecolor', [1 0 0], ...
%     'facecolorselected', nice_colors(1,:), ...
%     'geommode', 'off', ...
%     'edgemode', 'on', ...
%     'edgecolorselected', 'k', ...
%     'edgecolor', 'k' ...
%     );

% %Plot GM
% 
% %edges
mphviewselection(fem,geom,gm_edge, ...
    'entity', 'edge', ...
    'parent',ax, ...
    'facemode', 'off', ...
    'geommode', 'off', ...
    'edgemode', 'on', ...
    'edgecolorselected', [1 1 1], ...
    'edgecolor', [1 1 1] ...
    );

% %faces
% mphviewselection(fem,geom,gm_dom(1:6), ...
%     'entity', 'domain', ...
%     'parent',ax, ...
%     'facealpha', 0.1, ...
%     'facecolor', [1 0 0], ...
%     'facecolorselected', nice_colors(1,:), ...
%     'geommode', 'off', ...
%     'edgemode', 'on', ...
%     'edgecolorselected', 'k', ...
%     'edgecolor', 'k' ...
%     );
% %faces
% mphviewselection(fem,geom,gm_dom(7:end), ...
%     'entity', 'domain', ...
%     'parent',ax, ...
%     'facealpha', 0.1, ...
%     'facecolor', [1 0 0], ...
%     'facecolorselected', nice_colors(1,:), ...
%     'geommode', 'off', ...
%     'edgemode', 'on', ...
%     'edgecolorselected', 'k', ...
%     'edgecolor', 'k' ...
%     );
% 
% % Plot WM
% 
% %edges
mphviewselection(fem,geom,wm_edge, ...
    'entity', 'edge', ...
    'parent',ax, ...
    'facemode', 'off', ...
    'geommode', 'off', ...
    'edgemode', 'on', ...
    'edgecolorselected', [1 1 1], ...
    'edgecolor', [1 1 1] ...
    );
% 
% %faces
% mphviewselection(fem,geom,wm_dom(1:6), ...
%     'entity', 'domain', ...
%     'parent',ax, ...
%     'facealpha', 0.1, ...
%     'facecolor', [1 0 0], ...
%     'facecolorselected', nice_colors(5,:), ...
%     'geommode', 'off', ...
%     'edgemode', 'on', ...
%     'edgecolorselected', 'k', ...
%     'edgecolor', 'k' ...
%     );
% %faces
% mphviewselection(fem,geom,wm_dom(7:end), ...
%     'entity', 'domain', ...
%     'parent',ax, ...
%     'facealpha', 0.1, ...
%     'facecolor', [1 0 0], ...
%     'facecolorselected', nice_colors(5,:), ...
%     'geommode', 'off', ...
%     'edgemode', 'on', ...
%     'edgecolorselected', 'k', ...
%     'edgecolor', 'k' ...
%     );
% 
% % CSF
% 
% %edges
mphviewselection(fem,geom,csf_edge, ...
    'entity', 'edge', ...
    'parent',ax, ...
    'facemode', 'off', ...
    'geommode', 'off', ...
    'edgemode', 'on', ...
    'edgecolorselected', [1 1 1], ...
    'edgecolor', [1 1 1] ...
    );
% 
% %faces
% mphviewselection(fem,geom,csf_dom(1:6), ...
%     'entity', 'domain', ...
%     'parent',ax, ...
%     'facealpha', 0.1, ...
%     'facecolor', [1 0 0], ...
%     'facecolorselected', nice_colors(10,:), ...
%     'geommode', 'off', ...
%     'edgemode', 'on', ...
%     'edgecolorselected', 'k', ...
%     'edgecolor', 'k' ...
%     );
% %faces
% mphviewselection(fem,geom,csf_dom(7:end), ...
%     'entity', 'domain', ...
%     'parent',ax, ...
%     'facealpha', 0.1, ...
%     'facecolor', [1 0 0], ...
%     'facecolorselected', nice_colors(10,:), ...
%     'geommode', 'off', ...
%     'edgemode', 'on', ...
%     'edgecolorselected', 'k', ...
%     'edgecolor', 'k' ...
%     );
options = {['']};
plot_tree(tree{1},[1 0 0],[],[],[],'-p -thick');
plot_tree(tree{2},[1 0 0],[],[],[],'-p -extrathick');
%plot3(-72829.2057,-117390.9301,158484.5581, 'k*');
% view(3);
axis tight;
zlim([1e4 2.6e4])
grid on;
%axis equal;
%zlim([1.5e5 1.75e5]);
%view([190 30]);

view([35 -10]);
%axis off;
whitebg

% set(ax,'FontSize',20);
% set(gca,'XTick',[-8:1:-6].*1e4)
% set(gca,'XTickLabel',{''; ''; ''})
% set(gca,'YTick',[-12:1:-11].*1e4)
% set(gca,'YTickLabel',{''; ''})
% set(gca,'ZTick',[14:1:17].*1e4)
% set(gca,'ZTickLabel',{'';'';'';''})
ax.TickLabelInterpreter = 'tex';
xlabel('x (\mum)');
ylabel('y (\mum)');
zlabel('z (\mum)');
set(gca,'FontSize',10)
screen2png([tempdata_address 'axon_view']);

