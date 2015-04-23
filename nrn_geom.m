function nrn_geom(spl, diam, n_nodes, points_per_node )
%UNTITLED Summary of this function goes here
%s: points along the spline
%spl: the spline
%diam: diameter of the fiber
%n_nodes: number of nodes
%points_per_node

os = ispc; 
%code for system agnosticism in opening directory
if os == 1
    tempdata_address = '.\tempdata\' ;
    nrniv_dir = 'C:\nrn73w64\bin64\nrniv.exe' ;
else 
    tempdata_address = 'tempdata/' ;
    %nrniv_dir = '/Applications/NEURON-7.3/nrn/x86_64/bin/nrniv';
    nrniv_dir = '/Applications/NEURON-7.3/nrngui';
end 

fname = strcat(tempdata_address, 'Ia_geometry');
fid = fopen(fname,'w');

count = 1;

for a = 0:n_nodes-1
        fprintf(fid, 'Ia_node[%d] {\npt3dclear()\n',a);

        fprintf(fid, 'pt3dadd(%4.4f, %4.4f, %4.4f, %4.4f)\n'...
            ,spl(1,count),spl(2,count),spl(3,count),diam);
        fprintf(fid, '}\n');
        count = count+1;
            fprintf(fid, 'Ia_paranode[%d] {\npt3dclear()\n',a);
    for b = 1:points_per_node-1
       fprintf(fid, 'pt3dadd(%4.4f, %4.4f, %4.4f, %4.4f)\n'...
           ,spl(1,count),spl(2,count),spl(3,count),diam);
      count = count+1;
    end
%     if a ~= n_nodes-2
%         fprintf(fid, 'pt3dadd(%4.4f, %4.4f, %4.4f, %4.4f)\n'...
%             ,(spl(1,a+1)+spl(1,a+2))./2,(spl(2,a+1)+spl(2,a+2))./2,...
%             (spl(3,a+1)+spl(3,a+2))./2,diam);
%     end
    fprintf(fid, '}\n');
end

fclose(fid);
close all;
end

