import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import plotly.graph_objects as go


def Visualization():
    df = pd.read_csv('data_store/customer_browsing/SalesForCourse_quizz_table.csv')

    df.dropna(subset=['Country'], inplace=True)
    df[["month_number", "day", "year"]] = df['Date'].str.split("/", expand=True)
    df1 = pd.DataFrame()
    df1['states'] = df['State'].value_counts().index
    df1['Users'] = df['State'].value_counts().values
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    df1['Lat'] = ''
    df1['Long'] = ''

    option = st.radio(
        "CLICK OPTION THAT YOU WANT TO KNOW",
        ('NONE','OVERALL COST VS REVENUE FROM EACH COUNTRY', 'OVERALL USERS FROM EACH STATES'))


    if option == 'NONE':
        st.write('CURRENTLY, USER SELECTED NONE')
    elif option == 'OVERALL COST VS REVENUE FROM EACH COUNTRY':
        df_view = df.sort_values(['month_number'], ascending=[True])
        fig = px.scatter(df_view, x="Cost",  y="Revenue",size="Revenue", animation_frame="Month", animation_group="State",
                        color="State", hover_name="State", facet_col="Country",
                        title="OVERALL COST VS REVENUE FROM EACH COUNTRY",
                        log_x=True, size_max=45)
        fig.update_layout(width=1000, height=700, bargap=0.10)
        #fig.update_traces(textposition="bottom right")
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
        #st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.write(fig)

    else:
        for i in range(len(df1)):
            location = geolocator.geocode(df1['states'].iloc[i])
            df1['Lat'][i] = location.latitude
            df1['Long'][i] = location.longitude

        color_scale = [(0, 'orange'), (1, 'red')]
        st.markdown("### OVERALL USERS FROM EACH LOCATIONS")
        fig = px.scatter_mapbox(df1,
                                lat="Lat",
                                lon="Long",
                                hover_name="states",
                                hover_data=["states", "Users"],
                                color="Users",
                                color_continuous_scale=color_scale,
                                size="Users", color_discrete_sequence=["fuchsia"], zoom=3, height=400)

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_traces(textposition="bottom right")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        #st.write(fig)

    df['age_group'] = ""

    for index in range(len(df)):
      if(df['Customer Age'].iloc[index] >= 17 and df['Customer Age'].iloc[index] < 20):
        df['age_group'][index] = '17-19'
      elif(df['Customer Age'].iloc[index] >= 20 and df['Customer Age'].iloc[index] <= 25):
        df['age_group'][index] = '20 - 25'
      elif(df['Customer Age'].iloc[index] >= 26 and df['Customer Age'].iloc[index] <= 30):
        df['age_group'][index] = '26 - 30'
      elif(df['Customer Age'].iloc[index] >= 31 and df['Customer Age'].iloc[index] <= 35):
        df['age_group'][index] = '31 - 35'
      elif(df['Customer Age'].iloc[index] >= 36 and df['Customer Age'].iloc[index] <= 40):
        df['age_group'][index] = '36 - 40'
      elif(df['Customer Age'].iloc[index] >= 41 and df['Customer Age'].iloc[index] <= 45):
        df['age_group'][index] = '41 - 45'
      elif(df['Customer Age'].iloc[index] >= 46 and df['Customer Age'].iloc[index] <= 50):
        df['age_group'][index] = '46 - 50'
      elif(df['Customer Age'].iloc[index] >= 51 and df['Customer Age'].iloc[index] <= 60):
        df['age_group'][index] = '51 - 60'
      else:
        df['age_group'][index] = 'over 60'



    data_group = df.groupby(['age_group','Product Category','Sub Category'])['Cost','Revenue'].apply(pd.Series.mean)
    data_group  = data_group.reset_index()
    new_data_group = data_group.sort_values(['age_group','Revenue'], ascending=[True, False])

    new_data_group['Cost'] = new_data_group['Cost'].apply(lambda x:round(x,2))
    new_data_group['Revenue'] = new_data_group['Revenue'].apply(lambda x:round(x,2))

    option = st.selectbox(
        'Select age group',
        ('17-19', '20 - 25', '26 - 30','31 - 35','36 - 40','41 - 45','46 - 50','51 - 60','over 60'))

    st.write('You selected:', option)


    filter_age = new_data_group[new_data_group['age_group'] == option]
    filter_bike = filter_age[filter_age['Product Category'] == 'Bikes']
    filter_Clothing = filter_age[filter_age['Product Category'] == 'Clothing']
    filter_Accessories = filter_age[filter_age['Product Category'] == 'Accessories']


    st.markdown(
        "<h5 style='text-align: center; color: green;'>REVENUE FROM EACH PRODUCT CATEGORY AND (SUB-CATEGORIES)</h5>",
        unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fig = px.sunburst(filter_age, path=['age_group', 'Product Category','Revenue'], values='Revenue',
                          color='Revenue', hover_data=['Cost'],color_continuous_scale='RdBu')
        fig.update_layout(width=630, height=600, bargap=0.10)
        st.write(fig)

    with col4:
        fig = px.bar(filter_age, x='Sub Category', y='Revenue',
                       hover_data=['Cost'], color='Revenue',
                       labels={'Revenue': 'Revenue'},color_continuous_scale='RdBu')

        fig.update_layout(width=630, height=600, bargap=0.10)
        st.write(fig)



    st.markdown(
        "<h5 style='text-align: center; color: green;'>REVENUE FROM PRODUCT CATEGORY (BIKE) AND ITS (SUB-CATEGORIES)</h5>",
        unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fig1 = px.sunburst(filter_bike, path=['Product Category','Sub Category', 'Revenue'], values='Revenue',
                          color='Revenue', hover_data=['Cost'],color_continuous_scale='RdBu')
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig1)


    with col4:
        fig1 = px.bar(filter_bike, x='Sub Category', y='Revenue',
                       hover_data=['Cost'], color='Revenue',
                       labels={'Revenue': 'Revenue'},color_continuous_scale='RdBu')
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig1)




    st.markdown(
        "<h5 style='text-align: center; color: green;'>REVENUE FROM PRODUCT CATEGORY (CLOTHING) AND ITS (SUB-CATEGORIES)</h5>",
        unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fig2 = px.sunburst(filter_Clothing,path=['Product Category','Sub Category', 'Revenue'], values='Revenue',
                          color='Revenue', hover_data=['Cost'],color_continuous_scale='RdBu')
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig2)


    with col4:
        fig2 = px.bar(filter_Clothing, x='Sub Category', y='Revenue',
                       hover_data=['Cost'], color='Revenue',
                       labels={'Revenue': 'Revenue'},color_continuous_scale='RdBu')
        fig2.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig2)



    st.markdown(
        "<h5 style='text-align: center; color: green;'>REVENUE FROM PRODUCT CATEGORY (ACCESSORIES) AND ITS (SUB-CATEGORIES)</h5>",
        unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fig3 = px.sunburst(filter_Accessories, path=['Product Category','Sub Category', 'Revenue'], values='Revenue',
                          color='Revenue', hover_data=['Cost'],color_continuous_scale='RdBu')
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig3)


    with col4:
        fig3 = px.bar(filter_Accessories, x='Sub Category', y='Revenue',
                      hover_data=['Cost'], color='Revenue',
                      labels={'Revenue': 'Revenue'},color_continuous_scale='RdBu')
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig3)


    st.markdown(
        "<h5 style='text-align: center; color: white;'>NUMBER OF USERS PER STATES OF SELECTED AGE</h5>",
        unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        df = df[df['age_group'] == option]
        df1 = pd.DataFrame()
        df1['states'] = df['State'].value_counts().index
        df1['Users'] = df['State'].value_counts().values
        df1 = df1.sort_values(['Users'], ascending= False)
        df1 = df1.head(10)
        fig = px.bar(df1, x='Users', y='states',text_auto='.2s')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False,marker_color='orange')
        fig.update_layout(width=700, height=500, bargap=0.05)
        st.write(fig)









