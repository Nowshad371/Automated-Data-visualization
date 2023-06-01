import pandas as pd
import csv
import time
from pathlib import Path
from tqdm import tqdm
import streamlit as st
placeholder = st.empty()
import plotly.express as px
import numpy as np
'''print('data1')
data1 = pd.read_csv('inputMovies.csv')
print(data1.shape)
print(data1)
print('\ndata2')
data2 = pd.read_csv('/Users/mdnowshadulalam/Desktop/FYP work/inputMovies.csv')

vertical_concat = pd.concat([data1, data2], axis=0)

# Using DataFrame.drop() method.
#data1=data1.drop(data1.columns[1], axis=1)

vertical_concat.to_csv('inputMovies.csv',index=False)

print('\nnew data\n')
data = pd.read_csv('inputMovies.csv')
print(data)'''
Main_data = pd.read_csv('inputMovies1.csv')
a = 'inputMovies'
flag = True
i = 2
while(flag == True):
    b = str(i)
    c = a+b+'.csv'
    path = Path(c)
    if (path.is_file() == True):
        data = pd.read_csv(c)
        Main_data = pd.concat([Main_data, data], axis=0)
        Main_data.to_csv('inputMovies1.csv', index=False)
        Main_data = pd.read_csv('inputMovies1.csv')
        Main_data_reset =  Main_data.groupby('title')['rating'].mean()
        Main_data_reset  = Main_data_reset.reset_index()
        Total_avg_vote_count = np.mean(Main_data["rating"])
        avg_vote_count = np.mean(data["rating"])
        with placeholder.container():
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label="New Ratings Average ⏳",
                value=round(avg_vote_count),
                delta=round(avg_vote_count) - 10,
            )
            kpi2.metric(
                label="Total Ratings Average ⏳",
                value=round(Total_avg_vote_count),
                delta=round(Total_avg_vote_count) - 10,
            )


            col1, col2, col3,col4,col5,col6,col7 = st.columns(7)
            '''with col1:
                st.markdown("### Chart")
                fig2 = px.histogram(data_frame=data, x="rating")
                st.write(fig2)'''
            with col1:
                with st.container():
                    st.markdown("### Table")
                    st.dataframe(data.style.highlight_max(axis=0))
                with st.container():
                    st.markdown("### Table")
                    st.dataframe(Main_data)
            with col2:
                st.markdown("### Chart")
                fig = px.line(data, x="title", y="rating", title='rating of users')
                st.write(fig)
                with st.container():
                    st.markdown("### Chart")
                    fig = px.line(Main_data_reset, x="title", y="rating", title='rating of users')
                    st.write(fig)


            time.sleep(1)
    else:

        st.balloons()
        '''with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success('Done!')'''
        '''loop= tqdm(total= 1000, position = 0, leave = False)
        for k in range(1000):
            loop.set_description("Loading...".format(k))
            loop.update(1)
        loop.close()
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1, text=progress_text)'''
        '''with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success('Done!')'''


        flag = False
    i = i+1




