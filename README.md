# MusicMatch - AI Music Recommender System

## 1. Project Overview

**MusicMatch** is an intelligent **content-based music recommender
system** designed to suggest similar tracks based on a user's input
song.\
The system uses a modern **Streamlit Web Interface** and analyzes key
audio-related features such as:

-   Track Popularity\
-   Artist Followers\
-   Genres

Similarity between tracks is calculated using the **Cosine Similarity**
metric.

This project was submitted to the:\
**University of Information Technology and Communications -- College of
Business Information**

**Submitted By:** Um Al-Banein Yaqub Yusuf\
**Supervisors:** Dr. Samerra Faris, Dr. Zainab Khudair\
**Programming Language:** Python\
**Dataset:** `track_data_final.csv`

---

## 2. Project Requirements and Installation

### A. Required Python Libraries

Install all dependencies using:

``` bash
pip install streamlit pandas numpy scikit-learn fuzzywuzzy
```

### Library Usage Overview

  Library            Purpose in the Project
  ------------------ ---------------------------------------------------
  **streamlit**      Builds the interactive web interface (dashboard)
  **pandas**         Data handling, CSV loading, duplicate removal
  **numpy**          Numerical operations for vector calculations
  **scikit-learn**   MinMaxScaler + cosine_similarity (core algorithm)
  **fuzzywuzzy**     Fuzzy Matching for robust input handling

----

### B. File Structure

Place the following files in the same directory:

    recommender_engine.py   # Main system logic + Streamlit UI
    track_data_final.csv    # Dataset containing track features
    logo.png                # App icon used in the browser tab

---

## 3. Execution Instructions

### 3.1 Run the Application

In your terminal, navigate to the project folder and run:

``` bash
python -m streamlit run recommender_engine.py
```

### 3.2 System Interaction

After launching, Streamlit will open automatically in your browser
(usually at):

    http://localhost:8501

-   **Search:** Enter a song name (e.g., "The Hills")\
-   **Results:**
    -   The closest matched track (via Fuzzy Matching)\
    -   A grid of recommended songs\
    -   Match percentages\
    -   A logical explanation for each recommendation

### 3.3 Exit the Application

To stop the Streamlit server:

    Ctrl + C

----

## 4. Technical Summary for Evaluation

### Data Cleaning

-   Automatic removal of missing values\
-   Duplicate handling based on track and artist names to ensure unique
    recommendations

### Feature Scaling

-   Uses **MinMaxScaler** to normalize numerical features to a `[0, 1]`
    range\
-   Track duration was intentionally excluded to prioritize stylistic
    similarity over length

### Similarity Metric

-   Core similarity is computed using **Cosine Similarity** between
    feature vectors

### Robust Input Handling

-   `fuzzywuzzy` matches user input to the closest existing song\
-   A minimum match score (≥ 60) ensures relevant results and typo
    tolerance

### Explainability Module

Each recommendation is supported by a clear justification based on:

-   Shared Genres\
-   Same Artist similarity\
-   Popularity Trends: Mainstream Hits vs. Hidden Gems

---
