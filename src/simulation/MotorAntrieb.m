set(0, 'defaultAxesFontSize', 14);
set(0, 'defaultLineLineWidth', 2);

clear;
close all;

%Eigenschaften Motor
alpha_i = 25.9e-3;
alpha_w = 1/((369/60)*2*pi);
mu_r = 0.0000;
J = 0.00000335;

R = 0.611;
L = 0.119e-3;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Variable Spannung über die Zeit mit Steigung k_p
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function f=U(t)
  
  %Spannungssteuerung
  k_p = 1/3;
  U_max = 15.8;
    
  f = U_max * t* k_p;
  
  if (f >= U_max)
    f = U_max;
  endif;
endfunction

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Drehmoment je nach Beschleunigung (Trägheitskraft)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function f=M_l(t, y)

persistent t_old = 0;
persistent y_old = 0;

%Mechanische Eigenschaften
persistent r = 11e-3;
persistent m=3;
persistent mu_reib = 0;

delta_t = t-t_old;
delta_y = y-y_old;

if (delta_t == 0)
  f = 0;
else
  %Diskrete Ableitung der Winkelgeschwindigkeit
  a_winkel = delta_y / delta_t;  
  a_tan = a_winkel *r;
  f = m*a_tan *r + mu_reib * y;
endif;
endfunction

% Anfangswerte
% y = [i, phi, phi_p]
y_0 = [0; 0; 0;];

%Koeffizienttenmatrix der DGL
A = [ (-R/L)  0   (-alpha_w/L);
      0       0   1;
      (+alpha_i/J)    0   (-1/J * ((0*2*alpha_i*alpha_w/R) + mu_r));];
     
%Strörgrössen
u = @(t, y_3) [ U(t)/L; 0; 1/J*(((0*2*alpha_i*U(t))/R) - M_l(t, y_3));];

%Diskrete Ableitungsfunktion
y_p = @(t, y) A*y + u(t, y(3));     

%lösen der DGL
start = 0;
ende = 5;
[t, y] = ode45(y_p, [start ende], y_0);%, odeset("InitialStep", 0.5, "MaxStep", 5));

%Nachrechnen der Spannung fürs Plotten
u_temp = zeros(rows(t),1);
for k = 1:rows(t)
  u_temp(k) = U(t(k));
endfor

%Nachrechnen des Lastmomentes fürs Plotten
M_l_temp = zeros(rows(t),1);
for k = 1:rows(t)
  M_l_temp(k) = M_l(t(k), y(k,3));
endfor

%Nachrechnen der Zugsgeschweindigkeit fürs Plotten
v_temp = zeros(rows(t),1);
for k = 1:rows(t)
  v_temp(k) = y(k,3) * 11e-3 /2; % '/2' wegen Übersetzung
endfor


figure(1)
hold on;
plot(t, y(:,1));
plot(t, u_temp);
plot(t, M_l_temp);
plot(t, v_temp);
legend('i' ,'u', 'M_l', 'v');
hold off

