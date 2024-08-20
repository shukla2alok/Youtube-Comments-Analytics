from textblob import TextBlob

def analyze_sentiment(df):
    df['polarity'] = df['comment'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment'] = df['polarity'].apply(lambda p: 'positive' if p > 0 else 'negative' if p < 0 else 'neutral')
    return df
