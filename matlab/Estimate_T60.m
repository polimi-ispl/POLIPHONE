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

function T60 = Estimate_T60(IR,Fs,plot_ok)
%--------------------------------------------------------------------------
% Estimate the Reverberation Time (T60)
%--------------------------------------------------------------------------
%
% Input:      IR:        room Inpulse Response
%             Fs:        sampling frequency [Hz]
%             plot_ok:   plot the Energy Decay Curve
%
% Output:     T60:       reveberation time [s]
%
%--------------------------------------------------------------------------

EDC_region = [-5,-20];   % EDC region used for line fitting [dB]

if size(IR,2) == 1
    IR = IR.';
end

% Take only the part of IR after the direct path
[~,maxIndx] = max(abs(IR));
IR = IR(maxIndx:end);

% Energy Decay Curve
EDC = zeros(size(IR));
EDC(end:-1:1) = cumsum(IR(end:-1:1).^2);
EDC_dB = 10*log10(EDC/max(EDC));

% Linear regression
EDC_dB_reg = EDC_dB(EDC_dB <= EDC_region(1) & EDC_dB >= EDC_region(2));
x = 1:length(EDC_dB_reg);
length(x);
length(EDC_dB_reg);
p = polyfit(x,EDC_dB_reg,1); 
y = p(1)*x+p(2);

% Intersection of the fitted line with -60dB
y0 = y(1) - p(1)*find(EDC_dB <= EDC_region(1), 1, 'first');
x60 = (-60-y0)/p(1);

T60 = x60/Fs;  

% Plot results
if plot_ok == 1
    linewidth = 2;
    fontsize = 14;
    
    x = 1:x60;
    y = p(1)*x+y0;
    figure
    hold on
    plot(linspace(0,length(EDC_dB)/Fs,length(EDC_dB)), EDC_dB,'-.b', 'LineWidth',linewidth);
    plot(linspace(0,length(y)/Fs,length(y)), y, '-.r', 'LineWidth',linewidth);
    line( [0 0.6*length(IR)/Fs],[EDC_region(1)  EDC_region(1)],'Color','black','LineStyle','--','LineWidth',linewidth);
    line( [0 0.6*length(IR)/Fs],[EDC_region(2)  EDC_region(2)],'Color','black','LineStyle','--','LineWidth',linewidth);
    line( [0 0.6*length(IR)/Fs],[-60 -60],'Color','black','LineStyle','--','LineWidth',linewidth);
    axis( [0 0.6*length(IR)/Fs -65 0]);
    xlabel('Time [s]','FontSize',fontsize,'fontWeight','bold');
    ylabel('Energy Decay Curve [dB]','FontSize',fontsize,'fontWeight','bold');
    legend('Energy decay curve','Linear regression')
    title('Reverberation time estimation','FontSize',fontsize,'fontWeight','bold');
    text(0.5*T60 ,-15,['Estimate of reverberation time = ',num2str(round(T60*100)/100),' [s]'],'FontSize',fontsize,'fontWeight','bold','color','k');
    set(gca,'fontsize',14,'fontWeight','bold','fontname','arial');
end
