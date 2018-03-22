import pandas as pd
import numpy as np
from scipy import sparse as sps

from Base.Cython.cosine_similarity import Cosine_Similarity
from elastic_net_cython import Elastic_Net


movies = [i.strip().split("::") for i in open('/home/luca/Scaricati/ml-10M100K/movies.dat', 'r').readlines()]

movies_df = pd.DataFrame(movies, columns = ['MovieID', 'Title', 'Kind'], dtype = int)

tempKind, tempID = [], []

for i in range(len(movies_df.MovieID)):
    temp = movies_df.Kind[i].split("|")
    tempKind.extend(temp)
    tempID.extend([movies_df.MovieID[i] for y in range(len(temp))])

movies_df = pd.DataFrame({"MovieID": tempID, "Kind": tempKind})

print('Starting create unique list')
movie_list = list(movies_df.MovieID.unique())
kind_list = list(movies_df.Kind.unique())
print(len(movie_list))
print(kind_list)

'''
print('Starting create rows and cols')
rows = list()
cols = list()

cols = movies_df.MovieID.astype('category', categories=movie_list).cat.codes
rows = movies_df.Kind.astype('category', categories=kind_list).cat.codes
data = np.ones(len(rows)).squeeze()
icm = sps.csc_matrix((data, (rows, cols)), shape=(len(kind_list),len(movie_list)))

ratings = [i.strip().split("::") for i in open('/home/luca/Scaricati/ml-10M100K/ratings.dat', 'r').readlines()]

ratings_df = pd.DataFrame(ratings, columns = ['UserID', 'MovieID', 'Ratings', 'Timestamp'], dtype = int)

print('Starting create unique list for urm')
user_list = list(ratings_df.UserID.unique())
print(len(user_list))


cols = list()
rows = list()

cols = ratings_df.MovieID.astype('category', categories=movie_list).cat.codes
rows = ratings_df.UserID.astype('category', categories=user_list).cat.codes
data = ratings_df.Ratings.astype(float)

urm = sps.csc_matrix((data, (rows, cols)), shape=(len(user_list),len(movie_list)), dtype=np.float32)
sps.save_npz("files/urm.npz", urm)
'''

movie_list = np.load('files/movies_list.npy')
user_list = np.load('files/user_list.npy')
kind_list = np.load('files/kind_list.npy')

urm = sps.load_npz("files/urm.npz")
icm = sps.load_npz("files/icm.npz")

el = Elastic_Net(icm, urm)
el.fit()

