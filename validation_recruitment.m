clear;clc; close all;

fold_name = 'A:\CSN - Corticospinal Neuroprosthetics\Raw_data&Processed_activations\';

files_to_load = {[ fold_name ...
    'Q21_6-02_trial01_recruitcurves_data.mat'],...
    [fold_name ...
    'Q21_6-02_trial09_recruitcurves_data.mat'],...
    [fold_name ...
    'Q21_6-02_trial10_recruitcurves_data.mat']};

EMG_amp = zeros(4,8);
total_EMG = [];

which_muscle = 8;

for c = 1:length(files_to_load)
    load(files_to_load{c});
    count = 1;
    for a = 1:8
        
        for b = 1:4
            
            EMG_trace = info.windoweddata{which_muscle};
            EMG_time = info.windowedtime{which_muscle};
            EMG_amp(b,a) = trapz(EMG_time(count,:),abs(EMG_trace(count,:)));
            count = count + 1;
        end
        
    end
    total_EMG = [total_EMG ; EMG_amp];
end

total_EMG = 100 .* total_EMG ./ (max(max(total_EMG)));
EMG_mean = mean(total_EMG);
EMG_std = std(total_EMG);

bound_up = EMG_mean + EMG_std;
bound_down = EMG_mean - EMG_std;

patch_x = [stimvalues fliplr(stimvalues)];
patch_y = [bound_up fliplr(bound_down)];

h1 = plot(stimvalues, total_EMG, 'k.','DisplayName','Data');
hold on;
h2 = plot(stimvalues,EMG_mean,'k-','DisplayName','Mean');
h3 = patch(patch_x,patch_y,'r','EdgeColor','none','FaceAlpha',0.5,'DisplayName','Standard Deviation');

legend([h1(1); h2; h3]);

xlabel('Stimulation Ampliude (V)');
ylabel('Integral of EMG (% of max)');