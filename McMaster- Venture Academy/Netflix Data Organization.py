# Venture Academy Fall 2021 Clubs
# AI Coding 9-12
# Python Recommender System Project

# Import required libraries
import pandas as pd
from math import pow, sqrt

# Data Organization and Preprocessing
# Read ratings & movies datasets into pandas dataframe objects
ratings = pd.read_csv('ratings.csv', engine='python')
print(ratings.head())

movies = pd.read_csv( 'movies.csv', engine= 'python')
movies.genres = movies.genres.str.split('|')
print(movies.head())

# Functions Defitions - 'getters'
def getRating(user,movieid):
  # Get rating a user gave a movie
  return (ratings.loc[(ratings.userId==user) & (ratings.movieId == movieid),'rating'].iloc[0])

def getMovieids(user):
  # Get list of all movieIds that a user has rated
  return (ratings.loc[(ratings.userId==user),'movieId'].tolist())

def getMovieTitle(movieid):
  # Get movie title from given movieId
  return (movies.loc[(movies.movieId == movieid),'title'].iloc[0])

def moviesWatched(user):
  # Return list of all movie titles a user has rated
  movieList = {}
  index = 0
  for i in getMovieids(user):
    movieList[index] = getMovieTitle(i)
    index += 1
  return (movieList)

# Test getter functions
userA = 52
movieA = 193
print('\nMovies watched by user', userA, ':\n', getMovieids(userA))
print('\nTitle of movie', movieA, ':', getMovieTitle(movieA))
print('\nTitles of movies watched by user', userA, ':\n', moviesWatched(userA))

def pearsonCorrelation(user1, user2):
  # Calculates similarity scores between 2 users between -1 and 1

  bothWatch = []
  list1 = ratings.loc[ratings.userId==user1, 'movieId'].tolist()
  list2 = ratings.loc[ratings.userId==user2, 'movieId'].tolist()  
  for i in list1:
    if i in list2: 
      bothWatch.append(i)

  if len(bothWatch) == 0:
    return 0 

  # Calculations
  ratingSum_1 = sum([getRating(user1, i) for i in bothWatch])
  ratingSum_2 = sum([getRating(user2, i) for i in bothWatch])
  ratingSquaredSum_1 = sum([pow(getRating(user1, i),2) for i in bothWatch])
  ratingSquaredSum_2 = sum([pow(getRating(user2, i),2) for i in bothWatch])
  productSumRating = sum([getRating(user1, i) * getRating(user2, i) for i in bothWatch])
  
  numerator = productSumRating - ((ratingSum_1 * ratingSum_2) / len(bothWatch))
  denominator = sqrt((ratingSquaredSum_1 - pow(ratingSum_1,2) / len(bothWatch)) * (ratingSquaredSum_2 - pow(ratingSum_2,2) / len(bothWatch)))
  
  #Catch potential math error!
  if denominator == 0:
   return 0
   
  return numerator/denominator

# Test finding Pearson Score for 2 users
userx = 88
usery = 69
print( 'Pearson Correlations Score for users' , userx, 'and', usery)
print(pearsonCorrelation(userx, usery))

def getRecs(user):
  # Get movie recommendations for user, based on correlation scores with other users and their ratings
  # and their ratings 

  user_ids = ratings.userId.unique().tolist()
  total = {}
  similaritySum = {}

  #Iterate over other users ids 
  for i in user_ids: 
    #Calculate similarity score
    score = pearsonCorrelation(user, i)

    #Skip if users have a 0 or negative score because they aren't a good match 
    if score <= 0: 
      continue 

    #Get weighted similarity scores 
    for movieid in getMovieids(i):
      if movieid not in getMovieids(user) or getRating(user, movieid) == 0:
        total[movieid] = getRating(i, movieid) * score
        similaritySum[movieid] = score 

    #Normalize ratings 
    ranking = [(tot/similaritySum[movieid], movieid) for movieid, tot in total.items()]
    ranking.sort()
    ranking.reverse()

    #Get movie titles instead of numbers and return the top 10 matches 
    rec = [getMovieTitle(movieid) for score, movieid in ranking]
    return rec[:10] 

# Test finding movie recommendations for a user
userx = 30


print('\nRecommended movies for user', userx, ':')
print(getRecs(userx))












