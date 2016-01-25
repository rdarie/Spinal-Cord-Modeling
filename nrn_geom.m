function nrn_geom(spl, diam, n_nodes, points_per_node, inl,debugging)
%UNTITLED Summary of this function goes here
%s: points along the spline
%spl: the spline
%diam: diameter of the fiber
%n_nodes: number of nodes
%points_per_node

system_id;

fname = strcat(tempdata_address, 'Ia_geometry');
fid = fopen(fname,'w');

%spl = spl - repmat(spl(:,size(spl,2)),1,size(spl,2));

count = 1;
if debugging
    figure();
end
for a = 0:n_nodes-1
    fprintf(fid, 'Ia_node[%d] {\npt3dclear()\n',a);
    
    [x,y,z] = node_edges(spl,count,diam);
    for b = 1:2
        fprintf(fid, 'pt3dadd(%4.4f, %4.4f, %4.4f, %4.4f)\n'...
            ,x(b),y(b),z(b),diam);
        
        if debugging
            plot3(spl(1,count),spl(2,count),spl(3,count),'co')
            hold on
            plot3(spl(1,count+1),spl(2,count+1),spl(3,count+1),'yo')
            plot3(x(b),y(b),z(b),'mo')
        end
        
    end
    fprintf(fid, '}\n');
    
    fprintf(fid, 'Ia_paranode[%d] {\npt3dclear()\n',a);
    % draw node-paranode junction
    fprintf(fid, 'pt3dadd(%4.4f, %4.4f, %4.4f, %4.4f)\n'...
        ,x(2),y(2),z(2),diam);
    
    if debugging
        plot3(spl(1,count),spl(2,count),spl(3,count),'bo')
        plot3(spl(1,count+1),spl(2,count+1),spl(3,count+1),'go')
        plot3(x(2),y(2),z(2),'ro');
    end
    
    count = count+1;
    
    for b = 1:points_per_node-2
        [x,y,z] = paranode_edges(spl,count,diam,inl./points_per_node);
        fprintf(fid, 'pt3dadd(%4.4f, %4.4f, %4.4f, %4.4f)\n'...
            ,x(2),y(2),z(2),diam);
        
        if debugging
            plot3(spl(1,count),spl(2,count),spl(3,count),'bo')
            plot3(spl(1,count+1),spl(2,count+1),spl(3,count+1),'go')
            plot3(x(2),y(2),z(2),'ro')
        end
        
        count = count+1;
    end
    
    try
        [x,y,z] = node_edges(spl,count+1,diam);
        fprintf(fid, 'pt3dadd(%4.4f, %4.4f, %4.4f, %4.4f)\n'...
            ,x(1),y(1),z(1),diam);
        
        if debugging
            plot3(x(1),y(1),z(1),'ro');
        end
        
        count = count+1;
    catch
        [x,y,z] = paranode_edges(spl,count,diam,inl./points_per_node);
        fprintf(fid, 'pt3dadd(%4.4f, %4.4f, %4.4f, %4.4f)\n'...
            ,x(2),y(2),z(2),diam);
        
        if debugging
            plot3(x(2),y(2),z(2),'ro')
        end
    end
    fprintf(fid, '}\n');
end

fclose(fid);
close all;
end

