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
 
function [ir] = extractirnoise(x, y, nfft)

% EXTRACTIRNOISE 
% This function compute the transfer function of between a white noise
% source and the measurement point. The transfer function H is compute in
% the frequency domain as a simple deconvolution. The impulse response is
% obtained as the inverse fourier transform of H.

X = fft(x, nfft);
Y = fft(y, nfft);

% ifft computes a signal with a same number of samples as its input
ir = real(ifft(Y./X));
