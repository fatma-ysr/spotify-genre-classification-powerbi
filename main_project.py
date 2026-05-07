import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import openpyxl

# =============================================================================
# 1. LOAD THE DATA
# =============================================================================
# INSTRUCTIONS: You can load the dataset either directly from Kaggle or from a local path.
# Choose ONE of the methods below and comment out the other.

# -----------------------------------------------------------------------------
# METHOD A: Download Directly from Kaggle (Recommended for cloning/sharing)
# -----------------------------------------------------------------------------
# NOTE: To use this method, you will need your Kaggle username and API key.
# You can generate an API token (kaggle.json) from your Kaggle Account Settings.
# Run the following command in your terminal (requires kaggle CLI):
# pip install kaggle
# kaggle datasets download -d joebeachcapital/30000-spotify-songs
# unzip 30000-spotify-songs.zip


# -----------------------------------------------------------------------------
# METHOD B: Load from a Local Path (Default)
# -----------------------------------------------------------------------------
# Place spotify_songs.csv in the same folder as this script, then run.

local_path = "spotify_songs.csv"
df = pd.read_csv(local_path)

# Display the first few rows to verify
print(df.head())

# =============================================================================
# 2. DROP UNNECESSARY COLUMNS (IDs, Names, and Subgenres)
# =============================================================================
# These columns prevent the model from focusing on audio features.
to_drop = [
    'track_id', 'track_name', 'track_artist', 'track_album_id', 
    'track_album_name', 'track_album_release_date', 
    'playlist_name', 'playlist_id', 'playlist_subgenre'
]
df_model = df.drop(columns=to_drop)

# =============================================================================
# 3. LIST NUMERICAL COLUMNS (For Visualization)
# =============================================================================
numeric_cols = df_model.select_dtypes(include=[np.number]).columns.tolist()

print(f"Prepared Dataset Shape: {df_model.shape}")
print(f"Independent Variables to be Used: {numeric_cols}")

# NOTE: Data Leakage Prevention: By dropping the playlist_subgenre column, 
# we prevented a logical error where the model predicts the main genre from the subgenre.

# =============================================================================
# VARIABLE DEFINITIONS:
# =============================================================================
# # track_popularity: General popularity score of the song on Spotify (0-100).
# # danceability: Suitability for dancing based on tempo and rhythm stability (0.0 - 1.0).
# # energy: Speed, loudness, and overall intensity of the sound; e.g., Metal is high, Classical is low energy.
# # key: The key of the track (numbers from 0 to 11 for C, C#, D, etc.).
# # loudness: Average loudness of the song in decibels (dB) (Usually between -60 and 0).
# # mode: Major (1) or minor (0) scale structure of the song; affects the cheerful or sad tone of the music.
# # speechiness: Word density in the song; above 0.66 is generally speech/rap, below 0.33 is music.
# # acousticness: Probability that the song is made with acoustic (non-electronic) instruments.
# # instrumentalness: Probability that the song contains no vocals (only instrumental).
# # liveness: Probability that the recording was performed live (in front of an audience).
# # valence: Emotional positiveness conveyed by the song (0.0 sad/aggressive, 1.0 happy/cheerful).
# # tempo: The number of beats per minute (BPM) of the song.
# # duration_ms: Total duration of the song in milliseconds.
# # playlist_genre: [TARGET VARIABLE] The main genre the song belongs to (Pop, Rock, Rap, etc.).

# =============================================================================
# VISUALIZATION
# =============================================================================

# -----------------------------------------------------------------------------
# 1. Correlation Heatmap
# -----------------------------------------------------------------------------
plt.figure(figsize=(12, 10))
sns.heatmap(df_model[numeric_cols].corr(), annot=True, cmap='RdBu_r', center=0, fmt='.2f')
plt.title("Correlation Between Numerical Variables")
plt.show()
## Comment
# High positive correlation (0.68) exists between energy and loudness, which might create a risk.
# We can say the same for energy and loudness.

# -----------------------------------------------------------------------------
# 2. Feature Distribution by Genre (Boxplots)
# -----------------------------------------------------------------------------
plt.figure(figsize=(20, 15))
for i, col in enumerate(numeric_cols):
    plt.subplot(4, 4, i+1) # 4 rows, 4 columns layout
    sns.boxplot(x='playlist_genre', y=col, data=df_model, palette="viridis", hue='playlist_genre', legend=False)
    plt.xticks(rotation=45) # Rotated genre names by 45 degrees
    plt.title(f"{col} Distribution", fontsize=12)
plt.tight_layout(pad=3.0) 
plt.show()
## Comment

# -----------------------------------------------------------------------------
# 3. Distribution Analysis (Histograms)
# -----------------------------------------------------------------------------
plt.figure(figsize=(20, 15))
for i, col in enumerate(numeric_cols):
    plt.subplot(4, 4, i+1)
    sns.histplot(df_model[col], kde=True, color="skyblue", bins=30)
    plt.title(f"{col} Frequency Distribution")
plt.tight_layout(pad=3.0)
plt.show()
## Comment
# There is extreme clustering at the value 0 for instrumentalness and speechiness data.
# This situation can negatively affect the model's performance.
# Z-Score Normalization (StandardScaler) can be applied.

# -----------------------------------------------------------------------------
# 4. Pairwise Relationships (Pairplot - Selected Features)
# -----------------------------------------------------------------------------
# A pairplot with all data can be very slow, selecting the 3-4 most important ones:
important_features = ['energy', 'danceability', 'tempo', 'speechiness', 'playlist_genre']
sns.pairplot(df_model[important_features], hue='playlist_genre', corner=True)
plt.show()
## Comment
# Points are very dense and mixed together.
# In this case, algorithms like KNN may experience performance loss.
# Instead, stronger algorithms like Random Forest or XGBoost can be used.

# -----------------------------------------------------------------------------
# 5. Genre Density Analysis with Violin Plots (for critical variables)
# -----------------------------------------------------------------------------
top_features = ['energy', 'speechiness', 'danceability', 'valence']
plt.figure(figsize=(16, 10))
for i, col in enumerate(top_features):
    plt.subplot(2, 2, i+1)
    sns.violinplot(x='playlist_genre', y=col, data=df_model, inner="quart")
    plt.title(f"{col} Genre Density Analysis")

plt.tight_layout()
plt.show()
## Comment

# Hybrid graph providing both types of information
# -----------------------------------------------------------------------------
# 6. Class Distribution (Countplot)
# -----------------------------------------------------------------------------
plt.figure(figsize=(10, 7))
sns.countplot(x='playlist_genre', data=df_model, palette="magma", hue='playlist_genre', legend=False)
plt.title("Distribution of Genres in the Dataset (Class Balance)")
plt.show()
## Comment
# Genres in the dataset are almost balanced.