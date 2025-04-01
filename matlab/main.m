% ------------------------------------------------------------------------------
% POLIPHONE Code
%
% This code is provided in connection with the article:
%
%   "POLIPHONE: A Dataset for Smartphone Model Identification from Audio Recordings"
%   Davide Salvi, Daniele Ugo Leonzio, Antonio Giganti, Claudio Eutizi, 
%   Sara Mandelli, Paolo Bestagini, and Stefano Tubaro.
%   IEEE Access, 2025. DOI: 10.1109/ACCESS.2025.3545152
%
% Copyright (c) 2025 by the authors. All rights reserved.
%
% Redistribution and use in source and binary forms, with or without 
% modification, are permitted for non-commercial research purposes provided 
% that the original authors and the source publication are credited appropriately.
%
% For any commercial use, please contact the copyright holders.
%
% This software is provided "as is" without any express or implied warranty.
% ------------------------------------------------------------------------------

% Main code to generate SWEEP and TEST audio data

clear all
clc
close all

%% Generate sweep

f1 = 20;
f2 = 20000;
FS = 44100;
T = 5;
tail = 0;
magSpect = 0;

[sweep, invsweepfft, sweepRate] = synthSweep(T,FS,f1,f2,tail,magSpect);


%% PROCESS CLEAN SWEEP

[audio,fs_clean] = audioread('/path/to/folder/sweep.wav');

spike_sample = 10584;
silence = 0.2 * fs_clean;
sweep_dur = 5.05 * fs_clean;

audio = audio(spike_sample+silence:spike_sample+silence+sweep_dur);

plot_RIR(audio, invsweepfft, 'CLEAN');



%% PROCESS RECORDED TRACK

[audio_rec,fs] = audioread('/path/to/recorded/sweep.wav');

spike_sample = 9263000;
silence = 0.25 * fs;
sweep_dur = 5 * fs;

security_factor = 0.05 * fs;

fs_clean = fs_clean(spike_sample+silence-security_factor:security_factor+spike_sample+silence+sweep_dur);

figure()
plot(audio_rec)

[irLin_rec, irNonLin_rec] = extractirsweep(audio_rec, invsweepfft);

figure()
subplot(121)
plot(irLin_rec)
subplot(122)
plot(irNonLin_rec)

