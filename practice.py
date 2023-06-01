from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
placeholder = st.empty()


# Function to extract Product Title

def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})

        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""
    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price


# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"

    return available

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
    amazon_df['Customer_rating'] = amazon_df['Customer_rating'].astype(float)
    #turning all product name into capital
    amazon_df['name'] = amazon_df['col'].apply(str.upper)
    #grouping same product and making new df
    amazon_df = amazon_df.groupby('name')['Customer_rating'].mean()
    amazon_df = amazon_df.reset_index()
    #sorting value into asending order
    amazon_df = amazon_df.sort_values(by='Customer_rating', ascending=True)
    #returning the clean dataframe
    return amazon_df

def get_url():
    Women_Fashion = st.selectbox('SELECT AN OPTION FROM PRODUCT CATEGORIES ',
                          ["Clothing", "Shoes", "Jewelry", "Watches", "Handbags",
                           "Accessories"])

    if (Women_Fashion == "Clothing"):
         URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A1040660&ref=nav_em__nav_desktop_sa_intl_clothing_0_2_12_2"
         #URL = pd.read_csv('amazon_data1.csv')
    elif (Women_Fashion == "Shoes"):
        #URL = pd.read_csv('amazon_data2.csv')
        URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A679337011&ref=nav_em__nav_desktop_sa_intl_shoes_0_2_12_3"
    elif (Women_Fashion == "Jewelry"):
        #URL = pd.read_csv('amazon_data3.csv')
        URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A7192394011&ref=nav_em__nav_desktop_sa_intl_jewelry_0_2_12_4"
    elif (Women_Fashion == "Watches"):
        #URL = pd.read_csv('amazon_data4.csv')
        URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A6358543011&ref=nav_em__nav_desktop_sa_intl_watches_0_2_12_5"
    elif (Women_Fashion == "Handbags"):
        #URL = pd.read_csv('amazon_data5.csv')
        URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A15743631&ref=nav_em__nav_desktop_sa_intl_handbags_0_2_12_6"
    else:
        #URL = pd.read_csv('amazon_data6.csv')
        URL = "https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A2474936011&ref=nav_em__nav_desktop_sa_intl_accessories_0_2_12_7"

    return URL

# add your user agent
HEADERS = ({'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'})

# The webpage URL
URL = get_url()

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)

# Soup Object containing all data
soup = BeautifulSoup(webpage.content, "html.parser")

# Fetch links as List of Tag Objects
links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})

# Store the links
links_list = []

# Loop for extracting links from Tag Objects
for link in links:
    links_list.append(link.get('href'))

d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}

# Loop for extracting product details from each link
for link in links_list:
    new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    # Function calls to display all necessary product information

    d['title'].append(get_title(new_soup))
    d['price'].append(get_price(new_soup))
    d['rating'].append(get_rating(new_soup))
    d['reviews'].append(get_review_count(new_soup))
    d['availability'].append(get_availability(new_soup))

amazon_df = pd.DataFrame.from_dict(d)
amazon_df['title'].replace('', np.nan, inplace=True)
amazon_df = amazon_df.dropna(subset=['title'])
#amazon_df.to_csv("amazon_data.csv", header=True, index=False)

#amazon_df = pd.read_csv('amazon_data.csv')'''

amazon_df = visualize(amazon_df)
avg_rating = np.mean(amazon_df["Customer_rating"])


# create two columns for charts
fig_col1, fig_col2,fig_col3 = st.columns(3)

with fig_col1:
    # drop rows that contain the partial string "Sci"

    st.markdown("### Popular Product ")
    import plotly.express as px

    fig = px.bar(amazon_df, x='Customer_rating', y='name', orientation='h',
                 color='Customer_rating', height=1000, width=1500)
    st.write(fig)










