import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
def find_season(month, hemisphere):
    if hemisphere == 'Southern':
        season_month_south = {
            12: 'Summer', 1: 'Summer', 2: 'Summer',
            3: 'Autumn', 4: 'Autumn', 5: 'Autumn',
            6: 'Winter', 7: 'Winter', 8: 'Winter',
            9: 'Spring', 10: 'Spring', 11: 'Spring'}
        return season_month_south.get(month)

    elif hemisphere == 'Northern':
        season_month_north = {
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Autumn', 10: 'Autumn', 11: 'Autumn'}
        return season_month_north.get(month)
    else:
        print('Invalid selection. Please select a hemisphere and try again')


def Visualization():
    df = pd.read_csv('data_store/holidays/SalesForCourse_quizz_table.csv')

    df = df.drop('Column1', axis=1)
    df.dropna(subset=['Date'], inplace=True)
    df[["month", "date", "year"]] = df['Date'].str.split("/", expand=True)
    df["month"] = df['month'].astype(int)
    demanded_product_up = df.groupby(['month','Product Category','Sub Category'])['Quantity','Cost','Revenue'].apply(pd.Series.mean)
    demanded_product_up = demanded_product_up.reset_index()
    demanded_product_up = demanded_product_up.sort_values(['month'], ascending=[True])

    season_list = []
    hemisphere = st.radio(
        "Select Region Hemisphere",
        ('Southern', 'Northern'))

    #hemisphere = 'Southern'
    for month in demanded_product_up['month']:
        season = find_season(month, hemisphere)
        season_list.append(season)

    demanded_product_up['Season'] = season_list
    list_season = []

    for i in range(len(demanded_product_up['Season'].value_counts())):
        list_season.append(demanded_product_up['Season'].value_counts().index[i])

    option = st.selectbox(
        'Select Option ',list_season
        )

    st.write('You selected:', option)


    filter = demanded_product_up[demanded_product_up['Season'] == option]
    filter = filter.groupby(['Product Category','Sub Category'])['Quantity','Cost','Revenue'].apply(pd.Series.mean)
    filter = filter.reset_index()

    filter = filter.sort_values(['Revenue'], ascending=[False])
    filter['ratio_cost_revenue'] = ((filter['Revenue'] - filter['Cost'])/filter['Cost'])*100
    filter['revenue_percentage'] = (filter['Revenue']/filter['Revenue'].sum())*100



    col1,col2,col3,col4 = st.columns(4)

    with col1:
        with st.container():
            fig = px.bar(filter, x= 'Sub Category', y= 'Revenue',text_auto='.2s',color='Revenue',
                         labels={'Revenue':'Revenue in Each Product'},color_continuous_scale='RdBu')
            fig.update_layout(width=650, height=600, bargap=0.10)

            st.write(fig)
        with st.container():
            fig = px.line(filter, x='Sub Category', y=['ratio_cost_revenue', 'revenue_percentage'],
                          labels={'value': 'Ratio and Percentage of Cost and Revenue'})
            fig.update_layout(width=650, height=600, bargap=0.10)
            st.write(fig)

    with col4:
        fig = px.line(x=filter['Sub Category'], y=filter['Revenue'], color=px.Constant("This year"),
                      labels=dict(x="Sub Category", y="Amount", color="Time Period"))
        fig.add_bar(x=filter['Sub Category'], y=filter['Revenue'], name="Trends")
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig)





