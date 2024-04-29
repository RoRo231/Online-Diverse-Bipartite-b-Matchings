ROOT="ml-1m/processed_dataset/"
f=open(ROOT + "GraphStructure/edges.dat", "r")

RHS_edges=dict()
LHS_edges=dict()
for line in f:
    vals=line.split("\n")[0].split(",")
    RHS_edges[vals[1]]=1
    LHS_edges[vals[2]]=1

f=open(ROOT + "subsampled_movies.dat", "r")
g=open(ROOT + "reduced_movies.dat", "w+")
for line in f:
  vals=line.split("::")

  if vals[0] in LHS_edges:
    g.write(line)
g.close()
