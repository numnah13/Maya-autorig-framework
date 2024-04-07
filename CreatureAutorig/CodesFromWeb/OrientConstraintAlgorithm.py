'''
Created on 24. 1. 2024

https://discourse.techart.online/t/maya-orientconstraint-algorithm/1359/5
'''


#I’ve tried reproducing Maya’s result in various ways, but for example these forms are incorrect:
Quaternion q= Quaternion.identity;
for (int i=0; i<targets.length; i++)
    q *= Quaternion.Slerp(Quaternion.identity, targets[i].q, targets[i].w
Quaternion q= Quaternion.identity;
for (int i=0; i<targets.length; i++)
    q *= Quaternion.Slerp(q, targets[i].q, targets[i].w
                          
# I forgot that maya also has weights for the constraints that you can manipulate                          
                          
rq = slerp (slerp (t0, t1), t2)
#The weight values are remapped into a range of 0 to 1.