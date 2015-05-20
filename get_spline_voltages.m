function [V_extra, domain, spl, n_nodes,diam] = get_spline_voltages(fem,datadir,inl)
%get_line_voltages.m Generate text file list of voltage values for NEURON communication
% fem is the comsol model object
% N is the number of diameters to simulate

pts = csvread([datadir 'fiber_inflection_points.csv']);
pts = pts';

spl_func = cscvn(pts(:,1:end));

% how many times longer is a paranode than a node?
diam = log(random('logn', 9, 0.2, 1, 1));
fib_len = arclength(pts(1,:),pts(2,:),pts(3,:),'spline');
n_nodes = floor((fib_len)./(diam*(inl+1)));
% how many nodes and paranodes does the axon have.

points_per_node = 21;
s = linspace(spl_func.breaks(1),spl_func.breaks(end),points_per_node*n_nodes);
spl = fnval(spl_func,s);

figure
hold on
fnplt(spl_func,'r',2)
mphgeom(fem,'geom1','entity','domain','selection',[1],'Facealpha',0);
axis([-4000 4000 -4000 4000 -4000 10000]);
view([0,0]);
xlabel('x (um)');
ylabel('y (um)');
zlabel('z (um)');
print('-dpng',[datadir 'axon_view1']);

figure;
hold on
fnplt(spl_func,'r',2)
mphgeom(fem,'geom1','entity','domain','selection',[1],'Facealpha',0);
axis([-4000 4000 -4000 4000 -4000 10000]);
view([90,90]);
xlabel('x (um)');
ylabel('y (um)');
zlabel('z (um)');
print('-dpng',[datadir 'axon_view2']);

V_extra=mphinterp(fem,'V','coord',spl);
% interpolate voltages from the COMSOL solution
domain = mphinterp(fem,'dom','coord',spl);

end
