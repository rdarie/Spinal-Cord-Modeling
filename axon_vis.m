function [ output_args ] = axon_vis( n_amps, n_nodes )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
close all;
system_id_old;

dt = 0.025;
cmp = parula(8);
cutoff = 400/dt;
for a = 1:n_amps
    f1 = rfig();
    hold on;
    f2 = rfig();
    f3 = rfig();
    dispim = [];
    %title(sprintf('Amplitude %d',a));
    
        v_filename = [vtraces_address 'Mn_v_' num2str(a-1)...
            '.dat'];
        [vtrace,~]=nrn_vread(v_filename,'n');
        t = (0:(length(vtrace)-1)).*dt;
        figure(f1);
        h2 = plot3(t(cutoff:end),t(cutoff:end).^0.*0,...
            vtrace(cutoff:end),'Color',cmp(5,:),'LineWidth',5,...
            'DisplayName','Motoneuron');
        
        tstimon = t(cutoff:end);
        stimon = zeros(1,length(tstimon));
        stim_time = 2500;
        stim_int = 100;
        stim_pw = 20;
        
        d = find(tstimon==stim_time,1);
        e = find(tstimon==stim_time+stim_pw,1);
        while d
            stimon(d:e) = 1;
            stim_time = stim_time + stim_int;
            d = find(tstimon==stim_time,1);
            e = find(tstimon==stim_time+stim_pw,1);
        end
        
    for c = 1:1:n_nodes
        v_filename = [vtraces_address 'Ia_v_' num2str(a-1)...
            '_node_' num2str(c-1) '.dat'];
        [vtrace,~]=nrn_vread(v_filename,'n');
        t = (0:(length(vtrace)-1)).*dt;
        figure(f1);
        h1 = plot3(t(cutoff:end),t(cutoff:end).^0.*c,...
            vtrace(cutoff:end),'Color',cmp(3,:),'LineWidth',1,...
            'DisplayName','Ia Fiber');
        dispim = [dispim;  vtrace(cutoff:end)'];
    end

    figure(f1);
    view([-10 30]);
    zlim([-100 0]);
    xlim([3050 3800]);
    ax = gca;
    legend([h1 h2],0);
    set(ax,'FontSize',20);
    ax.TickLabelInterpreter = 'latex';
    ax.YAxisLocation = 'right';
    xlabel('Time(msec)');
    ylabel('Node \#');
    zlabel('Membrane potential (mV)');
    %% Surface plot
    figure(f2);
    [X,Y] = meshgrid(t(cutoff:end),1:n_nodes);
    h = surf(X,Y,dispim);
    axis tight
    xlim([3050 3800]);
    set(h,'LineStyle','none')
    view([0 90])
    set(gca,'XTickLabel','', ...
    'YTickLabel','');
    colorbar('TickLabels','')
    %%
    v_filename = [vtraces_address 'Mn_v_' num2str(0)...
            '.dat'];
        [vtrace,~]=nrn_vread(v_filename,'n');
        t = (0:(length(vtrace)-1)).*dt;
        tplot = t(cutoff:end);
    figure(f3);   
    ha = tight_subplot(3, 1, 0.05, 0.05, 0.05);
    
    % axon voltage
    axes(ha(1));hold on;
    axtrace = plot(tplot, dispim(29,:),'Color',cmp(3,:),'DisplayName','Ia Fiber');
    %xlim([3050 3800]);
    % motorneuron voltage
    %axes(ha(3));
    motrace = plot(tstimon(stimon>0), 20.*stimon(stimon>0),'r-','DisplayName','Stimulation');
    stimtrace = plot(tplot, vtrace(cutoff:end),'Color',cmp(5,:),'DisplayName','Motoneuron');
    hold on;
    xlim([3050 3800]);
    axes(ha(2));
    plot(1:n_nodes, dispim(:,2810/dt),'Color',cmp(3,:));
    xlim([0 42]);
    legend([axtrace motrace stimtrace]);
end