# spotify-genre-classification-powerbi
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI"/>
  <img src="https://img.shields.io/badge/Kaggle-Dataset-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white" alt="Kaggle"/>
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Seaborn-Visualization-444876?style=for-the-badge&logoColor=white" alt="Seaborn"/>
</p>

<h1 align="center">🎵 Spotify Genre — Exploratory Data Analysis</h1>

<p align="center">
  <strong>Analyzing audio features of 30,000+ Spotify tracks across 6 music genres</strong><br/>
  <em>Exploratory Data Analysis (EDA) · Data Cleaning · Power BI Dashboard</em>
</p>

<p align="center">
  <a href="#-about-the-project">About</a> •
  <a href="#-dataset">Dataset</a> •
  <a href="#-technologies">Technologies</a> •
  <a href="#-exploratory-data-analysis">EDA</a> •
  <a href="#-data-cleaning">Data Cleaning</a> •
  <a href="#-power-bi-dashboard">Power BI</a> •
  <a href="#-setup">Setup</a> •
  <a href="#-project-structure">Structure</a>
</p>

---

## 📌 About the Project

This project explores the **audio characteristics** of Spotify tracks (danceability, energy, tempo, speechiness, etc.) to uncover patterns and differences across **six music genres**.

The analysis consists of two main stages:

| Stage | Tool | Description |
|-------|------|-------------|
| **Exploratory Data Analysis** | Python (Pandas, Seaborn, Matplotlib) | Correlation analysis, distribution plots, outlier detection |
| **Interactive Dashboard** | Power BI | Genre-based comparisons and visual storytelling |

---

## 📊 Dataset

> **Source:** [30,000 Spotify Songs — Kaggle](https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs?select=spotify_songs.csv)

| Info | Value |
|------|-------|
| Rows | ~32,833 |
| Columns | 23 |
| Target Variable | `playlist_genre` |
| Genres | Pop, Rock, Rap, R&B, Latin, EDM |

### 🔑 Key Features

| Feature | Description | Range |
|---------|-------------|-------|
| `danceability` | How suitable a track is for dancing based on tempo and rhythm stability | 0.0 – 1.0 |
| `energy` | Perceptual measure of intensity — fast, loud, noisy tracks score higher | 0.0 – 1.0 |
| `speechiness` | Presence of spoken words; values above 0.66 are mostly speech/rap | 0.0 – 1.0 |
| `acousticness` | Likelihood that the track was made with acoustic instruments | 0.0 – 1.0 |
| `instrumentalness` | Likelihood that the track contains no vocals | 0.0 – 1.0 |
| `liveness` | Probability that the track was recorded live with an audience | 0.0 – 1.0 |
| `valence` | Musical positiveness; 0.0 → sad/angry, 1.0 → happy/cheerful | 0.0 – 1.0 |
| `tempo` | Beats per minute (BPM) | > 0 |
| `loudness` | Average volume in decibels (dB) | -60 – 0 |
| `duration_ms` | Track duration in milliseconds | > 0 |
| `key` | Musical key of the track (C, C#, D, … mapped to 0–11) | 0 – 11 |
| `mode` | Major (1) or Minor (0) scale | 0 / 1 |
| `track_popularity` | Spotify popularity score | 0 – 100 |

---

## 🛠 Technologies

<table>
<tr>
  <td align="center"><strong>Language & Libraries</strong></td>
  <td align="center"><strong>Statistics</strong></td>
  <td align="center"><strong>Visualization</strong></td>
</tr>
<tr>
  <td>
    <code>Python 3.10+</code><br/>
    <code>Pandas</code><br/>
    <code>NumPy</code>
  </td>
  <td>
    <code>SciPy</code><br/>
    <code>Correlation Analysis</code><br/>
    <code>Distribution Analysis</code>
  </td>
  <td>
    <code>Matplotlib</code><br/>
    <code>Seaborn</code><br/>
    <code>Power BI</code>
  </td>
</tr>
</table>

---

## 🔍 Exploratory Data Analysis

### 1️⃣ Correlation Heatmap
Visualizes pairwise correlations between all numerical features.

> **Finding:** A strong positive correlation (**0.68**) was detected between `energy` and `loudness`. This indicates potential multicollinearity and should be considered when building predictive models.

### 2️⃣ Boxplots — Feature Distribution by Genre
Each numerical feature is compared across genres using box plots to identify separability and outliers.

### 3️⃣ Frequency Distributions (Histograms)
Histograms with KDE overlays reveal the overall shape of each feature's distribution.

> **Finding:** `instrumentalness` and `speechiness` exhibit extreme **zero-inflation** — the vast majority of values are concentrated at 0. This skewness may require special handling (e.g., log transformation or binning).

### 4️⃣ Pairwise Relationships (Pairplot)
Scatter plots of `energy`, `danceability`, `tempo`, and `speechiness` colored by genre.

> **Finding:** Data points are heavily overlapping across genres, suggesting that simple distance-based methods would struggle with this data. Ensemble methods would be more suitable for any classification tasks.

### 5️⃣ Violin Plots — Genre Density Analysis
Density distributions of critical features (`energy`, `speechiness`, `danceability`, `valence`) are compared across genres, combining boxplot and KDE information in a single chart.

### 6️⃣ Class Balance Check (Countplot)
Verifies whether the target variable is balanced across genres.

> **Finding:** All six genres have **approximately equal representation** in the dataset — no oversampling or undersampling would be needed.

---

## 🧹 Data Cleaning

Logical filters applied to remove invalid records:

```python
df_clean = df_model[
    (df_model['tempo'] > 0) &             # Tempo must be positive
    (df_model['duration_ms'] >= 10000) &   # Duration must be at least 10 seconds
    (df_model['loudness'] <= 0)            # Loudness must be 0 or negative (dB scale)
].copy()
```

Additionally, the following columns were dropped as they are identifiers or free-text fields irrelevant to audio analysis:

`track_id` · `track_name` · `track_artist` · `track_album_id` · `track_album_name` · `track_album_release_date` · `playlist_name` · `playlist_id` · `playlist_subgenre`

> **Note:** `playlist_subgenre` was specifically excluded to prevent **data leakage** — avoiding a scenario where genre could be trivially inferred from its subgenre label.

---

## 📈 Power BI Dashboard

An interactive Power BI dashboard was built for visual exploration. The `.pbit` template file is included in the repository.

**Dashboard highlights:**
- Audio feature comparisons across genres
- Popularity vs. energy relationship
- Genre-level distribution breakdowns

> 📥 Open `spotify-genre.pbit` with Power BI Desktop to explore the report.

---

## 🚀 Setup

### Requirements

```bash
pip install pandas numpy seaborn matplotlib scipy openpyxl
```

### Run

```bash
# 1. Clone the repository
git clone https://github.com/<YOUR_USERNAME>/spotify-genre-analysis.git
cd spotify-genre-analysis

# 2. Download the dataset
# https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs

# 3. Run the analysis script
python main_project.py
```

---

## 📁 Project Structure

```
spotify-genre-analysis/
│
├── README.md                  # Project documentation
├── main_project.py            # Exploratory data analysis script
├── spotify_songs.csv          # Raw dataset (from Kaggle)
├── spotify-genre.pbit         # Power BI template file
│
└── screenshots/               # (Optional) Charts and dashboard screenshots
    ├── heatmap.png
    ├── boxplots.png
    ├── pairplot.png
    └── powerbi_dashboard.png
```

---

## 📝 Notes & Future Work

- [ ] Apply StandardScaler normalization to skewed features
- [ ] Log-transform zero-inflated features (`instrumentalness`, `speechiness`)
- [ ] Export key visualizations as high-resolution PNGs
- [ ] Add detailed Power BI dashboard screenshots to README
- [ ] Investigate genre-level feature importance with statistical tests

---

## 📜 License

This project was created for educational purposes. The dataset is sourced from [Kaggle](https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs).

---

<p align="center">
  <strong>⭐ If you found this useful, consider giving the repo a star!</strong>
</p>
