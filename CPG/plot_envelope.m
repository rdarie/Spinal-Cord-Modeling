function plot_envelope(pop_name,dt,tstop)

close all;

if nargin == 3
    system_id;
    load([tempdata_address pop_name]);
else
    load('E:\Google Drive\CSP\2812V Model Data\pop_test.mat');
    dt = 0.025;
    tstop = 30000;
end
%

dec_factor = 5;

t = (0:dt*dec_factor:tstop).*1e-3;

rasters = zeros(1,length(t)-1);
fr = zeros(1,length(t)-1);
tot_rasters = zeros(1,length(t)-1);

f1 = rfig();

smooth_kernel = normpdf(-200:200, 0, 150);
smooth_kernel = smooth_kernel ./ sum(smooth_kernel);

ISI = [];

for a = 1:length(MN_F_v)
    
    trace = MN_E_v{a}(1:dec_factor:length(MN_F_v{a}));
    
    plot(t,trace);
    hold on;
    
    [~, locs] = findpeaks(trace,'minpeakheight',-20);
    spike_times = t(locs);
    
    plot(spike_times,trace(locs),'ro');
    ISI = [ISI diff(spike_times)];
    
    rasters = histcounts(spike_times,t);
    fr = fr + conv(rasters, smooth_kernel,'same')./length(MN_F_v);
    
    tot_rasters = tot_rasters + rasters;
    
end

f2 = rfig();
histogram(ISI(ISI < 0.2),25,'Normalization','pdf');

[~,edges] = histcounts(ISI(ISI < 0.2),25);
hold on;
pd = fitdist(ISI(ISI < 0.2)','Normal')
y = pdf(pd,edges);
plot(edges,y);

    rfig();
    plot(t(1:end-1),fr);
    
    burst_times = t(find(tot_rasters,1));
    
    for a = 1:length(tot_rasters)
        if (tot_rasters(a)) & t(a) > burst_times(end) + 0.3
            burst_times = [burst_times t(a)];
        end
    end
    
figure(f1);
plot(burst_times,-40.*burst_times.^0,'gd');

rfig();
burst_isi = diff(burst_times);
histogram(burst_isi,25);
[~,edges] = histcounts(burst_isi,25);
hold on;
pd = fitdist(burst_isi','Normal')
y = pdf(pd,edges);
plot(edges,y);
end