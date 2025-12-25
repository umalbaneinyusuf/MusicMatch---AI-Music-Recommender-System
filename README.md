# MusicMatch — AI Music Recommender System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-blue?logo=streamlit)](https://musicmatch---ai-music-recommender-system-t9qg7sqnj9nqi4wnvx3bq.streamlit.app/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](#license)

A content-based music recommender that suggests similar tracks given a user's input song. MusicMatch analyzes audio and metadata features, computes similarity using cosine similarity, and surfaces human-readable explanations for each recommendation through a Streamlit web interface.

---

Table of Contents
- Overview
- Live Demo
- Features
- Quick Start
- Installation
- Usage
- File Structure
- Data & Preprocessing
- Methodology
- Explainability
- Notes & Recommendations
- Contributing
- License
- Contact

---

## Overview

MusicMatch is a lightweight, explainable, content-based recommender system built for research and educational use. Given a song title (and optionally an artist), the app finds the closest match in the dataset (robust to typos) and returns a ranked set of similar songs along with match percentages and a concise explanation for each recommendation.

Key capabilities:
- Fuzzy/robust matching of user input
- Feature scaling and cosine-similarity based ranking
- Simple, intuitive Streamlit-based UI
- Explainability based on shared genres, artist similarity, and popularity signals

This project was developed as part of coursework at the University of Information Technology and Communications — College of Business Information.

Author: Um Al-Banein Yusuf

---

## Live Demo

Try the live application here:
https://musicmatch---ai-music-recommender-system-t9qg7sqnj9nqi4wnvx3bq.streamlit.app/

Click the "Live Demo" badge at the top to open the deployed Streamlit app.

---

## Features

- Search by song title (fuzzy matching — tolerates typos)
- Top-N recommendations with percentage match scores
- Visual grid of recommendations (cover art support if provided)
- Short explanation for each suggested track (genres, same artist, popularity)
- Fast inference with precomputed feature vectors and efficient cosine similarity

---

## Quick Start

Clone the repository and run the Streamlit app:

```bash
git clone https://github.com/umalbaneinyusuf/MusicMatch---AI-Music-Recommender-System.git
cd MusicMatch---AI-Music-Recommender-System
pip install -r requirements.txt    # or see Install below
python -m streamlit run recommender_engine.py
```

Open http://localhost:8501 in your browser if Streamlit doesn't open automatically.

---

## Installation

Install required packages:

```bash
pip install streamlit pandas numpy scikit-learn fuzzywuzzy python-Levenshtein
```

Alternatively, create a `requirements.txt` with:

```
streamlit
pandas
numpy
scikit-learn
fuzzywuzzy
python-Levenshtein
```

and install with:

```bash
pip install -r requirements.txt
```

Notes:
- `python-Levenshtein` is recommended to speed up fuzzy matching.
- Consider replacing `fuzzywuzzy` with `rapidfuzz` for better performance in large-scale systems.

---

## Usage

1. Ensure `recommender_engine.py`, `track_data_final.csv`, and `logo.png` are present in the project root.
2. Run the app with Streamlit (see Quick Start).
3. Type a song name (e.g., "The Hills by The Weeknd") into the search box.
4. Review the matched track and the grid of recommended songs with explanations.

Example:
- Input: "Blinding Lights"
- Output: Closest dataset match + top 10 similar tracks with match scores and why each was chosen.

---

## File Structure

- recommender_engine.py — main Streamlit app and recommender logic
- track_data_final.csv — dataset of tracks and features
- logo.png — app icon used in the browser tab
- README.md — project documentation

(If you add additional scripts, models, or notebooks, list them here for clarity.)

---

## Data & Preprocessing

Dataset: track_data_final.csv

Preprocessing steps implemented in the project:
- Missing value removal
- Duplicate handling (track + artist deduplication)
- Feature selection and normalization
- Numerical features scaled to [0, 1] using MinMaxScaler
- Track duration excluded to prioritize stylistic similarity over length

If you plan to extend the dataset:
- Keep consistent column names and feature semantics
- Recompute scaling and vectors after updates

---

## Methodology

- Input normalization → map user input to nearest dataset title via fuzzy matching
- Feature vector construction → numeric features (popularity, followers, genre indicators, etc.)
- Feature scaling → MinMaxScaler
- Similarity calculation → Cosine similarity on feature vectors
- Ranking → Retrieve top-K most similar tracks
- Output → Present result set with match percentages and textual justifications

---

## Explainability

Each recommendation includes a short explanation derived from:
- Genre overlap (shared genre tags)
- Artist match (same artist boosts similarity)
- Popularity relationship (mainstream vs. niche)
These explanations help users understand why tracks were recommended and improve trust.

---

## License

This project is provided under the MIT License. See LICENSE for details.

---

## Author

Um Al-Banein Yusuf  

---
