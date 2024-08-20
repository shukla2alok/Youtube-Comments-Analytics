from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def plot_word_cloud(df):
    # Combine all comments into a single string
    comment_words = ' '.join(df['comment'].tolist())
    
    # Generate a word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comment_words)
    
    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # No axes for a cleaner look
    st.pyplot(plt.gcf())  # Display in Streamlit

def plot_sentiment_pie_chart(df):
    sentiment_counts = df['sentiment'].value_counts()
    labels = sentiment_counts.index
    sizes = sentiment_counts.values
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    # Make the pie chart smaller by adjusting figsize
    plt.figure(figsize=(3, 3))  # Smaller figsize for a smaller chart
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(plt.gcf())  # Display the pie chart in Streamlit

def plot_polarity_distribution(df):
    df['polarity'].hist(bins=20)
    plt.title('Polarity Distribution')
    plt.xlabel('Polarity')
    plt.ylabel('Frequency')
    st.pyplot()
# Example of time series sentiment trend plotting
import matplotlib.pyplot as plt

def plot_sentiment_trends(df):
    df['date'] = pd.to_datetime(df['date'])
    sentiment_trends = df.groupby(df['date'].dt.to_period('M'))['sentiment'].value_counts().unstack().fillna(0)
    sentiment_trends.plot(kind='line', marker='o')
    plt.title('Sentiment Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Comments')
    plt.legend(title='Sentiment')
    st.pyplot()


