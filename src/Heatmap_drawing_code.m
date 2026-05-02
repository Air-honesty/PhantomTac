clear all;
clc;
format long;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Step 1: Read data and generate mesh
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
num = xlsread('Sensor reverse engineering data_3mm.xlsx');
X = num(:,1);
Y = num(:,2);
Z = num(:,3);
temp_data = num(:,4);
humi_data = num(:,5);
aqi_data  = num(:,6);

min_x = -6; max_x = 6;
min_y = -6; max_y = 6;
min_z = 0;   max_z = 2;

x1 = linspace(min_x, max_x, 100);
y1 = linspace(min_y, max_y, 100);
z1 = linspace(min_z, max_z, 100);
[X1,Y1,Z1] = meshgrid(x1, y1, z1);

% Slice position
X_slice = [-3 0 3];
Y_slice = [-3 0 3];
Z_slice = [0];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Step: Plotting
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% figure1：Fx
figure('Position',[100,50,900,700],'Color','w');
F_temp = scatteredInterpolant(X,Y,Z,temp_data,'linear','none');
slice(X1,Y1,Z1,F_temp(X1,Y1,Z1),X_slice,Y_slice,Z_slice);
colormap(jet); 
shading interp; 
cb = colorbar;
view(3); 
axis equal; 
box on;

set(gca,'FontName','Times New Roman','FontSize',16);
set(cb,'FontName','Times New Roman','FontSize',16);
xlabel('X Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
ylabel('Y Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
zlabel('Z Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
title('Distribution of Fx','FontSize',20,'FontWeight','bold','FontName','Times New Roman');

% figure2：Fy
figure('Position',[250,50,900,700],'Color','w');
F_humi = scatteredInterpolant(X,Y,Z,humi_data,'linear','none');
slice(X1,Y1,Z1,F_humi(X1,Y1,Z1),X_slice,Y_slice,Z_slice);
colormap(jet);
shading interp; 
cb = colorbar;
view(3); 
axis equal; 
box on;
set(gca,'FontName','Times New Roman','FontSize',16);
set(cb,'FontName','Times New Roman','FontSize',16);
xlabel('X Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
ylabel('Y Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
zlabel('Z Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
title('Distribution of Fy','FontSize',20,'FontWeight','bold','FontName','Times New Roman');

% figure3：Fz
figure('Position',[400,50,900,700],'Color','w');
F_aqi = scatteredInterpolant(X,Y,Z,aqi_data,'linear','none');
slice(X1,Y1,Z1,F_aqi(X1,Y1,Z1),X_slice,Y_slice,Z_slice);
colormap(jet);
shading interp; 
cb = colorbar;
view(3); 
axis equal; 
box on;
set(gca,'FontName','Times New Roman','FontSize',16);
set(cb,'FontName','Times New Roman','FontSize',16);
xlabel('X Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
ylabel('Y Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
zlabel('Z Axis','FontSize',18,'FontWeight','bold','FontName','Times New Roman');
title('Distribution of Fz','FontSize',20,'FontWeight','bold','FontName','Times New Roman');