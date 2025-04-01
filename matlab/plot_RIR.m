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

function [irLin, irNonLin] = plot_RIR(audio, invsweepfft, title_main)

[irLin, irNonLin] = extractirsweep(audio, invsweepfft);

% apply circshift
irLin = circshift(irLin, length(irLin)/2);
irNonLin = circshift(irNonLin, length(irNonLin)/2);

figure()
subplot(121)
plot(irLin)
title('Linear response')
subplot(122)
plot(irNonLin)
title('Non-linear response')
sgtitle(title_main);

end

