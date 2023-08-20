import streamlit as st
import pandas as pd
import plotly.express as px
from annotated_text import annotated_text

# Set page title
st.title("Amtrak Reviews Dashboard 🚆")

# Show DataFrame
df = pd.read_csv("https://raw.githubusercontent.com/thealphacubicle/Amtrak-Review-Analysis/main/reviews_cleaned.csv")
df.drop(["Unnamed: 0"], axis=1, inplace=True)

# Sidebar for user input
st.sidebar.header("Development:")


st.sidebar.write('This dashboard and supplemental analysis was made by Srihari Raman! ')
st.sidebar.write('The full analysis document can be found '
                 '[here](https://github.com/thealphacubicle/Amtrak-Review-Analysis)!')

st.sidebar.header('Contact the Developer:')
st.sidebar.write('Github: [@thealphacubicle](https://github.com/thealphacubicle)')
st.sidebar.write('LinkedIn: [@srihari-r](https://www.linkedin.com/in/srihari-r-006034176/)')
st.sidebar.write('Email: srihariraman9@gmail.com')

# Create tabs
t1, t2, t3 = st.tabs(['Data', 'Visualizations', 'Analysis'])

# Tab 1: Data
with t1:
    with st.container():
        # Data about df
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Number of Reviews:", f"{df.shape[0]}")
        col2.metric("Number of Features", f"{df.shape[1]}")
        col3.metric("Average Sentiment Score", round(df['review_polarity'].mean(),3),
                    f"{round(0+df['review_polarity'].mean(), 4) * 100}%")
        col4.metric("Average Subjectivity Score", round(df['review_subjectivity'].mean(), 3),
                    f"{round(0 + df['review_subjectivity'].mean(), 4) * 100}%")

        # Show df sample
        st.subheader("Data Sample")
        st.data_editor(df.iloc[345:355], hide_index=True, use_container_width=True)

# Tab 2: Visualizations
with t2:
    # CONTAINER 1
    with st.container():
        st.subheader("Website Class Distribution")

        # Plot
        st.plotly_chart(px.bar(df, x="Website", color="Website"))

        # Expander with analysis
        with st.expander(label="See in-depth explanation:"):
            st.write("Post-processing, we can see that Amtrak reviews are not equally balanced in this dataset, "
                     "with there being class imbalance in the number of reviews originating from each website. "
                     "TrustPilot and ComplaintsBoard make up a majority of the reviews, hence meaning that polarity and "
                     "sentiment metrics calculated are likely to be more biased towards these reviews.")
    st.divider()

    # CONTAINER 2
    with st.container():
        st.subheader("Sentiment Score Distribution by Website")

        # Plot
        st.plotly_chart(px.box(df, x="Website", y="review_polarity", color="Website", points="outliers"))

        # Expander with analysis
        with st.expander(label="See in-depth explanation:"):
            st.write("Analyzing by website, we see that 3 of 4 analyzed websites are skewed more negatively, with the "
                     "distribution of average review sentiment scores for the 3 websites being centered more around "
                     "-1.0. However, the only website to have more positive reviews is Yelp.com. This could pose an "
                     "interesting question as to whether or not Yelp reviews are actually made by consumers who've "
                     "experienced journeys on Amtrak.")
    st.divider()

    with st.container():
        st.subheader("Overall Subjectivity Distribution")
        st.caption('*Outliers are shown as data points*')

        # Plot
        st.plotly_chart(px.box(df, y="review_subjectivity", points="outliers"))

        st.subheader("Overall Sentiment Distribution")
        # Plot
        st.plotly_chart(px.box(df, y="review_polarity", points="outliers"))


        # Expander with analysis
        with st.expander(label="See in-depth explanation:"):
            st.write("Overall, Amtrak's customer reviews are either skewed more negatively or positively, with the "
                     "overall outlook being more negative than positive. The overall sentiment score is centered more "
                     "around -1.0 and 0.7, thus meaning that customers either had a great experience or a very negative "
                     "experience. In contrast, the overall subjectivity score distribution is more unimodal, "
                     "centered around approximately 0.5. This means that, overall, customer reviews were balanced in "
                     "terms of opinionated or fact-based.")
    st.divider()
    # CONTAINER 3
    with st.container():
        st.subheader("Subjectivity Distribution by Website")
        st.caption('*Outliers are shown as data points*')

        # Plot
        st.plotly_chart(px.box(df, x="Website", y="review_subjectivity", color="Website"))

        # Expander with analysis
        with st.expander(label="See in-depth explanation:"):
            st.write("Similarly, the subjectivity scores of the websites are relatively similar in that their "
                     "distributions are approximately unimodal and centered around 0.5. However, SiteJabber seems to "
                     "lean more towards fact-based evidence. Through descriptive analysis (see tables above), we can "
                     "see than 75% of review sentiment scores being centered between 0.52-0.63. Thus, we can see that "
                     "of the four websites analyzed in this project, most of the reviews are neutral in terms of being "
                     "opinionated and fact-based.")
    st.divider()

# Tab 3: Analysis
with t3:
    with st.container():
        st.subheader("Common Topics of Concern:")
        annotated_text(("Time", "Scheduling"), ("Trip", "Overall Experience"), ("People", "Customer Service"),
                       ("Hour", "Scheduling"),("Food", "Customer Service"))
        st.subheader("Recommendations")
        st.write("In the analysis, I also wanted to look at which words most frequently occured in the reviews. On an "
                 "aggregated level, the most apparent words were **time**, **ticket**, **trip**, and **hour**. "
                 "This means that most of the reviews (by making a loose-level guess) were concerned either about train "
                 "timings or trip/ticketing experiences. Because the overall sentiment towards Amtrak is negative, it is "
                 "likely that these topics are what caused a slim majority of customers dissatisfaction.")
        st.write("When analyzing website-specific review content, Yelp reviews were more centered around the Acela "
                 "exeperience. A lot of reviews seemed to be concerned with the Boston train, with **time** and "
                 "**ticket**, and **seat** being some of the important keywords. Because Yelp was a much more "
                 "positively-skewed website, it is likely that Amtrak should focus on their strengths with the Acela "
                 "Express and try and cross-implement them with their other services.")
        st.write("Trustpilot was more concerned around the **time**, **trip**, **food**, and **people**. Because it "
                 "was one of the negatively-skewed review sites, Amtrak should take a look at things like train timing, "
                 "overall trip experiences, food quality/taste, and the staff that work on these trains. By improving "
                 "these segments, Amtrak is likely to acquire more customer satisfaction!")
        st.write("Complaintsboard and Sitejabber were similar in that the overall topics concerned around timing and "
                 "service on the trains.  Keywords in these reviews included **ticket**, **time**, **customer**, and "
                 "**experience**. This likely means that customers posting on this site had an issue with train "
                 "timing/scheduling and customer service. Amtrak should analyze the customer service experience they "
                 "are providing—customer service representatives, train staff, etc.—and should focus on improving those "
                 "segments as well!")
