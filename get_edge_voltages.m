function [V_extra, coords, arc_lengths] = get_edge_voltages(fem, diam, n_nodes, inl, geom, edge)
%get_line_voltages.m Generate text file list of voltage values for NEURON communication
% fem is the comsol model object
% N is the number of diameters to simulate

c = mphgetcoords(fem, geom, 'edge', edge);
% axon lies along this edge in our model. gets the x,y,z coordinates of the 2
% points that make up edge 13.

x = c(1,2)-c(1,1);
y = c(2,2)-c(2,1);
z = c(3,2)-c(3,1);
% translate the coordinate system so that the edge starts at the origin. x,
% y, and z are the coordinates of the end of the line in this new coordinate
% system
r = sqrt((x)^2+(y)^2+(z)^2);
% the length of the edge
theta = acosd(z/r);
phi = atand(y/x);
% polar coordinate transformation, gets the orientation of the line in this
% coordinate system.
start_point = [c(1,1);
    c(2,1);
    c(3,1)];
% coordinate of the first node to evaluate

V_extra = zeros(1,2*n_nodes);
arc_lengths = zeros(1,2*n_nodes);
% preallocate vector to hold extracellular voltages for each node and paranode

arc_lengths = diam./2+(0:2*(n_nodes)-1).*(diam*(inl+1))./2;
% how far into the fiber are the node and paranode centers (arc lengths)

% the middle of the first node is at diam/2. From there on, we alternate
% between nodes and paranodes, and each one lies diam*(inl+1)/2 from the
% previous one. For instance, if diam = 2 dashes and INL = 3 we have this:
% |-*-|---*---|-*-|---*---|-*-|---*---|-*-|---*---|-*-|---*---|-*-|---*---|
% node             paranode       4 dashes between locations

coords = [start_point(1)+arc_lengths.*sind(theta).*cosd(phi);...
    start_point(2)+arc_lengths.*sind(theta).*sind(phi);...
    start_point(3)+arc_lengths.*cosd(theta)];
% rotate the collection of arc lengths into position
V_extra=mphinterp(fem,'V','coord',coords);
% interpolate voltages from the COMSOL solution

end
