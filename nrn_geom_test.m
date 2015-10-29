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

s = linspace(0,1,500);

spl = interparc(s,xyz(1,:),xyz(2,:),xyz(3,:),'spline'); % a 3-d curve
spl = spl';
hold on;
plot3(spl(1,:),spl(2,:),spl(3,:),'k-','LineWidth',1);
hold off

inl = 100;
% how many times longer is a paranode than a node?
%diam = log(random('logn', 9, 0.2, 1, 1)).*1e-3; %stats toolbos
n_nodes = floor((spl_func.breaks(end)-spl_func.breaks(1))./(diam*inl));
%breaks are along length of linear line
% how many nodes and paranodes does the axon have.

points_per_node = 10;
offset = 5;
s = linspace(spl_func.breaks(1),spl_func.breaks(end),points_per_node*n_nodes);
ds = s(2)-s(1);
s = s + ds.*offset.*1e-2.*points_per_node;
spl = fnval(spl_func,s); %fnval = xyz coords of 10 pts along node
hold on
plot3(spl(1,:),spl(2,:),spl(3,:),'ko');


nrn_geom(spl, diam, n_nodes, points_per_node);