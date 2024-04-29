f=open("ml-1m/processed_dataset/reduced_users.dat", "r")
users=dict()
for line in f:
  #vals=line.split("\n")[0]
  vals=line.split("::")[0]
  users[vals]=1
f.close()


f=open("ml-1m/original_dataset/ratings.dat", "r")
g=open("ml-1m/processed_dataset/reduced_ratings.dat", "w+")
for line in f:
  vals=line.split("::")
  _user=vals[0]

  if vals[0] in users:
    g.write(line)
f.close()
g.close()
