function [ cont ] = numberofobstraces( P,r,l )
%NUMBEROFOBSTRACES Computes the number of observed traces of P of length l
%   P           path structure
%   l           trace length
%   r           #paths

N=0;
l = l+1;
for i=1:r
    p = P.path(:,N+1:N+P.pathlen(i));
    N = N + P.pathlen(i);
    Pn(i).path = p;
end
c=1;
Q = [];
for i=1:r
    if size(Pn(i).path,2)>=l
        Q(1).path = Pn(i).path(:,1:l);
        break
    end
end
for i=1:r
    if size(Pn(i).path,2)>=l
        aux = 0;
        for j=1:length(Q)
            if Q(j).path == Pn(i).path(:,1:l)
                aux=1;
            end
        end
        if aux == 0
            c = c+1;
            Q(c).path = Pn(i).path(:,1:l);
        end
    end
end
cont = length(Q);

