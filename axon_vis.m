function [ output_args ] = axon_vis( n_amps, n_nodes )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

system_id_old;

dt = 0.025;
cmp = parula(8);

for a = 1:n_amps
    rfig();
    title(sprintf('Amplitude %d',a));
    hold on;
    for b = 1:n_nodes
        v_filename = [vtraces_address 'Ia_v_' num2str(a-1)...
            '_node_' num2str(b-1) '.dat'];
        [vtrace,~]=nrn_vread(v_filename,'n');
        t = (0:(length(vtrace)-1)).*dt;
        plot3(t,t.^0.*b,vtrace,'Color',cmp(3,:));
    end
    view([0 10]);
end