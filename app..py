import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# -----------------------------------------------------------------------------
# Configuration & Layout
# -----------------------------------------------------------------------------
st.set_page_config(page_title="College Student Dietary Analysis", layout="wide", page_icon="🍔")
st.title("🍔 College Student Dietary & Lifestyle Dashboard")
st.markdown("A comprehensive analysis of student eating habits, comfort foods, and health perceptions.")

# -----------------------------------------------------------------------------
# Data Loading & Cleaning
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('food_coded.csv')
    
    # Clean numerical columns that might contain text/errors
    cols_to_numeric = ['GPA', 'weight', 'calories_day']
    for col in cols_to_numeric:
        if col in df.columns:
            # Coerce errors to NaN, then drop rows where weight or GPA is missing for cleaner visualizations
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Map numerical gender to categorical for readability (assuming 1=Female, 2=Male based on standard coding, adjust if dataset differs)
    if 'Gender' in df.columns:
        df['Gender_Label'] = df['Gender'].map({1: 'Female', 2: 'Male'}).fillna('Unknown')
        
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'food_coded.csv' not found. Please ensure the file is in the same directory as this script.")
    st.stop()

# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------
st.sidebar.header("Filter Data")

# Gender Filter
selected_genders = st.sidebar.multiselect(
    "Select Gender:",
    options=df['Gender_Label'].unique(),
    default=df['Gender_Label'].unique()
)

# Grade Level Filter (if available)
if 'grade_level' in df.columns:
    selected_grades = st.sidebar.multiselect(
        "Select Grade Level:",
        options=df['grade_level'].dropna().unique(),
        default=df['grade_level'].dropna().unique()
    )
else:
    selected_grades = []

# Apply Filters
filtered_df = df[(df['Gender_Label'].isin(selected_genders))]
if 'grade_level' in df.columns and selected_grades:
    filtered_df = filtered_df[filtered_df['grade_level'].isin(selected_grades)]

# -----------------------------------------------------------------------------
# Top Level KPIs
# -----------------------------------------------------------------------------
st.markdown("### 📊 High-Level Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

avg_gpa = filtered_df['GPA'].mean()
avg_weight = filtered_df['weight'].mean()
most_common_sports = filtered_df['sports'].value_counts().idxmax() if 'sports' in filtered_df.columns else "N/A"
total_responses = len(filtered_df)

kpi1.metric("Total Respondents", f"{total_responses}")
kpi2.metric("Average GPA", f"{avg_gpa:.2f}" if pd.notna(avg_gpa) else "N/A")
kpi3.metric("Average Weight (lbs)", f"{avg_weight:.1f}" if pd.notna(avg_weight) else "N/A")
kpi4.metric("Sports Participation (1=Yes)", f"{most_common_sports}")

st.divider()

# -----------------------------------------------------------------------------
# Main Dashboard Sections
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Demographics & Health", "Dietary Preferences", "Comfort Food Psychology"])

# --- TAB 1: Demographics & Health ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gender Distribution")
        fig_gender = px.pie(filtered_df, names='Gender_Label', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_gender, use_container_width=True)
        
    with col2:
        st.subheader("Weight Distribution by Gender")
        fig_weight = px.box(filtered_df, x='Gender_Label', y='weight', color='Gender_Label',
                            labels={'Gender_Label': 'Gender', 'weight': 'Weight (lbs)'})
        st.plotly_chart(fig_weight, use_container_width=True)

    st.subheader("GPA vs. Perception of Healthy Feeling")
    if 'healthy_feeling' in filtered_df.columns:
        fig_gpa_health = px.scatter(filtered_df, x='healthy_feeling', y='GPA', color='Gender_Label',
                                    hover_data=['comfort_food'], trendline="ols",
                                    labels={'healthy_feeling': 'Healthy Feeling Score (1-10)'})
        st.plotly_chart(fig_gpa_health, use_container_width=True)

# --- TAB 2: Dietary Preferences ---
with tab2:
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Likelihood to Eat Out")
        if 'eating_out' in filtered_df.columns:
            fig_out = px.histogram(filtered_df, x='eating_out', nbins=10, 
                                   labels={'eating_out': 'Frequency of Eating Out (1-5)'})
            st.plotly_chart(fig_out, use_container_width=True)

    with col4:
        st.subheader("Estimated Daily Calories by Gender")
        if 'calories_day' in filtered_df.columns:
            fig_cal = px.box(filtered_df, x='Gender_Label', y='calories_day', points="all")
            st.plotly_chart(fig_cal, use_container_width=True)
            
    st.subheader("Cuisine Preferences (1 to 5 Scale)")
    cuisines = ['ethnic_food', 'greek_food', 'indian_food', 'italian_food', 'persian_food', 'thai_food']
    available_cuisines = [c for c in cuisines if c in filtered_df.columns]
    
    if available_cuisines:
        cuisine_means = filtered_df[available_cuisines].mean().reset_index()
        cuisine_means.columns = ['Cuisine', 'Average Rating']
        fig_cuisine = px.bar(cuisine_means, x='Cuisine', y='Average Rating', color='Cuisine',
                             title="Average Rating of Different Cuisines")
        st.plotly_chart(fig_cuisine, use_container_width=True)

# --- TAB 3: Comfort Food Psychology ---
with tab3:
    st.subheader("What do students eat for comfort?")
    st.markdown("A visual representation of the most frequently mentioned comfort foods.")
    
    if 'comfort_food' in filtered_df.columns:
        # Combine all text into one large string, dropping NaNs
        text = " ".join(review for review in filtered_df['comfort_food'].dropna().astype(str))
        
        if text.strip() != "":
            wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text)
            
            fig_wc, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig_wc)
        else:
            st.info("Not enough data to generate comfort food word cloud.")
            
    st.subheader("Reasons for eating comfort food")
    if 'comfort_food_reasons' in filtered_df.columns:
        # Display a sample of raw responses for qualitative context
        st.dataframe(filtered_df[['Gender_Label', 'comfort_food', 'comfort_food_reasons']].dropna().head(15), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Dashboard developed for high-level exploratory data analysis of the food_coded dataset.*")
