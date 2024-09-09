% Aero-Optics
% Determine polarizibility using approach similar to Buldakov

clear
clc
close all

a_e = 1.618E-30; % [m^3]. From Ref 4 of Buldakov. Uncertainty: +/- 0.0004
a_e_1 = 1.76E-30; % [m^3]. From Ref 13 of Buldakov. Uncertainty: +/- 0.07
a_e_2 = 3.4E-30; % [m^3]. From Ref 13 of Buldakov. Uncertainty: +/- 0.4
a_e_3 = -23.7E-30; % [m^3]. From Ref 15 of Buldakov. Uncertainty: +/- ???

B_e = 1.4376766; % [cm^-1]. From NIST/2T code.

k = 1.38064852E-23; % Boltzmann consant
h = 6.62607004E-34; % Planck's consant
theta_vib = 2280; % [K]. From MGD book
we = (k/h) * theta_vib; % [Hz] Oscillating frequency. Similar as omega_e but different units.

c = 2.99792E8; % [m/s]. Speed of light. WolframAlpha

alpha_e = 0.01593; % [cm^-1]. rotational constant ? first term. From NIST.
omega_e = 1580.193; % [cm^-1.] vibrational constant ? first term. From NIST
omega_e_x_e = 11.981; % [cm^-1]. 	vibrational constant ? second term. From NIST.
omega_e_y_e = 0.04747; % [cm^-1]. 	vibrational constant ? second term. From NIST.
D_e = 4.839E-6; % [cm^-1]. 	vibrational constant ? second term. From NIST.

a1 = -alpha_e * omega_e / (6 * B_e^2)-1; % Dunham Approx.
a2 = (5/4) * a1^2 - (2/3) * (omega_e_x_e / B_e); % Herschbach
%a3 = (2*omega_e^2/B_e^2 + 15 + 14 * a1 - 9 * a2 - 23*a1*a2 + 21 * (a1^2 + a1^3)/2) / (-15);

%a3 = (144*B_e^7 + (8064*a1^3-2313*a1^4 + 5544*a1^2 * (2+a2) -64 * a1 * (-199 + 207 * a2) + 16 * (652 - 476 * a2 + 31 * a2^2))*B_e^5 * omega_e + 128 * B_e^3 * omega_e^3 - 32 * D_e * omega_e^5 - 288 * B_e^5 * omega_e * omega_e_y_e )/ ...
%    (320*(-18+11*a1)*B_e^5 * omega_e);

a3 = a1^3 * 0.35; % Ogilvie and Koo approx

%a3 = 2 * a2 * a1 - (11/12) * a1^3 + (1/4) * a1^2 + (1/6)*a1;

eps_0 = 8.8541878128E-12; % [F/m] Vaccuum permittivity

J = [5,15,21];
v = 0:1:20;

alpha = zeros(length(v),length(J));

for i = 1:length(v)
    for j = 1:length(J)
        term1 = a_e;
        term2 = 0.5 * (2*(v(i)+1)) * (-3 * a1 * a_e_1 + a_e_2) * (B_e / omega_e);
        term3 = 4 * J(j) * (J(j) + 1) * a_e_1 * (B_e / omega_e)^2;
        term4 = (a_e_1 * ((-3/8)* a1^3 * (15 * (2*v(i) + 1)^2 + 7) + a1*a2/4 * (39 * (2 * v(i) + 1)^2 + 23) - ...
        15/4 * a3 * ((2 * v(i) + 1)^2 + 5))+...
        a_e_2 * (a1^2/8 * (15 * (2*v(i)+1)^2 + 7) - 3 * a2/4 * ((2*v(i)+1)^2 + 5)) - ...
        1/24 * a_e_3 * a1 * (15 * (2*v(i)+1)^2 + 7)) * (B_e / omega_e)^2;
        term5 = (a_e_1 * (27 * a1 * (1 + a1) + 24 * (1 - a2)) - 3 * a_e_2 * (1 + 3 * a1) + (1/8) * a_e_3) * ...
        J(j) * (J(j) + 1) * (2 * v(i) + 1) * (B_e / omega_e)^3;
        
        alpha(i,j) = term1+term2+term3+term4+term5;
    end
end


%alpha(length(v),length(J))-alpha(1,1)

% Convert units
alpha_Fm = 4 * pi * eps_0 * alpha; 


x = [v', alpha(:,1)*1E30, alpha(:,2)*1E30, alpha(:,3)*1E30, alpha_Fm(:,1)*1E40, alpha_Fm(:,2)*1E40, alpha_Fm(:,3)*1E40];

save alpha.dat x -ascii

J5 = [v',alpha_Fm(:,1)];
J15 = [v',alpha_Fm(:,2)];
J21 = [v',alpha_Fm(:,3)];

writematrix(J5,'J5_buldakov.csv');
writematrix(J15,'J15_buldakov.csv');
writematrix(J21,'J21_buldakov.csv');



figure(1)
plot(alpha)

figure(2)
plot(alpha_Fm)
