from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
placeholder = st.empty()
import time
# Function to extract Product Title


def visualize(amazon_df):
    del amazon_df['price']
    amazon_df = amazon_df.dropna()
    #Taking only ratings
    #amazon_df['reviews'].replace('', np.nan, inplace=True)
    amazon_df[['Customer_rating', 'empty']] = amazon_df['rating'].str.split(" out of 5 stars", expand=True)
    #removing extra column
    del amazon_df['empty']
    #taking relavent name of the product
    amazon_df["col"] = amazon_df["title"].str.split().str[:7].str.join(sep=" ")
    #droping extra character from title
    #amazon_df[["name", 'empty']] = amazon_df["col"].str.split(",| - | /", expand=True)
    #coverting rating into float from string
    amazon_df['CUSTOMER RATING'] = amazon_df['Customer_rating'].astype(float)
    #turning all product name into capital
    amazon_df['PRODUCT NAME'] = amazon_df['col'].apply(str.upper)
    #grouping same product and making new df
    amazon_df = amazon_df.groupby('PRODUCT NAME')['CUSTOMER RATING'].mean()
    amazon_df = amazon_df.reset_index()
    #sorting value into asending order
    amazon_df = amazon_df.sort_values(by='CUSTOMER RATING', ascending=True)
    #returning the clean dataframe
    return amazon_df

def get_url():
    Women_Fashion = st.selectbox('SELECT AN OPTION FROM PRODUCT CATEGORIES ',
                          ["Clothing", "Shoes", "Jewelry", "Watches", "Handbags",
                           "Accessories"])

    if (Women_Fashion == "Clothing"):
       # URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A1040660&ref=nav_em__nav_desktop_sa_intl_clothing_0_2_12_2"
         URL = pd.read_csv('data_store/amazon_customer_review/amazon_data1.csv')
    elif (Women_Fashion == "Shoes"):
        URL = pd.read_csv('data_store/amazon_customer_review/amazon_data2.csv')
        #URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A679337011&ref=nav_em__nav_desktop_sa_intl_shoes_0_2_12_3"
    elif (Women_Fashion == "Jewelry"):
        URL = pd.read_csv('data_store/amazon_customer_review/amazon_data3.csv')
        #URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A7192394011&ref=nav_em__nav_desktop_sa_intl_jewelry_0_2_12_4"
    elif (Women_Fashion == "Watches"):
        URL = pd.read_csv('data_store/amazon_customer_review/amazon_data4.csv')
        #URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A6358543011&ref=nav_em__nav_desktop_sa_intl_watches_0_2_12_5"
    elif (Women_Fashion == "Handbags"):
        URL = pd.read_csv('data_store/amazon_customer_review/amazon_data5.csv')
        #URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A15743631&ref=nav_em__nav_desktop_sa_intl_handbags_0_2_12_6"
    else:
        URL = pd.read_csv('data_store/amazon_customer_review/amazon_data6.csv')
       # URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A2474936011&ref=nav_em__nav_desktop_sa_intl_accessories_0_2_12_7"

    return URL


def Visualization():
    amazon_df = get_url()
    amazon_df = visualize(amazon_df)
    amazon_df = amazon_df.head(15)


    # create two columns for charts
    fig_col1, fig_col2,fig_col3 = st.columns(3)

    with fig_col1:
        # drop rows that contain the partial string "Sci"

        st.markdown("### Popular Product ")
        import plotly.express as px

        fig = px.bar(amazon_df, x='CUSTOMER RATING', y='PRODUCT NAME', orientation='h',
                     color='CUSTOMER RATING', height=600, width=1000, text_auto='.2s',color_continuous_scale='RdBu')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.write(fig)










