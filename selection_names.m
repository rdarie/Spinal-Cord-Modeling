%clear;clc;close all;

inl = 100;
% how many times longer is a paranode than a node?

comsol_file = 'E:\Google Drive\CSP\testbed\COMSOL Trial\pieces';
%fem = mphload([comsol_file '.mph']);
geom = 'geom1';

system_id_old;
gm_dom = mphgetselection(fem.selection('sel7'));
wmc_dom = mphgetselection(fem.selection('sel10'));
wmr_dom = mphgetselection(fem.selection('sel11'));
csf_dom = mphgetselection(fem.selection('sel5'));
tiss_dom = mphgetselection(fem.selection('sel1'));
metal_dom = mphgetselection(fem.selection('sel8'));
save([tempdata_address 'sel_names_pieces.mat'], 'gm_dom',...
    'wmc_dom', 'wmr_dom', 'csf_dom', 'tiss_dom', 'metal_dom');
fprintf('Done!');