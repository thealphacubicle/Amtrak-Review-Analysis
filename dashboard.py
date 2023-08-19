import streamlit as st
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Set page title
st.title("Amtrak Reviews Dashboard")

# Sub header
st.subheader("Data Sample")

# Show DataFrame
df = pd.read_csv("/Users/srihariraman/PycharmProjects/AmtrakTwitterAnalysis/Amtrak-Twitter-Analysis/reviews_cleaned.csv")
df.drop(["Unnamed: 0"], axis=1, inplace=True)
st.data_editor(df.head(10), hide_index=True, use_container_width=True)

# Sidebar for user input
st.sidebar.header("Development:")


st.sidebar.write('This dashboard and supplemental analysis was made by Srihari Raman! '
                 'The full analysis document can be found '
                 '[here](https://github.com/thealphacubicle/Amtrak-Review-Analysis)!')

st.sidebar.header('Contact the Developer:')
st.sidebar.write('Github Link: [@thealphacubicle](https://github.com/thealphacubicle)')
st.sidebar.write('Email: srihariraman9@gmail.com')

# Sentiment Analysis using TextBlob
if text_input:
    st.header("Sentiment Analysis using TextBlob")
    blob = TextBlob(text_input)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        sentiment_label = "Positive"
    elif sentiment_score < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    st.write(f"Sentiment Score: {sentiment_score:.2f}")
    st.write(f"Sentiment Label: {sentiment_label}")

# Sentiment Analysis using VADER
if text_input:
    st.header("Sentiment Analysis using VADER")
    analyzer = SentimentIntensityAnalyzer()
    vader_scores = analyzer.polarity_scores(text_input)

    st.write(f"Positive Score: {vader_scores['pos']:.2f}")
    st.write(f"Neutral Score: {vader_scores['neu']:.2f}")
    st.write(f"Negative Score: {vader_scores['neg']:.2f}")
    st.write(f"Compound Score: {vader_scores['compound']:.2f}")
