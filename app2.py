import streamlit as st
import pandas as pd
from recommender2 import recommend_movies2
from recommender import recommend_movies

# Load the movie data
movies = pd.read_csv("data.csv")

# Function to search for movies
def search_movie(search_term):
    search_term = search_term.lower()
    filtered_movies = movies[movies['title'].str.lower().str.contains(search_term)][:5].reset_index(drop=True)
    titles = filtered_movies['title'].tolist()
    overview = filtered_movies['overview'].tolist()
    return titles, overview

# Streamlit app layout
st.title("Movie Recommender")

# Search for movies
st.header("Search for a Movie")
search_term = st.text_input("Enter a movie title")

if search_term:
    titles, overviews = search_movie(search_term)
    if titles:
        st.subheader("Search Results")
        for i in range(len(titles)):
            st.write(f"**Title:** {titles[i]}")
            st.write(f"**Overview:** {overviews[i]}")
            st.write("---")
    else:
        st.write("No movies found.")

# Movie recommendation section
st.header("Get Movie Recommendations")
chosen_movies = st.text_input("Enter chosen movie titles (comma separated)")

if st.button("Recommend"):
    if chosen_movies:
        chosen_movies_list = [movie.strip() for movie in chosen_movies.split(',')]
        if len(chosen_movies_list) == 1:
            recommendations = recommend_movies(chosen_movies_list)
        else:
            recommendations = recommend_movies2(chosen_movies_list)
        
        if recommendations:
            st.subheader("Recommended Movies")
            for rec in recommendations:
                st.write(rec)
        else:
            st.write("No recommendations found.")
    else:
        st.write("Please enter at least one movie title.")
