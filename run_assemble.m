clear;clc;close all;

ppn = 10+1;
inl = 100;% how many times longer is a paranode than a node?
%diam = log(random('logn', 9, 0.2, 10, 1));
diam = [9,5];
%start_offset = 0:5:100;
start_offset = 0;
file_list = {'\move_root_um',...
};
tag_list = {'moved, root there',...
};
points_list = {'move_root_points.csv',...
};
for a = 1:length(file_list)
    assemble_voltages(file_list{a},tag_list{a},...
        points_list{a},diam,start_offset, inl, ppn,0);
end