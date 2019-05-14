function [ n , tree ] = numberoftracesdaoct( auto,x0,l,r )
%EXCEEDING Computes the number of traces of AUTO with a given length l
%   auto.X      states
%   auto.lt     complete output
%   auto.l      output
%   auto.theta  conditional transition function
%   auto.Xf     final states
%   x0          initial state
%   l           trace length
%   r           #paths

node=x0;i=0;R = [1:1:r];tree(1).state=x0;tree(1).path=R;tree(1).l=auto(x0).l;
c=1;
while i<l;
    newnode=[];
    for j=1:length(node);
        tree(node(j)).theta = [];
        lxaj = length(auto(tree(node(j)).state).theta)/2;
        xnxaj = auto(tree(node(j)).state).theta(2:2:length(auto(tree(node(j)).state).theta));
        pnxaj = auto(tree(node(j)).state).theta(1:2:length(auto(tree(node(j)).state).theta)-1);
        vecaux = [];
        for p=1:lxaj
            indaux = find(xnxaj(p)==vecaux);
            if length(indaux) == 0
                indxnxaj = find(xnxaj(p)==xnxaj);
                vecaux = [vecaux xnxaj(p)];
                interset = intersect(tree(node(j)).path,pnxaj(indxnxaj));
                if length(interset)~=0
                    c=c+1;
                    tree(c).state=xnxaj(p);
                    tree(c).path = interset;
                    tree(c).l = auto(xnxaj(p)).l;
                    tree(node(j)).theta = [tree(node(j)).theta c];
                    newnode=[newnode c];
                end
            end
        end
    end   
    node = newnode;
    i=i+1;
end
n = length(newnode);
        
            
            
            




