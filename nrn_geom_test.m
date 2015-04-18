clear; clc; close all;

npts = 13;
t = linspace(0,8*pi,npts);
z = linspace(-1,1,npts);
omz = sqrt(1-z.^2);
xyz = [cos(t).*omz; sin(t).*omz; z];
plot3(xyz(1,:),xyz(2,:),xyz(3,:),'ro','LineWidth',2);
text(xyz(1,:),xyz(2,:),xyz(3,:),[repmat('  ',npts,1), num2str((1:npts)')])
ax = gca;
ax.XTick = [];
ax.YTick = [];
ax.ZTick = [];
box on

spl_func = cscvn(xyz(:,[1:end])); %interpolates spline through pts
hold on
fnplt(spl_func,'r',2) %visuals
hold off

inl = 100;
% how many times longer is a paranode than a node?
diam = log(random('logn', 9, 0.2, 1, 1)).*1e-3; %stats toolbos
n_nodes = floor((spl_func.breaks(end)-spl_func.breaks(1))./(diam*inl));
%breaks are along length of linear line
% how many nodes and paranodes does the axon have.

points_per_node = 10;
s = linspace(spl_func.breaks(1),spl_func.breaks(end),points_per_node*n_nodes);
spl = fnval(spl_func,s); %fnval = xyz coords of 10 pts along node
hold on
plot3(spl(1,:),spl(2,:),spl(3,:),'ko');


nrn_geom(spl, diam, n_nodes, points_per_node);