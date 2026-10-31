import pandas as pd
import pickle
import streamlit as st
import requests
import pandas as pd
import os

import requests
import streamlit as st


import requests
import streamlit as st


API_KEY = st.secrets["TMDB_API_KEY"]
@st.cache_data(ttl=86400)
def fetch_posters(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:
        response = requests.get(
            url,
            params={"api_key": API_KEY},
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except requests.exceptions.RequestException as e:
        print("Poster fetching error:", e)
        return None




movies = pickle.load(open('movies.pkl', 'rb'))
print(movies.columns.tolist())
print(movies.head())
print(movies.columns.tolist())
similaritity = pickle.load(open('similaritity.pkl', 'rb'))
def recommend(movie):
    movie_index=movies[movies['title'] == movie].index[0]
    distances=similaritity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_posters(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movies_posters



# Streamlit application
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])

            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster unavailable")