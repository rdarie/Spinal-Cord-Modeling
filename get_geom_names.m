

tissue_info = mphgetselection(fem.selection('sel2'));
tissue_dom = tissue_info.entities;
tissue_bnd = mphgetadj(fem,geom,'boundary','domain',tissue_dom);
tissue_edge = mphgetadj(fem,geom,'edge','domain',tissue_dom);

el_info = mphgetselection(fem.selection('sel6'));
el_dom = el_info.entities;
el_bnd = mphgetadj(fem,geom,'boundary','domain',el_dom);
el_edge = mphgetadj(fem,geom,'edge','domain',el_dom);

gm_info = mphgetselection(fem.selection('sel5'));
gm_dom = gm_info.entities;
gm_bnd = cell(1,2);
gm_bnd{1} = mphgetadj(fem,geom,'boundary','domain',gm_dom(1:6));
gm_bnd{2} = mphgetadj(fem,geom,'boundary','domain',gm_dom(7:end));
gm_edge = mphgetadj(fem,geom,'edge','domain',gm_dom);

wm_info = mphgetselection(fem.selection('sel4'));
wm_dom = wm_info.entities;
wm_bnd = cell(1,2);
wm_bnd{1} = mphgetadj(fem,geom,'boundary','domain',wm_dom(1:6));
wm_bnd{2} = mphgetadj(fem,geom,'boundary','domain',wm_dom(7:end));
wm_edge = mphgetadj(fem,geom,'edge','domain',wm_dom);

csf_info = mphgetselection(fem.selection('sel3'));
csf_dom = csf_info.entities;
csf_bnd = cell(1,2);
csf_bnd{1} = mphgetadj(fem,geom,'boundary','domain',csf_dom(1:6));
csf_bnd{2} = mphgetadj(fem,geom,'boundary','domain',csf_dom(7:end));
csf_edge = mphgetadj(fem,geom,'edge','domain',csf_dom);