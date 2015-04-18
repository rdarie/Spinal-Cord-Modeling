RG_E_v = textread('RG_E_v.txt','%f');
    RG_F_v = textread('RG_F_v.txt','%f');
    Inrg_E_v = textread('Inrg_E_v.txt','%f');
    Inrg_F_v = textread('Inrg_F_v.txt','%f');
    
    rfig();
    subplot(4,1,1);
    plot(RG_E_v);
    title('RG_E');
    subplot(4,1,3);
    plot(RG_F_v);
    title('RG_F');
    subplot(4,1,2);
    plot(Inrg_E_v);
    title('INRG_E');
    subplot(4,1,4);
    plot(Inrg_F_v);
    title('INRG_F');
    
    rfig();
    plot(RG_E_v);
    hold on;
    
    plot(RG_F_v);
    
    