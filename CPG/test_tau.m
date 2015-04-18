clear; clc; close all;

v = linspace(-80, 50, 100);

paper_typo = 7 ./ (exp((v+40)./40) + exp(-(-v+40)./50));
paper = 7 ./ (exp((v+40)./40) + exp(-(v+40)./50));
booth = 4 ./ cosh((v+44.5)./10);

rfig();
plot(v,paper_typo);
hold on;
plot(v,paper);
plot(v,booth);

legend('typo', 'paper', 'booth');

new_cosh = 1200./ cosh(( v + 59 ) ./ 26);
old_cosh = 1200./ cosh(( v + 59 ) ./ 16);


rfig();
plot(v,new_cosh);
hold on;
plot(v,old_cosh);

legend(',new cosh', ',old cosh');

new_h = 1 ./ ( 1 + exp( ( v + 59 ) ./ 3 ) );
old_h = 1 ./ ( 1 + exp( ( v + 59 ) ./ 8 ) );


rfig();
plot(v,new_h);
hold on;
plot(v,old_h);

legend(',new h', ',old h');