import numpy as np

ROOT="ml-1m/processed_dataset/"

f=open(ROOT + "reduced_users_withArrivals.dat", "r")
g=open(ROOT + "GraphStructure/edges.dat", "w+")


f_movies=open(ROOT + "subsampled_movies.dat", "r" )
movies=dict()

for line in f_movies:
  vals=line.split("::")
  movies[vals[0]]=1

E=0
for line in f:
  user_id=int(line.split("::")[0])

  h=open(ROOT + "predictions/complete_ratings_" + str(user_id), "r")
  first=True
  for line in h:
    if first:
      first=False
      continue
    vals=line.split(";") #ctr;movieid;prediction;title;genre
    movieid = vals[1]
    prediction = vals[2]
    genre = vals[4]
    if vals[1] in movies:
      #continue
      g.write(str(E) + ","  + str(user_id) + "," + str(movieid) + "," + str(prediction) + ","+ genre)
    E+=1
h.close()
    
