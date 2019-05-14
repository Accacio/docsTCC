%clear all;
%k=1;
%set = [9:16 29:32];
x0=1;
%l=7;

%Datafaultfree2;

%[auto,Pn,Xfl,r,vecnormal] = faultfreemodel( vecfaultfree,set,k );%k cannot be longer than the length of the smallest path, or Xfl will be wrong
[ vecn,vecend ] = pathdisting2( Pn,r );
[ ntracesauto , tree ] = numberoftraces2( auto,x0,l,r );

%vecfault = tree(1).l;
vecfault = [];
curnode = 1;
tree(1).vecfault = [];
tree = excdaoct(tree,curnode,vecfault);

nred=0;
for i=1:length(tree)    
    if size(tree(i).vecfault,2)==l+1
        vecf = tree(i).vecfault;
        [ result,i,c,currentstate,laststate,thetasant,N ] = faultdetection3( auto,vecf,r,vecn,vecend,Xfl );
        if result==1
            nred = nred+1;
        end
    end
end

[ ntraces ] = numberofobstraces( Pn,r,l );
nexc = ntracesauto-nred-ntraces;


