function tree = excdaoct(tree,curnode,vecfault)

vecfault = [vecfault tree(curnode).l];
vecnext = tree(curnode).theta;
tree(curnode).vecfault = vecfault;

for i=1:length(vecnext)
    curnode = vecnext(i);
    tree = excdaoct(tree,curnode,vecfault);
end
vecfault = vecfault(:,1:size(vecfault,2)-1);
        