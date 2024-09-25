# MovieMingle
 
This is a simple movie recommender system built using Flask, Python, and content-based recommendation engine. It allows users to select movies they like and get recommendations for similar movies based on genre, keywords, overview, and popularity.

## Features

- **Search:** Users can search for movies by title.
- **Selection:** Users can select up to 5 movies they like.
- **Recommendation:** Based on the selected movies, the system recommends 10 similar movies using a content-based filtering approach.

## Technologies Used

- **Backend:** Python with Flask
- **Frontend:** HTML, CSS, JavaScript, jQuery
- **Machine Learning:** Scikit-learn (TfidfVectorizer, cosine similarity)
- **Data Processing:** Pandas, NumPy
- **Natural Language Processing:** NLTK (for lemmatization)

## How it Works

1. **Data Preprocessing:** The movie dataset ("data.csv") is cleaned and preprocessed, including:
   - Handling missing values
   - Lowercasing text
   - Removing punctuation
   - Variables lemmatization
2. **Feature Engineering:**
   - TF-IDF vectors are created for genres, keywords, and overviews to represent the textual content of movies.
   - Feature weights are applied to give different importance to each feature.
3. **Similarity Calculation:**
   - Cosine similarity is calculated between all movies based on their combined feature vectors (TF-IDF and popularity).
4. **Recommendation Generation:**
   - When a user selects movies, the system finds the indices of these movies in the dataset.
   - It calculates the sum of cosine similarities between the selected movies and all other movies.
   - The top 10 movies with the highest similarity scores are recommended.

## Installation and Setup

1. **Clone the repository:**
```bash
   git clone https://github.com/FadyJohn10/MovieMingle.git
   
  ```
2. **Install dependencies:**
```bash
   pip install -r requirements.txt
   
  ```
3. **Run the Flask app:**
```bash
   python app.py
   
  ```
