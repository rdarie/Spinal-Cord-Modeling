clear;clc;close all;

start_time = 250; % when to start stimulation (ms)

dur_time = 0.5;% how long is the stimulation on (ms)
interval_time = 200 - dur_time;% how long is the stimulation off (ms)
% together, these last two determine the waveform/duty cycle of the square
% wave that stimulates the fiber.

ampstart = 1;
ampmax = 1;
stepsize = 1;
ppn = 1e2+1;
inl = 100;

recruitment('5M mesh\no_root_um_axon_centers_cs', start_time, dur_time,...
    interval_time, ampstart, ampmax, stepsize, ppn, inl);