# APHELION_LAB
Data analysis of NASA exoplanet datasets using Python, SQL, and visualization

# 🌌 Exoplanet Data Explorer

A data analytics project that explores confirmed exoplanets using real datasets from NASA’s Exoplanet Archive.  
The project demonstrates end-to-end data handling: API ingestion, cleaning, SQL storage, statistical analysis, and visualization.

---

## 🚀 Project Overview

This project fetches exoplanet data from NASA’s Exoplanet Archive and analyzes relationships between planetary and stellar properties such as:

- Planet radius vs. host star temperature
- Orbital period distributions
- Identification of potentially Earth-like exoplanets

The goal is to showcase practical data engineering and analysis skills using real scientific datasets.

---

## 🧠 Key Features

- 📡 Fetches real exoplanet data via NASA Exoplanet Archive API
- 🧹 Data cleaning and preprocessing using Pandas & NumPy
- 🗄️ SQL database backend for structured querying
- 📊 Statistical analysis and correlation studies
- 📈 Visualizations using Matplotlib & Seaborn
- 🧪 Reproducible Jupyter notebooks

---

## 🛠️ Tech Stack

- **Language:** Python
- **Data Handling:** Pandas, NumPy
- **Database:** SQLite / PostgreSQL
- **Visualization:** Matplotlib, Seaborn
- **APIs:** NASA Exoplanet Archive
- **Optional UI:** Streamlit

---

## 📁 Project Structure

exoplanet-data-explorer/
│
├── data/
│   ├── raw/                # Original API / CSV data (read-only)
│   ├── processed/          # Cleaned & transformed datasets
│
├── notebooks/
│   ├── 01_data_fetch.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   ├── 04_statistical_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── nasa_exoplanet_api.py
│   │
│   ├── data_processing/
│   │   ├── __init__.py
│   │   └── cleaner.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── correlations.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── db_manager.py
│   │
│   └── visualization/
│       ├── __init__.py
│       └── plots.py
│
├── sql/
│   ├── schema.sql
│   └── example_queries.sql
│
├── dashboard/
│   └── app.py               # (Optional) Streamlit dashboard
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md


# Load dataset
print(" Loading exoplanet data...")
df = pd.read_csv("data/raw/exoplanets.csv")

print("\n Data loaded successfully!")

# 1️ Basic shape of the data
print("\n Dataset shape (rows, columns):")
print(df.shape)

# 2️ Column names
print("\n Column names:")
print(list(df.columns))

# 3️ Preview first rows
print("\n First 5 rows:")
print(df.head())

# 4️ Data types
print("\n Data types:")
print(df.dtypes)

# 5 Missing values count
print("\n Missing values per column:")
print(df.isnull().sum())

# 6️ Basic statistics for numeric columns
print("\n Basic statistics:")
print(df.describe())
