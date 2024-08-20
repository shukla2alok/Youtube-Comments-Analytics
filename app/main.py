import streamlit as st
from app.youtube_api import get_youtube_video_details
from app.data_processing import preprocess_comments
from app.sentiment_analysis import analyze_sentiment
from app.visualization import plot_sentiment_pie_chart, plot_word_cloud

# Set up Streamlit page configuration
st.set_page_config(page_title="YouTube Comments Analytics", layout="wide")

# Define CSS for custom styling
st.markdown("""
    <style>
    .main {
        background-color: #ffffff; /* White background for the entire app */
        font-family: 'Arial', sans-serif;
    }
    .title {
        font-size: 2.5em;
        color: #333;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .section-header {
        font-size: 1.5em;
        color: #444;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 2em;
        padding: 1em;
        background-color: #f8f9fa; /* Light background for the search container */
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Shadow for better visibility */
    }
    .search-container input {
        width: 60%;
        padding: 0.8em;
        font-size: 1em;
        border-radius: 8px;
        border: 1px solid #007BFF; /* Border color to distinguish */
        background-color: #ffffff; /* White background for input field */
    }
    .search-container button {
        padding: 0.8em 1.5em;
        font-size: 1em;
        border: none;
        border-radius: 8px;
        background-color: #007BFF; /* Blue button background */
        color: white;
        cursor: pointer;
        margin-left: 1em;
    }
    .search-container button:hover {
        background-color: #0056b3;
    }
    .video-details {
        margin-top: 1em;
        padding: 1em;
        background-color: #f8f9fa; /* Light background for the details section */
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .data-frame {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 1em;
        background-color: #ffffff;
    }
    .data-frame th {
        background-color: #f7f7f7;
    }
    .comment-section {
        display: flex;
        justify-content: space-between;
        gap: 1em;
        margin-top: 1.5em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("YouTube Comments Analytics")

# Input for YouTube video URL with custom styling
with st.container():
    video_url = st.text_input("Enter YouTube video URL:", "")
    if st.button("Analyze"):
        if video_url:
            with st.spinner("Fetching and analyzing video details..."):
                title, thumbnail_url, likes_count, comments = get_youtube_video_details(video_url)
                df = preprocess_comments(comments)
                df = analyze_sentiment(df)

                # Layout for video details and thumbnail
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(thumbnail_url, width=400)
                with col2:
                    st.markdown('<div class="video-details">', unsafe_allow_html=True)
                    st.write(f"**Video Title:** {title}")
                    st.write(f"**Likes Count:** {likes_count}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # Display positive and negative comments side by side
                st.markdown('<div class="comment-section">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Positive Comments")
                    st.write(df[df['sentiment'] == 'positive'][['comment', 'polarity', 'sentiment']].sort_values(by='polarity', ascending=False).style.set_table_styles(
                        [{'selector': 'thead th', 'props': [('background-color', '#f7f7f7')]}]
                    ).set_properties(**{'border': '1px solid #ddd'}), unsafe_allow_html=True)
                with col2:
                    st.subheader("Negative Comments")
                    st.write(df[df['sentiment'] == 'negative'][['comment', 'polarity', 'sentiment']].sort_values(by='polarity', ascending=False).style.set_table_styles(
                        [{'selector': 'thead th', 'props': [('background-color', '#f7f7f7')]}]
                    ).set_properties(**{'border': '1px solid #ddd'}), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Add sentiment analysis pie chart and word cloud
                st.subheader("Sentiment Analysis")
                plot_sentiment_pie_chart(df)  # Display the pie chart

                st.subheader("Word Cloud")
                plot_word_cloud(df)  # Display the word cloud
        else:
            st.error("Please enter a valid YouTube video URL.")
    st.markdown('</div>', unsafe_allow_html=True)
