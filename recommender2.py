import pandas as pd
import numpy as np
import string
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack, csr_matrix, hstack
import joblib
from sklearn.preprocessing import MinMaxScaler

# Load data
movies = pd.read_csv("data.csv")

# Data cleaning and preprocessing
movies = movies.fillna('')
movies = movies.applymap(lambda x: x.lower() if isinstance(x, str) else x)
translator = str.maketrans('', '', string.punctuation)
movies['genres'] = movies['genres'].apply(lambda x: x.translate(translator))
movies['keywords'] = movies['keywords'].apply(lambda x: x.translate(translator))
movies['overview'] = movies['overview'].apply(lambda x: x.translate(translator))

# Lemmatization
lemmatizer = WordNetLemmatizer()
movies['genres'] = movies['genres'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))
movies['keywords'] = movies['keywords'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))
movies['overview'] = movies['overview'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))

# Define weights for different features
weights = {
    'genres': 0.4,
    'keywords': 0.4,
    'overview': 0.1,
    'popularity': 0.1 
}

# Create a single TfidfVectorizer instance with a shared vocabulary
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
all_text_features = movies['genres'] + movies['keywords'] + movies['overview']
tfidf_vectorizer.fit(all_text_features)

# Create TF-IDF vectors with feature weights for text features
tfidf_matrices = {}
for feature, weight in weights.items():
    if feature != 'popularity':
        tfidf_matrices[feature] = tfidf_vectorizer.transform(movies[feature]) * weight

# Scale popularity to a range comparable to TF-IDF values
scaler = MinMaxScaler()
popularity_scaled = scaler.fit_transform(movies[['popularity']]).flatten() # Flatten the array

# Create a sparse matrix for popularity with the same number of columns as TF-IDF matrices
num_cols = tfidf_matrices['genres'].shape[1]
popularity_matrix = csr_matrix((popularity_scaled * weights['popularity'],
                                ([i for i in range(len(movies))], [0] * len(movies))),
                                shape=(len(movies), num_cols))

# Combine weighted TF-IDF matrices and popularity matrix vertically
combined_matrix = vstack(list(tfidf_matrices.values()) + [popularity_matrix])

# Calculate cosine similarity matrix (and cache it)
try:
    cosine_sim = joblib.load('cosine_sim.pkl')
except FileNotFoundError:
    cosine_sim = cosine_similarity(combined_matrix, combined_matrix)
    # joblib.dump(cosine_sim, 'cosine_sim.pkl')

# Function to recommend movies based on two input movies
def recommend_movies2(movieslist, cosine_sim=cosine_sim, df=movies):
    indices = []
    # Find the indices of the input movies
    for movie in movieslist:
        idx = df[df['title'] == movie.lower()].index[0]
        indices.append(idx)

    sim_scores = list(enumerate(np.sum([cosine_sim[idx] for idx in indices], axis=0)))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    n = len(movieslist)
    sim_scores = sim_scores[n:n + 10]

    movie_indices = [i[0] for i in sim_scores]

    return list(df['title'].iloc[movie_indices])
