function plot_envelope(fold_name, pop_name,dt,tstop)

close all;

plot_colors = {...
    [0    0.4470    0.7410],...
    [0.8500    0.3250    0.0980],...
    [0.9290    0.6940    0.1250],...
    [0.4660    0.6740    0.1880],...
    [0.4940    0.1840    0.5560]
};

if nargin == 4
    load([fold_name pop_name]);
else
    load('C:\Users\Radu Darie\Google Drive\Classes\APMA2821V\Final Project\pop_test2_d_ib_5.0000.mat');
    dt = 0.025;
    tstop = 30000;
end
%

dec_factor = 5;

t = (0:dt*dec_factor:tstop).*1e-3;

F_rasters = zeros(1,length(t)-1);
F_fr = [];
F_tot_rasters = zeros(1,length(t)-1);
E_rasters = zeros(1,length(t)-1);
E_fr = [];
E_tot_rasters = zeros(1,length(t)-1);

smooth_sigma = 5e-3; % standard deviation of smooth kernel, in sec
smooth_edges = [-3*smooth_sigma:dt.*1e-3:3*smooth_sigma];
smooth_kernel = normpdf(smooth_edges, 0, smooth_sigma);
smooth_kernel = smooth_kernel ./ sum(smooth_kernel);

F_ISI = [];
f1 = rfig();
for a = 1:length(MN_F_v)
    
    F_trace = MN_F_v{a}(1:dec_factor:length(MN_F_v{a}));
    E_trace = MN_E_v{a}(1:dec_factor:length(MN_E_v{a}));
    
    plot(t,F_trace,'Color',plot_colors{4});
    hold on;
    plot(t,E_trace,'Color',plot_colors{1});
    
    [~, locs] = findpeaks(F_trace,'minpeakheight',-20);
    F_spike_times = t(locs);
    [~, locs] = findpeaks(E_trace,'minpeakheight',-20);
    E_spike_times = t(locs);
    
    F_ISI = [F_ISI diff(F_spike_times)];
    E_ISI = [F_ISI diff(F_spike_times)];
    
    F_rasters = histcounts(F_spike_times,t);
    F_fr = [F_fr; conv(F_rasters, smooth_kernel,'same')./(dec_factor.*dt.*1e-3)];
    E_rasters = histcounts(E_spike_times,t);
    E_fr = [E_fr; conv(E_rasters, smooth_kernel,'same')./(dec_factor.*dt.*1e-3)];
    
    F_tot_rasters = F_tot_rasters + F_rasters;
    E_tot_rasters = E_tot_rasters + E_rasters;
    
end

f2 = rfig();
h1 = histogram(F_ISI(F_ISI < 0.2),25,'Normalization','pdf','DisplayName','Flexor');
hold on;
h2 = histogram(E_ISI(E_ISI < 0.2),25,'Normalization','pdf','DisplayName','Extensor');

[~,edges] = histcounts(F_ISI(F_ISI < 0.2),25);
hold on;
legend([h1 h2]);

rfig();
plot(t(1:end-1),mean(F_fr),'Color',plot_colors{4},'LineWidth',3);
hold on;
plot(t(1:end-1),mean(E_fr),'Color',plot_colors{1},'LineWidth',3);
xlabel('Time (s)');
legend('Flexor','Extensor');
ylabel('Firing Rate (Hz)');
xlim([tstop.*1e-3-10 tstop.*1e-3]);
ylim([0 40]);

%% Burst Statistics
% burst_times = t(find(E_tot_rasters,1));
% burst_cutoff = 0.1;
% a = find(E_tot_rasters,1)+1;
% 
% while a < length(E_tot_rasters)
%     
%     if E_tot_rasters(a)
%         curr_spike_time = t(a);
%         
%         last_spike_time = t(1:end-1);
%         last_spike_time = last_spike_time(logical(E_tot_rasters'));
%         last_spike_time = last_spike_time(last_spike_time < curr_spike_time);
%         last_spike_time = last_spike_time(end);
%         
%         if curr_spike_time > last_spike_time + burst_cutoff
%             burst_times = [burst_times curr_spike_time];
%             a = a + 0.2 ./ (dt * 1e-3) - 1;
%         end
%         
%     end
%     
%     a = a + 1;
% end
[~,burst_times] = findpeaks(mean(F_fr),t(1:end-1),...
    'MinPeakDistance',0.6, 'MinPeakHeight', 20);
figure(f1);
plot(burst_times,-40.*burst_times.^0,'gd');

rfig();
burst_isi = diff(burst_times);
histogram(burst_isi,5);
[~,edges] = histcounts(burst_isi,5);
hold on;
fprintf('Burst Occurence Rate');
pd = fitdist(burst_isi','Normal')
y = pdf(pd,edges);
plot(edges,y);
end