clear all;
k=1;
%set=[6:16 26:32];% 26:32];
set = [9:16 29:32];

Datafaultfree2;
tic
[auto,Pn,Xfl,r,vecnormal] = faultfreemodel( vecfaultfree,set,k );%k cannot be longer than the length of the smallest path, or Xfl will be wrong
toc
[ vecn,vecend ] = pathdisting2( Pn,r );



%Insert the file with the fault vector
%   datafault_act5stopb;
datafault_teste_myscene_intermittentfault_sensor_box;


%Exclude the neighbours vectors that are equal
vec4 = vecfault';
vec4n=vec4(1,:);

for i=1:size(vec4,1)-1
    dife = vec4(i,:)-vec4(i+1,:);
    if norm(dife)~=0
        vec4n=[vec4n;vec4(i+1,:)];
    end
end
vecfault=vec4n';

[ result,i,c,currentstate,laststate,vectheta,N ] = faultdetection3( auto,vecfault,r,vecn,vecend,Xfl )
%[ result,i,c] = faultdetectionNDAAO( auto,vecfault,r,vecn,vecend,Xfl )
