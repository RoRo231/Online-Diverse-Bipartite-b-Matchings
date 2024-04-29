import operator
import os
"""
f=open("ml-1m/original_dataset/ratings.dat", "r")

num_reviews=dict()

for line in f:
  vals=line.split("::")
  if vals[0] not in num_reviews:
    num_reviews[vals[0]]=0
  num_reviews[vals[0]]+=1

sorted_x = sorted(num_reviews.items(), key=operator.itemgetter(1))

sampled_users=list()
cnt=0
for key, value in sorted_x:
  sampled_users.append(key)
  cnt+=1

  if cnt == 200:
    break

f.close()
"""
sampled_users = list()
path = "ml-1m/processed_dataset/predictions/"
for filename in os.listdir(path):
    if len(filename.split("_"))<3:
        continue
    sampled_users.append(filename.split("_")[2])

f=open("ml-1m/original_dataset/users.dat", "r")
full_users=dict()
for line in f:
  vals=line.split("::")
  #print(vals[0])
  full_users[vals[0]]=line

f=open("ml-1m/processed_dataset/reduced_users.dat", "w+")
g=open("ml-1m/processed_dataset/reduced_users_id.dat", "w+")
for s in sampled_users:
  f.write(full_users[str(s)])
  g.write(s + "\n")
