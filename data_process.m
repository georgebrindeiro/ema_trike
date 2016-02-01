clear
close all
angle = load('data_angle');
control = load('data_control');
left_leg = load('data_femoral');
right_leg = load('data_gastrocnemius');
speed = load('data_filteredAngSpeed');
time = load('data_time');
%clock = 1000/(length(time)/(time(end)-time(1)))
t = time-time(1);
t_diff = diff(t);
T = mean(t_diff)*1000
F = 1000/T
plot(t(2:end),t_diff.*1000)