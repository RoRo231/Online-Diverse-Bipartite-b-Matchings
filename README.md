
# Online Diverse Bipartite $b$-Matchings

Our code is based on https://bitbucket.org/karthikabinav/onlinesubmodularbipartitematching/src/master/, the repo of the paper Balancing Relevance and Diversity in Online Bipartite Matching via Submodularity by John P. Dickerson, Karthik Abinav Sankararaman, Aravind Srinivasan, Pan Xu

Their training of the ML model on predicting ratings are missing. But the resulting dataset is available. We still keep the command here. 

## Preprocessing

Subsample 100 movies
```
!python getSubSampledMovies.py
```

Choose top 200 users who has rated the most number of movies
```
!python getReducedUsers.py
```

Use the collaborative filtering algorithm to complete ratings for all the 100 movies that were sub-sampled. The predicted ratings for each user is put in a separate folder. The folder m1-1m/processed_dataset/predictions/complete_ratings_X contains the predictions for each of the unseen movies for user X.
```
!python ml-1m/keras-movielens-cf/MovieLens/1M/Recommendations.py
```

Filter the predicted ratings for the (user, movie) pair which are present in the smaller sub-sampled dataset. 
```
!python getReducedRatings.py
```

Obtain the arrival rates for the users. For each user, we first choose a random number between 0 and 1. Let total be the sum of the random numbers generated for each user. At each time-step, a user is sampled with probability (random number)/total. There are two arguments for this command: arg1 = number of users per round, arg2 = number of rounds.
```
!python getArrivals.py 10 1
```

The movies form the LHS of the graph, the users form the RHS of the graph. We add an edge between every user and a movie if and only if the user hasn't seen this movie. The following command gives the edges.
```
!python getEdges.py
```

Remove movies with no edges
```
!python remove_unused_LHS_RHS.py
```

Finally, compute the weights for every (user, feature) pair.
```
!python getFeatureWeights.py
```

## Experiments


```
!python myGreedy.py
```



