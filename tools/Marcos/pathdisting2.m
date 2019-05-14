function [ vecn,vecend ] = pathdisting2( P,r )
%PATHDISTING2    provides the number of events that must be observed
%                to distinguish each path
%
%               
N=0;
vecn=[];
%Xfl=[];
vecend = P.pathlen;
for i=1:r
    p = P.path(:,N+1:N+P.pathlen(i));
    N = N + P.pathlen(i);
    Pn(i).path = p;
   % Xfl=[Xfl Pn(i).path(:,end)];
end
if r>1
    for i=1:r
        difind=[];
        for j=1:r
            if i~=j
                if size(Pn(i).path,2)>=size(Pn(j).path,2)
                    diffe = Pn(i).path(:,1:size(Pn(j).path,2))-Pn(j).path;
                else
                    diffe = Pn(i).path-Pn(j).path(:,1:size(Pn(i).path,2));
                end
                difindex = [];
                for l=1:size(diffe,2)
                    if norm(diffe(:,l))~=0
                        difindex = [difindex l];
                    end
                end
                difind = [difind difindex(1)];
            end
        end
        vecn = [vecn i max(difind)-1];
    end
else
    vecn=[1 1];
end

end
   