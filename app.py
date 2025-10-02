import streamlit as st
import pickle
import requests
import time 
# Custom CSS for styling
st.markdown(
    """
    <style>
    /* App background and text */
    .stApp {
        background-color: #141516;
        color: white;
    }

    /* Full selectbox background like button */
    div[role="combobox"] > div {
        background-color: #7a7c84 !important;
        border: 2px solid #7a7c84 !important;
        border-radius: 5px;
        color: white !important;
    }

    /* Dropdown text color */
    div[role="option"] {
        color: black !important;
    }

    /* Default button style */
    button {
        background-color: #7a7c84 !important;
        color: white !important;
        border: 2px solid #7a7c84 !important;
        border-radius: 5px;
    }

    /* Button click style */
    button:active {
        background-color: black !important;
        color: red !important;
        border: 2px solid red !important;
    }

    /* All other text white */
    p, h1, h2, h3, h4, h5, h6, label, span {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=522de07951caa2d0e06014b60ea5d043&language=en-US"
    alternate_poster = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_image_available_600_x_450.svg"

    for attempt in range(3):
        try:
            print(f"Fetching poster for movie ID: {movie_id} (Attempt {attempt+1})")
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            print("API Response received:", data.keys())  # Debug

            poster_path = data.get('poster_path')
            print("Poster Path:", poster_path)  # Debug

            if poster_path and isinstance(poster_path, str):
                return "https://image.tmdb.org/t/p/w500" + poster_path
            else:
                return alternate_poster

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if attempt < 2:
                time.sleep(2)
                continue
            return alternate_poster

    return alternate_poster


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Your movie journey starts here .Find your next favorite movie!',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <p style="color:white; font-weight:bold; font-size:16px;">{names[idx]}</p>
                    <img src="{posters[idx]}" style="width:100%; border-radius:10px;">
                </div>
                """,
                unsafe_allow_html=True
            )

