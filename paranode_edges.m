function [x,y,z] = paranode_edges(spl,count,diam,pn_size)

this_point = spl(:,count);
prev_point = spl(:,count-1);


dir = (prev_point-this_point)./norm(prev_point-this_point);
prepoint = this_point + pn_size*diam*dir/2;

if count == size(spl,2)
    postpoint = this_point - pn_size*diam*dir/2;
else
    next_point = spl(:,count+1);
    
    dir = (next_point-this_point)./norm(next_point-this_point);
    postpoint = this_point + pn_size*diam*dir/2;
    
end

x = [prepoint(1) postpoint(1)];
y = [prepoint(2) postpoint(2)];
z = [prepoint(3) postpoint(3)];

end