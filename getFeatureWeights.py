import numpy as np

ROOT="ml-1m/processed_dataset/GraphStructure/"

features=dict()
f=open(ROOT+"edges.dat", "r")

for line in f:
  vals=line.split("\n")[0].split(",")

  _feat=vals[4]
  _feat_vals=_feat.split("|")

  for _fe_va in _feat_vals:
    if _fe_va not in features:
      features[_fe_va]=np.random.uniform(0, 1)

f=open(ROOT + "../reduced_users_withArrivals.dat", "r")

RHS_list=list() #users
for line in f:
  vals=line.split("\n")[0].split("::")
  RHS_list.append(vals[0])

feature_avg=dict()
feature_cnt=dict()
for _rhs in RHS_list:
  #complete_ratings format counter;movieid;prediction;title;genre
  f=open(ROOT + "../predictions/complete_ratings_" + _rhs, "r")
  feature_avg[_rhs]=dict()
  feature_cnt[_rhs]=dict()
  first=True

  for line in f:
    if first:
      first=False
      continue
    vals=line.split("\n")[0].split(";")
    pred=float(vals[2])
    genres=vals[4].split("|")

    for _feat in genres:
      if _feat not in feature_avg[_rhs]:
        feature_avg[_rhs][_feat]=0
        feature_cnt[_rhs][_feat]=0
      feature_avg[_rhs][_feat] = (feature_avg[_rhs][_feat]*feature_cnt[_rhs][_feat] + pred)/(feature_cnt[_rhs][_feat]+1)
      feature_cnt[_rhs][_feat]+=1

g=open(ROOT + "feature_weights.dat", "w+")
for _feat in features:
  for _RHS in RHS_list:
    r=0
    if _RHS in feature_avg and _feat in feature_avg[_RHS]:
      r=feature_avg[_RHS][_feat]
    #r=np.random.uniform(0, 1)
    g.write(_feat + "," + _RHS + "," + str(r) + "\n")


    

