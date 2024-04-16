# app.py

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Dummy user data for login
users = {
    'user': 'user',
    'admin': 'admin'
}

authenticated = False

# Load data from Excel file into a pandas DataFrame
movies_df = pd.read_excel('movies_data.xlsx')

# Define a function to fetch movie details by movieId
def get_movie_details(movie_id):
    movie_details = movies_df[movies_df['movieId'] == movie_id].iloc[0]
    return {
        'title': movie_details['title'],
        'poster_working_url': movie_details['poster_working_url']
        # Add more fields as needed
    }


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

if __name__ == '__main__':
    app.run(debug=True)
