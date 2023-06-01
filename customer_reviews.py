import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from textblob import Word
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st




def get_Customer_Reviews():
    url = "https://www.amazon.in/New-Apple-iPhone-Mini-128GB/product-reviews/B08L5VN68Y/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    code = requests.get(url)
    soup = BeautifulSoup(code.content, 'html.parser')
    names = soup.select('span.a-profile-name')
    titles = soup.select('a.review-title span')
    dates = soup.select('span.review-date')
    stars = soup.select('i.review-rating span.a-icon-alt')
    reviews = soup.select('span.review-text-content span')

    ##
    cust_name = []
    rev_date = []
    ratings = []
    rev_title = []
    rev_content = []
    for i in range(len(reviews)):
        cust_name.append(names[i].get_text())
        rev_date.append(dates[i].get_text().replace("Reviewed in India on ", ""))
        ratings.append(stars[i].get_text())
        rev_title.append(titles[i].get_text())
        rev_content.append(reviews[i].get_text().strip("\n "))

    df = pd.DataFrame()
    df['Customer Name'] = cust_name
    df['Date'] = rev_date
    df['Ratings'] = ratings
    df['Review Title'] = rev_title
    df['Reviews'] = rev_content
    df.to_csv("amazon_reviews.csv")
    return df


#df = get_Customer_Reviews()

#Saving into csv file
def Visualization():
    from nltk.corpus import stopwords
    df = pd.read_csv('data_store/customer_opinion/amazon.csv')
    # Calculate word count
    df['word_count'] = df['Reviews'].apply(lambda x: len(str(x).split(" ")))

    #Character Count – total number of characters in each review
    df['char_count'] = df['Reviews'].str.len()

    #Average word length – the average length of words used
    def avg_word(review):
      words = review.split()
      return (sum(len(word) for word in words) / len(words))

    # Calculate average words
    df['avg_word'] = df['Reviews'].apply(lambda x: avg_word(x))

    #Stopword Count – total number of words which are considered stop words
    stop_words = stopwords.words('english')
    df['stopword_coun'] = df['Reviews'].apply(lambda x: len([x for x in x.split() if x in stop_words]))

    # Lower case all words
    df['review_lower'] = df['Reviews'].apply(lambda x: " ".join(x.lower() for x in x.split()))

    # Remove Punctuation
    df['review_nopunc'] = df['review_lower'].str.replace('[^\w\s]', '')

    # Import stopwords
    stop_words = stopwords.words('english')

    # Remove Stopwords
    df['review_nopunc_nostop'] = df['review_nopunc'].apply(lambda x: " ".join(x for x in x.split() if x not in stop_words))

    # CLEANING THE DATA SET
    other_stopwords = ['1','2','3','4','5','6','7','8','9','10','im','se','also','12']
    df['review_nopunc_nostop_nocommon'] = df['review_nopunc_nostop'].apply(lambda x: "".join(" ".join(x for x in x.split() if x not in other_stopwords)))


    # Lemmatize final review format
    df['cleaned_review'] = df['review_nopunc_nostop_nocommon']\
    .apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    #The polarity metric refers to the degree to which the text analysed is positive or negative,
    # between a range of -1 to 1. A score of 1 means highly positive whereas -1 is considered well and truly negative.

    # Calculate polarity
    df['polarity'] = df['cleaned_review'].apply(lambda x: TextBlob(x).sentiment[0])




    #We can also analyse subjectivity, this is the degree to which the text analysed relates
    # to personal emotion or factual information between a scale of 0 to 1.
    # With scores closer to one indicating a higher level of subjectivity and being based mostly on opinion.

    # Calculate subjectivity
    df['subjectivity'] = df['cleaned_review'].apply(lambda x: TextBlob(x).sentiment[1])











    #to disable deprecation.showPyplotGlobalUse
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.markdown(
        "<h5 style='text-align: center; color: #FAF9F6;'>Most repeated words</h5>",
        unsafe_allow_html=True)


    text = " ".join(i for i in df.cleaned_review)
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords,  background_color ='white',
                    min_font_size = 10).generate(text)
    fig, ax = plt.subplots(figsize = (12, 8))
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()
    st.pyplot()



    def highlight_polarity(p):
        return ['background-color: green']*len(p) if p.polarity >0.1 else ['background-color: red']*len(p) if p.polarity <0.01 else ['background-color: yellow']*len(p)



    def highlight_Subjectivity (s):
        return ['background-color: green']*len(s) if s.subjectivity <0.4 else ['background-color: red']*len(s) if s.subjectivity >0.6 else ['background-color: yellow']*len(s)


    st.markdown(
        "<h5 style='text-align: center; color: #FAF9F6;'>Polarity Table</h5>",
        unsafe_allow_html=True)

    st.dataframe(df.style.apply(highlight_polarity, axis=1))

    st.markdown(
        "<h5 style='text-align: center; color: #FAF9F6;'>Subjectivity Table</h5>",
        unsafe_allow_html=True)
    st.dataframe(df.style.apply(highlight_Subjectivity, axis=1))






















