# app.py
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Dummy user data for login
users = {
    'user': 'user',
    'admin': 'admin'
}

authenticated = False

# Load data from Excel file into a pandas DataFrame
movies_df = pd.read_excel('static/movies_data.xlsx')

# Define a function to fetch movie details by movieId
def get_movie_details(movie_id):
    movie_details = movies_df[movies_df['movieId'] == movie_id].iloc[0]

    # Extract genres names
    genres = eval(movie_details['genres'])
    genre_names = [genre['name'] for genre in genres]
    genres_str = ', '.join(genre_names)

    # Extract cast names and image links
    cast_info = eval(movie_details['cast'])
    cast_names = [actor['name'] for actor in cast_info]
    top_5_cast = cast_names[:5]
    cast_str = ', '.join(top_5_cast)


    # Format release date
    rel_date = movie_details['release_date']
    release_date = rel_date.strftime("%d %b %Y")

    # Convert runtime to hour and minute format
    runtime_hours = movie_details['runtime'] // 60
    runtime_minutes = movie_details['runtime'] % 60
    runtime = f"{runtime_hours}h {runtime_minutes}m"

    # Create a dictionary with all the extracted information
    movies_info = {
        'movieId' : movie_details['movieId'],
        'title': movie_details['title'],
        'poster_working_url': movie_details['poster_working_url'],
        'original_language': movie_details['original_language'],
        'overview': movie_details['overview'],
        'popularity': movie_details['popularity'],
        'budget': movie_details['budget'],
        'genres': genres_str,
        'production_companies': movie_details['production_companies'],
        'production_countries': movie_details['production_countries'],
        'release_date': release_date,  # Formatted release date
        'revenue': movie_details['revenue'],
        'runtime': runtime,  # Runtime in hours and minutes format
        'spoken_languages': movie_details['spoken_languages'],
        'vote_average': movie_details['vote_average'],
        'vote_count': movie_details['vote_count'],
        'keywords': movie_details['keywords'],
        'cast': cast_str,
        'crew': movie_details['crew']
    }
    return movies_info


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    global authenticated

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            authenticated = True
            # Assuming you have a list of movie IDs you want to display on the home page
            movie_ids_your5 = [2, 186, 20, 352, 748]  # Example movie IDs
            movie_ids_rec5 = [3450, 3629, 5096, 5720, 58559]  # Another set of example movie IDs
            
            # Fetch movie details for each set of movie IDs
            movies_data_your5 = [get_movie_details(movie_id) for movie_id in movie_ids_your5]
            movies_data_rec5 = [get_movie_details(movie_id) for movie_id in movie_ids_rec5]
            
            # Pass both sets of movie data to the template for rendering
            return render_template('home.html', authenticated=authenticated, movies_data_your5=movies_data_your5, movies_data_rec5=movies_data_rec5)
        else:
            error_message = "Incorrect email or password. Please try again."
            return render_template('login.html', error_message=error_message)    
    else:
        return redirect(url_for('login'))

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_details(movie_id)
    return render_template('movie_details.html', movie=movie)


if __name__ == '__main__':
    app.run(debug=True)
