function [V_extra,d2V_ds2, domain, mat_sigma, spl] =...
    get_spline_voltages(fem,get_v_extra, get_d2v_ds,geom,pointlist,datadir,plotting,inl,ppn,diam,start_offset)
%get_line_voltages.m Generate text file list of voltage values
%for NEURON communication

% fem is the comsol model object
% N is the number of diameters to simulate

pts = csvread(pointlist);
pts = pts';

fib_len = arclength(pts(1,:),pts(2,:),pts(3,:),'spline');
n_nodes = floor((fib_len)./(diam*(inl+1)));
% how many nodes and paranodes does the axon have.

arc_node_length = 1./n_nodes;
arc_offset = start_offset.*1e-2.*arc_node_length;
s = linspace(0+arc_offset,1-arc_node_length+arc_offset,ppn*n_nodes);

spl = interparc(s,pts(1,:),pts(2,:),pts(3,:),'spline'); % a 3-d curve
spl = spl';

if plotting
    figure;
    hold on
    plot3(spl(1,:),spl(2,:),spl(3,:),'r*-');
    get_geom_names;
    
    %% View Geometry
    nice_colors = parula(21);
    ax = gca;
    
    % Plot WM
    
    %edges
    mphviewselection(fem,geom,wm_edge, ...
        'entity', 'edge', ...
        'parent',ax, ...
        'facemode', 'off', ...
        'geommode', 'off', ...
        'edgemode', 'on', ...
        'edgecolorselected', [0 0 0], ...
        'edgecolor', [0 0 0] ...
        );
    
    xlabel('x (um)');
    ylabel('y (um)');
    zlabel('z (um)');
    print('-dpng',[datadir 'figures\last_axon']);
end

if get_v_extra
    V_extra = mphinterp(fem,'V','coord',spl,...
        'recover','pprint',...
        'edim','domain',...
        'Complexout','off',...
        'Differential','on',...
        'Evalmethod','harmonic',...
        'Ext',0.1);
else
    V_extra = [];
end

if get_d2v_ds
    
    d2V_ds2 = zeros(size(spl));
    d2V_ds2(1,:) = mphinterp(fem,'Vxx','coord',spl,...
        'Recover','pprint','Differential','on','Ext',1);
    
    d2V_ds2(2,:) = mphinterp(fem,'Vyy','coord',spl,...
        'Recover','pprint','Differential','on','Ext',.1);
    
    d2V_ds2(3,:) = mphinterp(fem,'Vzz','coord',spl,...
        'Recover','pprint','Differential','on','Ext',.1);
    
else
    d2V_ds2 = [];
end
% interpolate voltages from the COMSOL solution
domain = mphinterp(fem,'dom','coord',spl);
% get domain names
%mat_sigma = mphinterp(fem,'ec.sigmaxx','coord',spl);
 mat_sigma = zeros(size(spl));
    mat_sigma(1,:) = mphinterp(fem,'ec.sigmaxx','coord',spl);
    
    mat_sigma(2,:) = mphinterp(fem,'ec.sigmayy','coord',spl);
    
    mat_sigma(3,:) = mphinterp(fem,'ec.sigmazz','coord',spl);
end
