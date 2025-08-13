import streamlit as st
import pandas as pd
import requests
import pickle

similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=14a52afe6744ea05cc5f1a378dc6b5a7'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended, recommended_poster = [], []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movie_id))
    return recommended, recommended_poster

st.title("🎬 Movie Recommender System")
st.markdown("### Pick a movie you like, and we'll suggest 5 similar ones!")

selected_option = st.selectbox("📌 Select a Movie", movies['title'].values)

if st.button("🔍 Recommend"):
    names, posters = recommend(selected_option)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        h1 {
            text-align: center;
            color: #FF4B4B;
        }
        .movie-title {
            text-align: center;
            font-weight: bold;
            color: #fff;
            font-size: 16px;
        }
        .stImage > img {
            border-radius: 15px;
            transition: transform 0.2s ease-in-out;
        }
        .stImage > img:hover {
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)
