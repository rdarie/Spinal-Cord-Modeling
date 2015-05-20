clear;clc;close all;
comsol_file = 'A:\CSN - Corticospinal Neuroprosthetics\CSP Model\Spinal cord models\No root\no_root';
fem = mphload([comsol_file '.mph']);
geom = 'geom1';

system_id_old;
figure;
[tree, name, path] = load_tree([tempdata_address 'model_tree.neu']);
plot_tree(tree{1},[1 0 0]);
hold on;
plot_tree(tree{2},[1 0 0]);
mphgeom(fem,geom,'entity','domain','selection',[1],'Facealpha',0);
axis([-4000 4000 -4000 4000 -4000 10000]);


