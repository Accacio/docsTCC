function [ result,i,c,curstate,laststate,vectheta,N ] = faultdetection3( auto,vecf,r,vecn,vecend,Xfl )
%FAULTDETECTION3 Fault detection algorithm using the identified DAOCT 
%   auto        Identified model
%   vecf        Fault path of binary signals, where each column vector is
%               a set of binary signals. The first vector of vecf must be 
%               equal to the output label of the first state of auto
%   vecn        Number of observations for the distinguishability of each
%               path
%   vecend      Provides the number of vertices to reach the final state of
%               each path
%   Xfl         Provides the final state label of each path
%   result      Yes=1 or No=0
%   i           The number of the vector for which the fault is identified
%   c           Provides the condition that has been violated for the 
%               identification of the fault
vecn = vecn(2:2:end);
N=0;
curstate = 1;
laststate=1;
thetas = [1:1:r];
thetasant = thetas;
c=1;
vectheta(1).theta=thetas;
for i=2:size(vecf,2)
   result = 1;
   N=N+1;
   vecstate = auto(curstate).theta(2:2:end);
   vecpath = auto(curstate).theta(1:2:end-1);
   indj=[];
   
   for j=1:length(vecstate) %Verify if a possible state is reached
       if norm(auto(vecstate(j)).l-vecf(:,i))==0
           if length(indj) == 0
               laststate = curstate;
           end
           curstate = vecstate(j);
           indj = [indj j];
           result = 0;
       end
   end
   if result==1
       laststate = curstate;
       display('Fault detected');
       display('Reason: State not possible according to the identified model');
   end
   if result==0 %Unfeasible path
       thetasant = thetas;
       thetas = intersect(thetasant,vecpath(indj));
       if length(thetas)==0
           result = 1;
           c=2;
           display('Fault detected');
           display('Reason: The path is unfeasible');
       end
   end
   if result==0 %The path is identified before the correct number of
                %event occurrences
       if (length(thetasant)>1 && length(thetas)==1)
           if vecn(thetas)>N
               result = 1;
               c=3;
               display('Fault detected');
               display('Reason: The path has been identified before the correct number of event occurrences');
           end
       end
   end
   if result==0 %Verify if the observed vector is equal to the final state  
                %of the identified path 
       athetas = thetas;
       for y=1:length(athetas) %Reinitialization
           if (vecend(athetas(y))==N+1 && max(svd(auto(curstate).lt-Xfl(athetas(y)).value))==0)
               thetas=[1:1:r];
               N=0;
               curstate = 1;
           end
       end
       if N~=0
           maior = max(vecend(thetas));
           if maior == N+1
               result = 1;
               c = 4;
               display('Fault detected');
               display('Reason: Maximum number of events reached without reaching a final state');
           end
           athetas = thetas;%Eliminate the path from theta_s if the number 
                            %of events to reach the final state of the path 
                            %has occurred, and the final state has not been 
                            %reached
           for y=1:length(athetas)
               if vecend(athetas(y))==N+1
                   thetas = setdiff(thetas,athetas(y));
               end
           end
       end
   end    
   vectheta(i).theta=thetas;    
   if result==1
       break
   end
end
if result==0
    c=0;
    display('Fault not detected');
end
end
    
    


