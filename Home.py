import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import hydralit_components as hc
import streamlit.components.v1 as html
import requests
#import Homepage
import base64
import pandas as pd
import numpy as np
import re
import time
import math
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
import streamlit as st
import plotly.express as px
from pathlib import Path
from tqdm import tqdm
from nltk.corpus import stopwords
placeholder = st.empty()


import Deshboard
import Users_items
import website_browsing
import seasonal_items
import filterSpecificCustomer
import holidays_product
import scraping
import customer_reviews
import Potential_customer
import filterTimeFrame
menu_data = [
    {'icon': "fas fa-tachometer-alt", 'label': "Dashboard"},
    {'label': "Users & Products"},
    {'label': "Seasonal Items"},
    {'label': "Online Users Info"},
    {'label': "Holidays Product"},
    {'label': "Current Top Rated Product"},
    {'label': "Users Opinion"},
    {'label': "Filter Age"},
    {'label': "Filter Time duration"},
    {'label': "Storing Data"},
    {'label': "Predicted Value"}# no tooltip message
]




over_theme = {'txc_inactive': '#FFFFFF'}
with st.sidebar:
    st.header('REAL TIME DATA (NOWSHAD)')
    menu_id = hc.nav_bar(menu_definition=menu_data, key='sidetbar',
                              override_theme=over_theme, first_select=6)




if(menu_id == "Dashboard"):
    Deshboard.Visualization()
if(menu_id == "Users & Products"):
    Users_items.Visualization()
if(menu_id == "Online Users Info"):
    website_browsing.Visualization()
if(menu_id == "Seasonal Items"):
    seasonal_items.Visualization()
if(menu_id == "Filter Age"):
    filterSpecificCustomer.Visualization()
if(menu_id == "Holidays Product"):
    holidays_product.Visualization()
if(menu_id == "Current Top Rated Product"):
    scraping.Visualization()
if(menu_id == "Users Opinion"):
    customer_reviews.Visualization()
if (menu_id == "Predicted Value"):
    Potential_customer.Visualization()
if (menu_id == "Filter Time duration"):
    filterTimeFrame.Visualization()


