%clear;clc;
close all;
set(0,'defaultAxesFontName', 'Microsoft Sans Serif')

system_id;
comsol_files = {'move_root_move_root_points_cs.mat'};

axon_files = {'E:\Google Drive\Github\tempdata\model_tree.neu',...
    };

cmp = parula(8);
%points where action potential was initialized
init_points = [0.4267];

% fiber length, can get from get_spline_voltages.m on line 12
spl_len = [43306];

rfig();
hold on;

for a = 1
load([tempdata_address comsol_files{a}]);
spl = simulation{1}.coords;        
%comsol_file = 'A:\CSN - Corticospinal Neuroprosthetics\CSP Model\Spinal cord models\No root\no_root_HiRes';

nice_colors = parula(21);

hold on;
[tree, name, path] = load_tree(axon_files{a});

ax = gca;

options = {['']};
plot_tree(tree{1},cmp(5,:),[],[],[],'-p -thick');
plot_tree(tree{2},cmp(3,:),[],[],[],'-p -extrathick');

% plot stimulation point
%coord = floor(spl_len(a).*init_points(a));
%plot3(spl(1,coord),spl(2,coord),spl(3,coord),'k*');
end
%view(3);
% zlim([-2.5e4 -1e4])
grid off;
axis tight;
view([-128 -75]);
axis off;
whitebg
%ax.TickLabelInterpreter = 'tex';
% xlabel('x (mm)');
% ylabel('y (mm)');
% zlabel('z (mm)');
screen2png([tempdata_address 'axon_view']);

