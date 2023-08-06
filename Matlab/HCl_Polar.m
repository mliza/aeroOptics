% Aero-Optics
% Determine of HCl polarizibility using approach similar to Buldakov

double precision 

clear
clc
close all

B_e = 10.593416; % [cm^-1]. From NIST/2T code.



alpha_e = 0.307181; % [cm^-1]. rotational constant ? first term. From NIST.
omega_e = 2990.9463; % [cm^-1.] vibrational constant ? first term. From NIST
omega_e_x_e = 52.8186; % [cm^-1]. 	vibrational constant ? second term. From NIST.
omega_e_y_e = 0.22437; % [cm^-1]. 	vibrational constant ? second term. From NIST.
D_e = 5.3194E-4; % [cm^-1]. 	vibrational constant ? second term. From NIST.

a1 = -alpha_e * omega_e / (6 * B_e^2)-1; % Dunham Approx.
a2 = (5/4) * a1^2 - (2/3) * (omega_e_x_e / B_e); % Herschbach
%a3 = (2*omega_e^2/B_e^2 + 15 + 14 * a1 - 9 * a2 - 23*a1*a2 + 21 * (a1^2 + a1^3)/2) / (-15);

a3 = (144*B_e^7 + (8064*a1^3-2313*a1^4 + 5544*a1^2 * (2+a2) -64 * a1 * (-199 + 207 * a2) + 16 * (652 - 476 * a2 + 31 * a2^2))*B_e^5 * omega_e + 128 * B_e^3 * omega_e^3 - 32 * D_e * omega_e^5 - 288 * B_e^5 * omega_e * omega_e_y_e )/ ...
    (320*(-18+11*a1)*B_e^5 * omega_e);

a1 = -2.364256;
a2 = 3.66285;
a3 = -4.7076;
a4 = 5.2126;

Y30 = (B_e^2 / (2 * omega_e)) * (10 * a4 - 35 * a1 * a3 - 17 * a2^2/2 + 225*a1^2*a2/4 - 705* a1^4/32);