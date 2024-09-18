from flask import Flask, render_template, request, jsonify
import pandas as pd
from recommender2 import recommend_movies2
from recommender import recommend_movies

app = Flask(__name__)
movies = pd.read_csv("data.csv")

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to return JSON response for movie search results
@app.route('/search_movie', methods = ['POST'])
def search_movie():
    search_term = request.json['search_term'].lower()
    filtered_movies = movies[movies['title'].str.lower().str.contains(search_term)][:5].reset_index(drop=True)
    titles = filtered_movies['title'].tolist()
    overview = filtered_movies['overview'].tolist()
    return jsonify({'suggestions': titles, 'overviews': overview})

# Endpoint to get the movies used for AI recommendation
@app.route('/recommend', methods = ['POST'])
def getInputs():
    try:
        data = request.get_json()
        chosen_movies = data.get('chosen_movies')
        if chosen_movies:
            if len(chosen_movies) == 1:
                recommendations = recommend_movies(chosen_movies)
            else:
                recommendations = recommend_movies2(chosen_movies)
            app.logger.debug('Recommendations: %s', recommendations)
            return jsonify({'recommendations': recommendations})
        else:
            return jsonify({'error': 'No chosen movies selected'}), 400
    except Exception as e:
        app.logger.error('Error processing request: %s', e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
