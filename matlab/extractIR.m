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

function [irLin, irNonLin] = extractIR(sweep_response, invsweepfft)

% EXTRACTIR Extract impulse response from swept-sine response.
%   [irLin, irNonLin] = extractIR(sweep_response, invsweepfft) 
%   Extracts the impulse response from the swept-sine response.  Use
%   synthSweep.m first to create the stimulus; then pass it through the
%   device under test; finally, take the response and process it with the
%   inverse swept-sine to produce the linear impulse response and
%   non-linear simplified Volterra diagonals.  The location of each
%   non-linear order can be calculated with the sweepRate - this will be
%   implemented as a future revision.

if(size(sweep_response,1) > 1)
    sweep_response = sweep_response';
end

N = length(invsweepfft);
sweepfft = fft(sweep_response,N);

% convolve sweep with inverse sweep (freq domain multiply)

ir = real(ifft(invsweepfft.*sweepfft));

ir = circshift(ir', length(ir)/2); 

irLin = ir(end/2+1:end);
irNonLin = ir(1:end/2);
