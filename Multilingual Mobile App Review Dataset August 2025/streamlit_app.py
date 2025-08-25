# Author: Sandeep Malviya
# Purpose: An interactive Streamlit dashboard for analysing and visualizing
# the "Multilingual Mobile App Reviews Dataset 2025" from Kaggle.
# This app allows users to filter the data and explore insights dynamically.

import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
import os
import warnings

warnings.filterwarnings('ignore')

# --- Page Configuration ---
st.set_page_config(
    page_title="Mobile App Review Dashboard",
    page_icon="📱",
    layout="wide",
)

# --- Custom Styling ---
# A little bit of CSS to make the dashboard look cleaner.
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        font-size: 0.9rem;
        color: #888;
    }
    .footer a {
        color: #1f77b4;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)


# --- Data Loading & Caching ---
@st.cache_data(ttl=3600) # Cache the data for 1 hour
def load_and_process_data():
    """
    Downloads, cleans, and engineers features for the dataset.
    This function is cached to avoid re-running on every interaction.
    """
    try:
        # 1. Load Data from Kaggle
        with st.spinner("Downloading latest dataset from Kaggle Hub..."):
            path = kagglehub.dataset_download(
                "pratyushpuri/multilingual-mobile-app-reviews-dataset-2025"
            )
            csv_path = os.path.join(path, 'multilingual_mobile_app_reviews_2025.csv')
            df = pd.read_csv(csv_path)

        # 2. Clean and prepare the data
        df = clean_data(df)

        # 3. Add new features for deeper analysis
        df = add_custom_features(df)
        return df

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

def clean_data(df):
    """Handles missing values, data types, and basic formatting."""
    df_clean = df.copy()
    df_clean.dropna(subset=['review_text'], inplace=True)

    # Fix data types, filling missing numerical values with the median
    df_clean['rating'] = pd.to_numeric(df_clean['rating'], errors='coerce').fillna(df_clean['rating'].median())
    df_clean['user_age'] = df_clean['user_age'].fillna(df_clean['user_age'].median()).astype(int)
    df_clean['num_helpful_votes'] = pd.to_numeric(df_clean['num_helpful_votes'], errors='coerce').fillna(0).astype(int)
    df_clean['review_date'] = pd.to_datetime(df_clean['review_date'], errors='coerce')

    # Fill categorical missing values with 'Unknown'
    for col in ['user_country', 'user_gender', 'app_version']:
        df_clean[col].fillna('Unknown', inplace=True)

    # Standardize app version format
    df_clean['app_version'] = df_clean['app_version'].astype(str).str.lstrip('v')
    return df_clean

def add_custom_features(df):
    """Engineers new features for analysis."""
    df_enhanced = df.copy()

    # Text-based features
    df_enhanced['review_length'] = df_enhanced['review_text'].str.len()
    df_enhanced['review_word_count'] = df_enhanced['review_text'].str.split().str.len()

    # Time-based features
    df_enhanced['review_year'] = df_enhanced['review_date'].dt.year
    df_enhanced['review_month'] = df_enhanced['review_date'].dt.month

    # Derived categories for easier grouping and visualization
    rating_bins = [0, 1.9, 2.9, 3.9, 4.4, 5]
    rating_labels = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent']
    df_enhanced['rating_category'] = pd.cut(df_enhanced['rating'], bins=rating_bins, labels=rating_labels, include_lowest=True)

    age_bins = [0, 17, 24, 34, 49, 100]
    age_labels = ['Teen', 'Young Adult', 'Adult', 'Middle Age', 'Senior']
    df_enhanced['age_group'] = pd.cut(df_enhanced['user_age'], bins=age_bins, labels=age_labels, include_lowest=True)

    return df_enhanced


# --- UI & Filtering ---
def setup_sidebar(df):
    """Creates the sidebar with all the data filters."""
    st.sidebar.header("🔍 Data Filters")

    app = st.sidebar.selectbox("Select App", ['All'] + sorted(df['app_name'].unique()))
    category = st.sidebar.selectbox("Select Category", ['All'] + sorted(df['app_category'].unique()))
    rating_range = st.sidebar.slider(
        "Rating Range",
        min_value=1.0, max_value=5.0,
        value=(1.0, 5.0), step=0.1
    )
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(df['review_date'].min().date(), df['review_date'].max().date()),
        min_value=df['review_date'].min().date(),
        max_value=df['review_date'].max().date()
    )
    return app, category, rating_range, date_range

def filter_dataframe(df, app, category, rating_range, date_range):
    """Applies the user's filters to the main dataframe."""
    filtered_df = df.copy()
    if app != 'All':
        filtered_df = filtered_df[filtered_df['app_name'] == app]
    if category != 'All':
        filtered_df = filtered_df[filtered_df['app_category'] == category]

    filtered_df = filtered_df[
        (filtered_df['rating'] >= rating_range[0]) &
        (filtered_df['rating'] <= rating_range[1])
    ]
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df['review_date'].dt.date >= start_date.date()) &
            (filtered_df['review_date'].dt.date <= end_date.date())
        ]
    return filtered_df


# --- Plotting Functions ---
def plot_rating_distribution(df):
    fig = px.histogram(df, x='rating', nbins=20, title='Rating Distribution')
    fig.add_vline(x=df['rating'].mean(), line_dash="dash", line_color="red", annotation_text=f"Mean: {df['rating'].mean():.2f}")
    return fig

def plot_sentiment_pie(df):
    sentiment_counts = df['rating_category'].value_counts()
    fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index, title='Review Sentiment Distribution')
    return fig

def plot_top_apps(df):
    top_apps = df['app_name'].value_counts().head(10).sort_values(ascending=True)
    fig = px.bar(top_apps, y=top_apps.index, x=top_apps.values, orientation='h', title='Top 10 Most Reviewed Apps')
    fig.update_layout(xaxis_title="Number of Reviews", yaxis_title="App Name")
    return fig

def plot_category_ratings(df):
    fig = px.box(df, y='app_category', x='rating', title='Rating Distribution by App Category')
    return fig


# --- Main App Flow ---
def main():
    st.markdown('<h1 class="main-header">📱 Mobile App Reviews Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("An interactive tool to analyze the Multilingual Mobile App Reviews Dataset.")

    df = load_and_process_data()
    if df is None:
        return

    # --- Sidebar & Filtering ---
    app, category, rating_range, date_range = setup_sidebar(df)
    filtered_df = filter_dataframe(df, app, category, rating_range, date_range)

    if filtered_df.empty:
        st.warning("No data matches the selected filters. Please adjust your selection.")
        return

    # --- Main Page Layout ---
    st.info(f"Showing {len(filtered_df):,} reviews based on your filters.")

    # Overview Metrics
    st.markdown("## 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reviews", f"{len(filtered_df):,}")
    col2.metric("Average Rating", f"{filtered_df['rating'].mean():.2f}")
    col3.metric("Unique Apps", f"{filtered_df['app_name'].nunique():,}")
    col4.metric("Languages", f"{filtered_df['review_language'].nunique():,}")

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔬 Analysis", "💡 Insights"])

    with tab1:
        st.header("General Overview")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(plot_rating_distribution(filtered_df), use_container_width=True)
        with col2:
            st.plotly_chart(plot_sentiment_pie(filtered_df), use_container_width=True)

        if app == 'All': # Only show top apps if 'All' are selected
             st.plotly_chart(plot_top_apps(filtered_df), use_container_width=True)


    with tab2:
        st.header("Deeper Analysis")
        st.plotly_chart(plot_category_ratings(filtered_df), use_container_width=True)

        # More plots can be added here, e.g., temporal trends, correlations etc.
        st.markdown("### Average Rating by Age Group")
        age_group_ratings = filtered_df.groupby('age_group')['rating'].mean().sort_values()
        st.bar_chart(age_group_ratings)


    with tab3:
        st.header("Key Insights & Recommendations")

        # Dynamic insights based on filtered data
        avg_rating = filtered_df['rating'].mean()
        best_category = filtered_df.groupby('app_category')['rating'].mean().idxmax()
        worst_category = filtered_df.groupby('app_category')['rating'].mean().idxmin()

        st.markdown(f"""
        <div class="insight-box">
            <ul>
                <li>The average rating for the current selection is <strong>{avg_rating:.2f}</strong>.</li>
                <li>The best-performing category is <strong>{best_category}</strong>.</li>
                <li>The category with the most room for improvement is <strong>{worst_category}</strong>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎯 Recommendations")
        st.markdown("""
        1.  **Investigate Low Performers**: Dig deeper into reviews for the lowest-rated categories and apps to identify common pain points.
        2.  **Engage with Feedback**: The data shows users provide helpful feedback. Actively responding can improve user sentiment.
        3.  **Analyze by Language**: If you see significant rating differences between languages, it might point to localization issues or cultural preferences.
        """)

    # --- Footer ---
    st.markdown("---")
    footer_html = """
    <div class="footer">
        <p>
            Built by Sandeep Malviya | 
            <a href="https://www.linkedin.com/in/sandy-competent/" target="_blank">👔 LinkedIn</a> | 
            <a href="https://github.com/SandyCompetent/Kaggle-Analysis-Showcase" target="_blank">💻 GitHub</a> | 
            <a href="mailto:sandy.competent@gmail.com">📧 Email</a>
        </p>
        <p>
            <a href="https://www.kaggle.com/datasets/pratyushpuri/multilingual-mobile-app-reviews-dataset-2025/data" target="_blank">Data Source: Kaggle</a>
        </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
