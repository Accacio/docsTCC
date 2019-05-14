basicscript;%gerar AUTO de acordo com k
vecnexc=[];
vecntraces=[];
vecntracesauto=[];
nexca=0;
nautoa=0;
for l=1:12
    exceed_daoct;
    vecntraces=[vecntraces ntraces];
    nautoa=nautoa+ntracesauto-ntraces;
    nexca=nexca+nexc;
    vecnexc=[vecnexc nexca];
    vecntracesauto=[vecntracesauto nautoa];
end
figure(1)
hold off;plot(1:l,vecnexc,'k-d');hold on;plot(1:l,vecntracesauto,'k-*');