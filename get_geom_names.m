cutaway_index = 6;

tissue_info = mphgetselection(fem.selection('sel5'));
tissue_dom = tissue_info.entities;
tissue_bnd = mphgetadj(fem,geom,'boundary','domain',tissue_dom);
tissue_edge = mphgetadj(fem,geom,'edge','domain',tissue_dom);

el_info = mphgetselection(fem.selection('sel6'));
el_dom = el_info.entities;
el_bnd = mphgetadj(fem,geom,'boundary','domain',el_dom);
el_edge = mphgetadj(fem,geom,'edge','domain',el_dom);

gm_info = mphgetselection(fem.selection('sel9'));
gm_dom = gm_info.entities;
gm_bnd = cell(1,2);
gm_bnd{1} = mphgetadj(fem,geom,'boundary','domain',gm_dom(1:cutaway_index));
gm_bnd{2} = mphgetadj(fem,geom,'boundary','domain',gm_dom(cutaway_index+1:end));
gm_edge = mphgetadj(fem,geom,'edge','domain',gm_dom);

wm_info = mphgetselection(fem.selection('sel8'));
wm_dom = wm_info.entities;
wm_bnd = cell(1,2);
wm_bnd{1} = mphgetadj(fem,geom,'boundary','domain',wm_dom(1:cutaway_index));
wm_bnd{2} = mphgetadj(fem,geom,'boundary','domain',wm_dom(cutaway_index+1:end));
wm_edge = mphgetadj(fem,geom,'edge','domain',wm_dom);

csf_info = mphgetselection(fem.selection('sel7'));
csf_dom = csf_info.entities;
csf_bnd = cell(1,2);
csf_bnd{1} = mphgetadj(fem,geom,'boundary','domain',csf_dom(1:cutaway_index));
csf_bnd{2} = mphgetadj(fem,geom,'boundary','domain',csf_dom(cutaway_index+1:end));
csf_edge = mphgetadj(fem,geom,'edge','domain',csf_dom);