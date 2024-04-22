# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from datetime import datetime
import json
import numpy as np
import string
import pickle
import io
import torch
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

# Dummy user data for login
users = {
    'user': 'user',
    'admin': 'admin'
}

authenticated = False

movie_ids_your5 = [2, 134234, 20, 96079, 748]  # Example movie IDs
movie_ids_rec5 = [3450, 3629, 5096, 5720, 58559]

# Load data from Excel file into a pandas DataFrame
movies_df = pd.read_csv('static/movies_data3200.csv')

# Loading Image2Vec Similarity JSON 
with open('static/sorted_similarity.json', 'r') as file:
    sorted_similarity = json.load(file)

posters_like_this_dict = {}
for key, value in sorted_similarity.items():
    posters_like_this_dict[int(key)] = value[:5]

# Integrating DistilBert with Search
with open('static/encodings_description.pickle','rb') as file:
    encoded_data = pickle.load(file)

class CPU_Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'torch.storage' and name == '_load_from_bytes':
            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
        else:
            return super().find_class(module, name)
        
with open('static/model.pickle','rb') as file:
    model = CPU_Unpickler(file).load()

def find_similar_items(query: str, metadata: pd.DataFrame, model: SentenceTransformer = model, encodings: np.array = encoded_data, top_n: int = 5):
    query_vector = model.encode([query])
    # print(query_vector)
    similarity = np.dot(encodings,query_vector.T)
    # print(similarity)
    top_items = similarity.flatten().argsort()[-top_n:][::-1]
    # print(top_items)
    # return metadata['asin'].iloc[top_items]
    return list(metadata['movieId'].iloc[top_items].values)

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
    rel_date_obj = datetime.strptime(rel_date, '%Y-%m-%d')
    release_date = rel_date_obj.strftime("%d %b %Y")

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

            return render_template('home.html', authenticated=authenticated, movie_ids_your5=movie_ids_your5, movie_ids_rec5=movie_ids_rec5, posters_like_this_dict = posters_like_this_dict, get_movie_details=get_movie_details)
        else:
            error_message = "Incorrect email or password. Please try again."
            return render_template('login.html', error_message=error_message)    
    else:
        return redirect(url_for('login'))

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_details(movie_id)
    return render_template('movie_details.html', movie=movie, authenticated=authenticated, posters_like_this_dict=posters_like_this_dict, get_movie_details=get_movie_details)

@app.route('/search', methods=['POST'])
def search_movies():
    search_query = request.form['search_query']
    search_results = find_similar_items(search_query, movies_df)
    return render_template('home.html', authenticated=authenticated, movie_ids_your5=movie_ids_your5, movie_ids_rec5=movie_ids_rec5, posters_like_this_dict=posters_like_this_dict, search_results=search_results, get_movie_details=get_movie_details)

# Gemini Chatbot Integration
# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_instruction = "Friendly Lively tone"

gemini_model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

chat = gemini_model.start_chat(history=[
    {
        "role": "user",
        "parts": ["You are a friendly Chatbot named CavBot named after our awesome professor James Caverlee, Our team (Harshit, Rahul, Saptarshi and Kanak) have developed a Movie Recommendation Website named MFlix which provides recommendations for movies to users and retrieves query results which is integrated with DistilBert, for each movie we have displayed all the informations like Cast, Overview, Genre, Movie length etc. Also we are also displaying top 5 most similar poster for movies for each movie. Your task is to interact with user, ask about there mood, what kind of movie they want to watch what they are looking for in a movie and many other information in a friendly way and then provide me with a query at the end which I will feed to my distilbert model and provide recommendations. The info I have from my data is overview of the movie, genre, cast and title. My data was taken from movie lens but I am just using a small chunk of 3200 movies, so don't recommend any movie from your end, just interact with user and gather information to give a very nice keyword loaded query. The query should be a long sentence with very precise information based on the convesation with the user, when I say give me search query, provide just this query and nothing else.\n\nAlso, during the first message with the user, always greet them friendly and mention that your name is derived from our awesome professor James Caverlee"]
    },
    {
        "role": "model",
        "parts": ["Hey there! 👋 I'm CavBot, named after the awesome professor James Caverlee!  So, tell me, are you ready for a movie night? 🍿 What kind of mood are you in and what are you looking for in a movie tonight? 🤔 🎬"]
    },
    {
        "role": "user",
        "parts": ["I am looking for a horror movie"]
    },
    {
        "role": "model",
        "parts": ["Ooh, a horror fan! 👻 Do you prefer something classic and spooky or a more modern gore-fest? And are there any particular themes or monsters that you"]
    },
    {
        "role": "user",
        "parts": ["I prefer a classic movie"]
    },
    {
        "role": "model",
        "parts": ["A classic horror movie it is! 🎬 Any favorite directors or actors you'd like to see in your movie? Or maybe a specific decade you'd like to explore?"]
    },
    {
        "role": "user",
        "parts": ["No I don't know any famous horror movie actor name"]
    },
    {
        "role": "model",
        "parts": ["No worries at all!  How about the overall vibe you're looking for? Should it be suspenseful and psychological, or more on the jump-scare side of things? 😨"]
    },
    {
        "role": "user",
        "parts": ["suspensful"]
    },
    {
        "role": "model",
        "parts": ["Okay, suspenseful it is! 😨  Now, just to clarify, are we sticking purely to horror, or are you open to a bit of thriller or mystery mixed in? 🕵️‍♀️"]
    },
    {
        "role": "user",
        "parts": ["Yes thriller will be nice"]
    },
    {
        "role": "model",
        "parts": ["Sounds good! A classic, suspenseful horror-thriller it is then! 😄 Give me just a sec to cook up the perfect query for your movie recommendation... \n\nGive me search query"]
    },
    {
        "role": "user",
        "parts": ["Give me a search query"]
    },
    {
        "role": "model",
        "parts": ["Sounds good! A classic, suspenseful horror-thriller it is then! 😄 Give me just a sec to cook up the perfect query for your movie recommendation... \n\nGive me search query"]
    },
    {
        "role": "user",
        "parts": ["Give me a search query"]
    },
    {
        "role": "model",
        "parts": ["Classic horror thriller movie with suspenseful plot"]
    },
])

@app.route('/cavbot', methods=['POST'])
def gemini_chatbot():
    # Get user input from the request
    user_input = request.form.get('user_input')

    # Send user input to the chatbot
    response = chat.send_message(user_input, stream=True)

    # Extract and format the response from the chatbot
    bot_response = ""
    for chunk in response:
        bot_response += chunk.text

    # Return the chatbot's response as JSON
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
