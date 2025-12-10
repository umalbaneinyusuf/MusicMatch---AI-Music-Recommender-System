import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from fuzzywuzzy import process
import ast

st.set_page_config(
    page_title="MusicMatch",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown(f"""
<style>

    .stApp {{
        background-color: #121212;
    }}


    h1 {{
        color: white;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: 0px;
        padding-top: 20px;
    }}

    .subtitle {{
        text-align: center;
        color: #e0e0e0;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }}

    div[data-testid="stMetricValue"] {{
        font-size: 24px;
        color: #1db954;
    }}

    div.stButton > button:first-child {{
        background-color: #1db954;
        color: white;
        border-radius: 20px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        height: 45px;
        margin-top: 0px;
    }}
    div.stButton > button:first-child:hover {{
        background-color: #1ed760;
        transform: scale(1.05);
    }}

    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #191414;
        color: #b3b3b3;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #282828;
        z-index: 100;
    }}
</style>
""", unsafe_allow_html=True)


class MusicRecommender:
    def __init__(self, file_path="track_data_final.csv"):
        try:
            self.df = pd.read_csv(file_path)
        except FileNotFoundError:
            st.error(f"Error: The file '{file_path}' was not found.")
            st.stop()

        required_cols = ['track_name', 'artist_name', 'track_popularity', 'artist_genres']
        missing = [c for c in required_cols if c not in self.df.columns]
        if missing:
            st.error(f"Error: Missing columns: {missing}")
            st.stop()

        self.df.dropna(subset=required_cols, inplace=True)
        self.df.drop_duplicates(subset=['track_name', 'artist_name'], keep='first', inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        self.df['genres_list'] = self.df['artist_genres'].apply(self._parse_genres)

        self.numeric_cols = [
    'track_popularity', 'artist_popularity', 'artist_followers', 'explicit'
]
        self.used_cols = [c for c in self.numeric_cols if c in self.df.columns]
        self.df[self.used_cols] = self.df[self.used_cols].fillna(0)

        scaler = MinMaxScaler()
        self.features_matrix = scaler.fit_transform(self.df[self.used_cols])
        self.cosine_sim = cosine_similarity(self.features_matrix)

    def _parse_genres(self, val):
        try:
            if pd.isna(val) or val == "[]" or val == "N/A": return []
            return ast.literal_eval(val)
        except:
            return []

    def find_song(self, user_input):
        search_list = (self.df['track_name'] + " " + self.df['artist_name']).tolist()
        match = process.extractOne(user_input, search_list, score_cutoff=60)
        if match:
            idx = search_list.index(match[0])
            return idx, self.df.iloc[idx]
        return None, None

    def explain_recommendation(self, input_song, rec_song):
        reasons = []
        if input_song['artist_name'] == rec_song['artist_name']:
            return f"🎵 Same artist: **{input_song['artist_name']}**."

        input_genres = set(input_song['genres_list'])
        rec_genres = set(rec_song['genres_list'])
        common = list(input_genres.intersection(rec_genres))
        if common:
            reasons.append(f"Shares genre: *{', '.join(common[:2])}*")

        pop_diff = rec_song['track_popularity'] - input_song['track_popularity']
        if pop_diff > 20: reasons.append("More popular hit 🔥")
        elif pop_diff < -20: reasons.append("Hidden gem 💎")

        if reasons:
            return " • ".join(reasons)
        else:
            return "Statistical match (Sound & Vibe)"

    def get_recommendations(self, song_name, top_n=5):
        idx, input_song = self.find_song(song_name)
        if idx is None:
            return None, None

        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_indices = sim_scores[1:top_n+1]

        results = []
        for i, score in top_indices:
            rec_song = self.df.iloc[i]
            explanation = self.explain_recommendation(input_song, rec_song)
            results.append({
                "song": rec_song['track_name'],
                "artist": rec_song['artist_name'],
                "score": round(score * 100, 1),
                "reason": explanation
            })
        return input_song, results


@st.cache_resource
def load_engine():
    return MusicRecommender("track_data_final.csv")

try:
    engine = load_engine()
except Exception as e:
    st.error("Please make sure 'track_data_final.csv' is in the same folder!")
    st.stop()


st.title("MusicMatch")
st.markdown('<div class="subtitle">Your next obsession starts here</div>', unsafe_allow_html=True)



col1, col2 = st.columns([4, 1], vertical_alignment="bottom") 

with col1:
    user_input = st.text_input("Search", placeholder="e.g., 'The Hills by The Weeknd'", label_visibility="collapsed")

with col2:

    search_btn = st.button("Recommend", type="primary", use_container_width=True)


if search_btn and user_input:
    with st.spinner('Analyzing audio features...'):

        input_song, recommendations = engine.get_recommendations(user_input)

    if input_song is not None:
        st.markdown("---")

        st.markdown(f"<h3 style='text-align: center; color: white;'>Selected: {input_song['track_name']} <span style='color: #b3b3b3; font-size: 0.8em;'>by {input_song['artist_name']}</span></h3>", unsafe_allow_html=True)
        st.write("") 

        st.subheader("Top Recommendations")

        cols = st.columns(3)
        
        for i, rec in enumerate(recommendations):
            with cols[i % 3]:
                with st.container(border=True):

                    st.markdown(f"**{rec['song']}**")

                    st.caption(f"👤 {rec['artist']}")
                    

                    st.metric(label="Match Score", value=f"{rec['score']}%")
                    

                    st.info(f"{rec['reason']}")

    else:
        st.error("Could not find that song! Please check the spelling.")

elif search_btn:
    st.warning("⚠️ Please enter a song name first!")

st.markdown("""
<div class="footer">
    Designed & Developed by <b>Um Al-Banein Yusuf</b>
</div>
""", unsafe_allow_html=True)
