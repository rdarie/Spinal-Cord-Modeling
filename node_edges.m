function [x,y,z] = node_edges(spl,count,diam)

this_point = spl(:,count);
next_point = spl(:,count+1);

dir = (next_point-this_point)./norm(next_point-this_point);

postpoint = this_point + diam*dir;

if count == 1
    prepoint = this_point - diam*dir;
else
    prev_point = spl(:,count-1);
    
    dir = (prev_point-this_point)./norm(prev_point-this_point);
    prepoint = this_point + diam*dir;
end

x = [prepoint(1) postpoint(1)];
y = [prepoint(2) postpoint(2)];
z = [prepoint(3) postpoint(3)];

end