function [ auto ] = daoct2( P,k,r )
%DAOCT Function provides the identified DAOCT
%   P.path      paths p_i
%   P.pathlen   path lengths
%   k           free parameter
%   r           #paths

N=0;
auto(1).X = 1;
p1k = newpath(P.path(:,1:P.pathlen(1)),k);
auto(1).lt = p1k(:,1:k);
auto(1).l = p1k(:,k);
auto(1).theta = [];
for i=1:r
    pk = newpath(P.path(:,N+1:N+P.pathlen(i)),k);
    N = N + P.pathlen(i);
    for j=1:P.pathlen(i)-1
        current=0;next=0;
        for q=1:length(auto)
            if auto(q).lt==pk(:,(j-1)*k+1:j*k)
                current=q;
            end
            if auto(q).lt==pk(:,j*k+1:(j+1)*k)
                next=q;
            end
        end
        if next==0
            next = length(auto)+1;
            auto(next).X = next;
            auto(next).lt = pk(:,j*k+1:(j+1)*k);
            auto(next).l = pk(:,(j+1)*k);
        end
        vec1 = auto(current).theta(1:2:end-1);
        vec2 = auto(current).theta(2:2:end);
        ind1 = find(i==vec1);
        ind = find(next == vec2(ind1));
        if length(ind)==0
            auto(current).theta = [auto(current).theta i auto(next).X];
        end
        if j == P.pathlen(i)-1
            auto(next).Xf = 1;
        end
    end
end
