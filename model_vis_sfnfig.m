%clear;clc;
close all;
set(0,'defaultAxesFontName', 'Microsoft Sans Serif')

system_id_old;
comsol_files = {'5M mesh\move_root_um_altelmoved_axon_centers_cs.mat',...
    '5M mesh\one_root_um_altelaxon_centers_cs.mat'};

axon_files = {'E:\Google Drive\CSP\SfN 2015 Poster\moved_tree.neu',...
    'E:\Google Drive\CSP\SfN 2015 Poster\straight_tree.neu'};

cmp = parula(8);
init_points = [0.4267 0.2581];
spl_len = [44044 43043];
rfig();
hold on;
for a = 1:2
load([tempdata_address comsol_files{a}]);
spl = coords{1};        
%comsol_file = 'A:\CSN - Corticospinal Neuroprosthetics\CSP Model\Spinal cord models\No root\no_root_HiRes';

nice_colors = parula(21);

hold on;
[tree, name, path] = load_tree(axon_files{a});

ax = gca;

options = {['']};
plot_tree(tree{1},cmp(5,:),[],[],[],'-p -thick');
plot_tree(tree{2},cmp(3,:),[],[],[],'-p -extrathick');

coord = floor(spl_len(a).*init_points(a));
plot3(spl(1,coord),spl(2,coord),spl(3,coord),'k*');
end
% view(3);
% zlim([-2.5e4 -1e4])
grid off;
axis tight;
view([0 0]);
axis off;
whitebg
%ax.TickLabelInterpreter = 'tex';
% xlabel('x (mm)');
% ylabel('y (mm)');
% zlabel('z (mm)');
screen2png([tempdata_address 'axon_view']);

