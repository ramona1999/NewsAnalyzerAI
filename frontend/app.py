import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

# Base URL of FastAPI server
BASE_URL = "http://host.docker.internal:8000"


# Streamlit App
st.title("📰 News Analysis App")

# Sidebar for company input with form
with st.sidebar:
    with st.form(key="company_form"):
        company = st.text_input("Enter Company Name:")
        submit_button = st.form_submit_button("Run Full Analysis")


# Function to fetch analysis data
def fetch_full_analysis(company):
    if company:
        with st.spinner("Fetching news data..."):
            response = requests.get(f"{BASE_URL}/full-analysis/{company}")
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error {response.status_code}: {response.text}")
    return None


# Initialize analysis_data
analysis_data = None

# Process request when form is submitted
if submit_button and company:
    st.session_state["analysis_data"] = None
    analysis_data = fetch_full_analysis(company)

# Define tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "News Data",
        "Summaries",
        "Sentiment Analysis",
        "Comparative Report",
        "Audio Summary",
    ]
)

# Tab 1: News Data
with tab1:
    st.header("📰 News Articles")
    if analysis_data:
        for item in analysis_data["news_data"]:
            st.markdown(
                f"**🔹 {item['title']}**  \n📌 Source: {item['source']}  \n🔗 [Read More]({item['link']})  \n📅 Published Date: {item['published_date']}",
                unsafe_allow_html=True,
            )
            st.write("---")  # Separator for better readability
    elif company:
        st.warning("No news data available.")

# Tab 2: Expandable Summaries
with tab2:
    st.header("📌 Summaries")
    if analysis_data:
        for item in analysis_data["news_data"]:
            with st.expander(f"🔹 {item['title']}"):
                st.write(item["summary"])
    elif company:
        st.warning("No summaries available.")

# Tab 3: Sentiment Analysis
with tab3:
    st.header("📊 Sentiment Analysis")
    if analysis_data:
        df = pd.DataFrame(analysis_data["news_data"])
        if "sentiment" in df.columns:
            st.dataframe(df[["title", "link", "sentiment"]])
            sentiment_counts = df["sentiment"].value_counts()
            st.bar_chart(sentiment_counts)
        else:
            st.warning("Sentiment data not available.")
    elif company:
        st.warning("No sentiment data available.")

# Tab 4: Comparative Report
with tab4:
    st.header("📑 Comparative Report")
    if analysis_data:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("English Summary")
            st.write(analysis_data["comparative_summary"])
        with col2:
            st.subheader("Hindi Summary")
            st.write(analysis_data["translated_summary"])
    elif company:
        st.warning("No comparative report available.")

# Tab 5: Audio Summary
with tab5:
    st.header("🔊 Hindi Audio Summary")
    if analysis_data and analysis_data.get("audio_path"):
        st.audio(analysis_data["audio_path"], format="audio/mp3")
    else:
        st.warning("Audio summary not available.")
