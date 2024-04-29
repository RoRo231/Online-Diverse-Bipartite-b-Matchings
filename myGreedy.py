import sys
from statistics import median, mean
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from tabulate import tabulate

def allEdges():
    ROOT="ml-1m/processed_dataset/"


#reduced_movie format: movieid, name, genre,  
#edges format: counter,userid,movieid,prediction,genre
#construct edges using dict(), together with the neighbourhood of RHS = users and LHS = movies
    f_edges=open(ROOT + "GraphStructure/edges.dat", "r")

    edges=dict()
    neigh_RHS=dict()
    reverse_edge=dict()
    E=0

    for line in f_edges:
        vals=line.split("\n")[0].split(",")
        E+=1
    
        edges[vals[0]]=dict()
        edges[vals[0]]["RHS"]=vals[1] #users
        edges[vals[0]]["LHS"]=vals[2] #movieid
        edges[vals[0]]["prediction"]=float(vals[3])
        edges[vals[0]]["features"]=set()
    
        reverse_edge[vals[1] + "<>" + vals[2]]=vals[0]
        if vals[1] not in neigh_RHS:
            neigh_RHS[vals[1]]=set()


        neigh_RHS[vals[1]].add(vals[2])

        edges[vals[0]]["features"]=set(vals[4].split("|")) #multiple genres for a single movie

    f_edges.close()
    
    return edges, neigh_RHS, reverse_edge

def totalProportion(all_edges):
    total_proportion = dict()
    for edge in all_edges:
        for feature in all_edges[edge]["features"]:
            if feature not in total_proportion:
                total_proportion[feature] = 0
            total_proportion[feature]+= 1
    return total_proportion

def utilityGreedyAlgo():
    ROOT="ml-1m/processed_dataset/"
    edges, neigh_RHS, reverse_edge = allEdges()
    #Beginning of the actual algorithm
    t=0
    arr=dict()
    #need to change run
    for run in range(1):
        arrivals=dict()
        f_arr=open(ROOT + "GraphStructure/Arrivals/" + str(run), "r")

        f_LHS=open(ROOT + "subsampled_movies.dat", "r")

        av_LHS=dict()
        max_LHS = dict()
        temp_ctr = 0 #NEED TO CHANGE THIS
        for line in f_LHS:
            vals=line.split("\n")[0]
            movieID = vals.split("::")[0]
            av_LHS[movieID]=0
            if temp_ctr == 10:
                temp_ctr = 0
            temp_ctr+=1
            max_LHS[movieID] = 30
        f_LHS.close()  


    #take all users arrive at a specific run
        for line in f_arr:
            vals=line.split("\n")[0]
            arr[t]=vals
            t+=1
        f_arr.close()

    final_matching_feature = dict()
    final_matching = dict()
    for i in range(t):
        chosenEdges=dict()
        arr_v=arr[i]
        #print("UserID"+arr_v)
        if arr_v not in final_matching_feature:
            final_matching_feature[arr_v] = set()
            final_matching[arr_v] = []
        if arr_v == "-1":
            continue
        LHS_v=neigh_RHS[arr_v]  #movie recommendation candidates
        #print("movie candidates:")
        #print(LHS_v)
        #Making the Greedy choice

        objectiveVal = dict()
 
        for movieID in LHS_v:
            if av_LHS[movieID]>=max_LHS[movieID]: #CHANGE THIS
                continue
            edge = reverse_edge[arr_v + "<>" + movieID]
            objectiveVal[edge] = edges[edge]["prediction"]
        sortedMovie = {edge: rating for edge, rating in sorted(objectiveVal.items(), key = lambda item: item[1])}
        chosenEdges = {edge: edges[edge] for edge in list(sortedMovie)[-5:]}
        for edge in chosenEdges:
            final_matching_feature[arr_v] = final_matching_feature[arr_v].union(chosenEdges[edge]["features"])
            movieID = chosenEdges[edge]["LHS"]
            av_LHS[movieID]+=1
        final_matching[arr_v].append(chosenEdges)
        
        #print(final_matching[arr_v])
        #print(chosenEdges)
    #print(av_LHS)
    #print(max_LHS)        
    #print(final_matching)
    return final_matching, final_matching_feature


def computeF(S,edges):
    covered=set()
    for e in S:
        #e is edge ID
        #print(e)
        user = edges[e]["RHS"]
        #print(S)
        covered = covered.union(edges[e]["features"])
        #print(covered)
    total=0
    total_coverage = totalCoverage()
    for _cov in covered:
        total = total + total_coverage[user][_cov]
        #print(fWeights[_cov][user])
        
    #print(total)
    return total


def totalCoverage():
  ROOT="ml-1m/processed_dataset/"
  fWeights=dict()
  total_coverage = dict()
  f_fweights=open(ROOT + "GraphStructure/feature_weights.dat", "r")
  #feature, user, weight
  for line in f_fweights:
    vals=line.split("\n")[0].split(",")
    feature = vals[0]
    user = vals[1]
    weight = vals[2]
    if user not in total_coverage:
      total_coverage[user]=dict()
    if feature not in total_coverage[user]:
      total_coverage[user][feature]= 0
    total_coverage[user][feature] = total_coverage[user][feature]+float(weight)

  return total_coverage

def diversityGreedyAlgo():
    ROOT="ml-1m/processed_dataset/"
    edges, neigh_RHS, reverse_edge = allEdges()
    #Beginning of the actual algorithm
    t=0
    arr=dict()
  
    #need to change run
    for run in range(1):
        arrivals=dict()
        f_arr=open(ROOT + "GraphStructure/Arrivals/" + str(run), "r")

        f_LHS=open(ROOT + "subsampled_movies.dat", "r")

        av_LHS=dict()
        max_LHS = dict()
        temp_ctr = 0 #NEED TO CHANGE THIS
        for line in f_LHS:
            vals=line.split("\n")[0]
            movieID = vals.split("::")[0]
            av_LHS[movieID]=0
            if temp_ctr == 10:
                temp_ctr = 0
            temp_ctr+=1
            max_LHS[movieID] = 30
        f_LHS.close()  


  #take all users arrive at a specific run
        for line in f_arr:
            vals=line.split("\n")[0]
            arr[t]=vals
            t+=1
        f_arr.close()

    final_matching_feature = dict()
    final_matching = dict()
    for i in range(t):
        chosenEdges=dict()
        arr_v=arr[i]
        #print("UserID"+arr_v)
        if arr_v not in final_matching_feature:
            final_matching_feature[arr_v] = set()
            final_matching[arr_v] = []
        if arr_v == "-1":
            continue
        LHS_v=neigh_RHS[arr_v]  #movie recommendation candidates
        #print("movie candidates:")
        #print(LHS_v)
        #Making the Greedy choice

        counter = 0
        while counter != 5:
            maxEdge, av_LHS = findBestMovie(LHS_v, av_LHS, max_LHS, arr_v, chosenEdges)
            chosenEdges[maxEdge]=edges[maxEdge]
            counter += 1
        
        for edge in chosenEdges:
            final_matching_feature[arr_v] = final_matching_feature[arr_v].union(edges[edge]["features"])
        final_matching[arr_v].append({edge: edges[edge] for edge in chosenEdges})
    return final_matching, final_matching_feature

def findBestMovie(LHS_v, av_LHS, max_LHS, arr_v, chosenEdges):
    maximum = -1
    maxEdge = ""
    for movieID in LHS_v:
        if av_LHS[movieID]>=max_LHS[movieID]: #CHANGE THIS
            #print("here"+ movieID)
            #print(av_LHS[movieID])
            continue
        edge=reverse_edge[arr_v + "<>" + movieID]
        _chosenEdges=chosenEdges.copy()  #current set of matchings for arr_v (user)
        
        if edge in chosenEdges:
            continue
        
        _chosenEdges[edge]=edges[edge]
        _value=computeF(_chosenEdges, edges)-computeF(chosenEdges, edges)   #compute the submodular objective function

        if _value>maximum:
            maximum=_value
            maxEdge=edge
        
        if maximum == -1:
            continue
        if maxEdge not in edges:
            continue
    av_LHS[edges[maxEdge]["LHS"]]+=1
    return maxEdge, av_LHS

def compute_POD(diverse_matching, utility_matching, all_edges):
    sum_diversity = 0
    sum_utility = 0
    #print("Diversity predction")
    for user in diverse_matching:
        #print(user)
        for edges in diverse_matching[user]: 
            #print(diverse_matching[user])
            for edge in edges:
                sum_diversity += all_edges[edge]["prediction"]
                #print(all_edges[edge]["prediction"])        
    for user in utility_matching:
        for edges in utility_matching[user]: 
            for edge in edges:
                sum_utility += all_edges[edge]["prediction"]
                #print(all_edges[edge]["prediction"])
    return sum_diversity/sum_utility

def computeEntropy(matchings, all_edges):
    proportion = dict()
    entropy = dict()
    #print(matchings)
    for user in matchings:
        if user not in proportion:
            proportion[user] = dict()
        for edges in matchings[user]:
            for edge in edges:
                for feature in all_edges[edge]["features"]:
                    if feature not in proportion[user]:
                        proportion[user][feature] = 0
                    proportion[user][feature] += 1
    total_proportion = totalProportion(all_edges)
    entropy = dict()
    for user in matchings:
        entropy[user] = 0
        for feature in proportion[user]:
            p = proportion[user][feature]/total_proportion[feature]
            entropy[user] = entropy[user] - p*math.log(p)
        
            
    return entropy

edges, neigh_RHS, reverse_edge = allEdges()
diverse_final_matching, diverse_final_matching_feature = diversityGreedyAlgo()
utility_final_matching, utility_final_matching_feature = utilityGreedyAlgo()
print(diverse_final_matching_feature)
print(utility_final_matching_feature)
diversity_entropy = computeEntropy(diverse_final_matching,edges)
print(diversity_entropy)
utility_entropy = computeEntropy(utility_final_matching, edges)
print(utility_entropy)
print(compute_POD(diverse_final_matching,utility_final_matching, edges))



users = list(utility_entropy.keys())
utility_entropy = list(utility_entropy.values())
diversity_entropy = list(diversity_entropy.values())
plt.plot(users, utility_entropy, marker = 'o', color = "blue", label = "entropy for OUM")  # 'o' for circle markers
plt.plot(users, diversity_entropy, marker = 'o', color = "pink", label = "entropy for OBDBM")  # 'o' for circle markers
plt.legend(loc="upper left")
plt.xlabel('User ID')
plt.ylabel('Entropy')
plt.title('Line Chart for entropy vs user')
plt.grid(True)  # Show grid
plt.show()


headers_user_feature_data = ["User ID", "Matched Genres from OBDBM", "Matched Genres from OUM",]
user_feature_data = [list(diverse_final_matching_feature.keys()), list(diverse_final_matching_feature.values()), list(utility_final_matching_feature.values())]
user_feature_table = tabulate(user_feature_data, headers = headers_user_feature_data, tablefmt="grid")
print(user_feature_table)



   



   








