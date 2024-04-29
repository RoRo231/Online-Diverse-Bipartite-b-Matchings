import random
import sys
from numpy.random import choice

T=int(sys.argv[1])
runs=int(sys.argv[2])

f=open("ml-1m/processed_dataset/reduced_users.dat", "r")
g=open("ml-1m/processed_dataset/reduced_users_withArrivals.dat", "w+")

list_users=list()

arrivals=list()
_sum=0
for line in f:
  r=random.uniform(0, 1)
  r=1/float(T) #questionable practice
  arrivals.append(r)
  _sum+=r
f.close()

f=open("ml-1m/processed_dataset/reduced_users.dat", "r")
i=0
for line in f:
  vals=line.split("\n")[0]
  g.write(vals + "::" + str(arrivals[i]/float(_sum)) + "\n")
  arrivals[i]=arrivals[i]/float(_sum)
  list_users.append(vals.split("::")[0])
  i+=1
  
for _r in range(runs):
  f=open("ml-1m/processed_dataset/GraphStructure/Arrivals/" + str(_r), "w+")
  
  for t in range(T):
    _v=choice(list_users, 1, arrivals)
    f.write(str(_v[0]) + "\n")

