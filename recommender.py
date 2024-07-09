import pandas as pd
import numpy as np
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("data.csv")

# data cleaning
movies = movies.fillna('')
movies = movies.applymap(lambda x: x.lower() if isinstance(x, str) else x)
translator = str.maketrans('', '', string.punctuation)
movies['genres'] = movies['genres'].apply(lambda x: x.translate(translator))
movies['keywords'] = movies['keywords'].apply(lambda x: x.translate(translator))
movies['overview'] = movies['overview'].apply(lambda x: x.translate(translator))

movies.loc[:, 'combined_features'] = movies['genres'] + ' ' + movies['keywords'] + ' ' + movies['overview']
movies['combined_features']

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(2, 3))
tfidf_matrix = tfidf_vectorizer.fit_transform(movies['combined_features'])

# Calculate cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to recommend movies based on two input movies
def recommend_movies(movieslist, cosine_sim=cosine_sim, df=movies):

    indices = []
    # Find the indices of the input movies
    for movie in movieslist:
        idx = df[df['title'] == movie.lower()].index[0]
        indices.append(idx)
    
    sim_scores = list(enumerate(np.sum([cosine_sim[idx] for idx in indices], axis=0)))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    n = len(movieslist)
    sim_scores = sim_scores[n:n+10]
    
    movie_indices = [i[0] for i in sim_scores]
    
    return list(df['title'].iloc[movie_indices])
