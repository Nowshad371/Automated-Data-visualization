import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#st.set_page_config(page_title="Dashboard", layout="wide")
from calendar import month_name

# bar plot for revenue and cost
def Visualization():

    df = pd.read_csv('data_store/customer_browsing/SalesForCourse_quizz_table.csv')

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


    data_group = df.groupby(['Month','age_group'])['Cost','Revenue'].apply(pd.Series.mean)
    data_group  = data_group.reset_index()
    month_lookup = list(month_name)
    data_group.Month = sorted(data_group.Month, key=month_lookup.index)


    col1, col2, col3, col4,col5,col6,col7,col8 = st.columns(8)

    with col1:

        fig1 = px.line(data_group, x="Month", y="Revenue", color="age_group",title="Revenue in Each Month From Each Age Group")
        fig1.update_layout(width=550, height=500, bargap=0.10)
        fig1.update_traces(textposition="bottom right")
        st.write(fig1)
    with col8:
        fig2 = px.line(data_group, x="Month", y='Cost', color="age_group",title="Cost in Each Month From Each Age Group")
        fig2.update_layout(width=550, height=500, bargap=0.10)
        fig2.update_traces(textposition="bottom right")
        st.write(fig2)



    col1, col2, col3, col4,col5,col6,col7,col8 = st.columns(8)

    with col1:

        data_group = df.groupby(['Month'])['Unit Cost','Unit Price','Cost','Revenue'].apply(pd.Series.mean)
        data_group  = data_group.reset_index()
        month_lookup = list(month_name)
        data_group.Month = sorted(data_group.Month, key=month_lookup.index)

        fig2 = px.line(data_group, x="Month", y=['Unit Cost','Unit Price','Cost','Revenue'],title='Cost and Revenue In Each Month')
        fig2.update_layout(width=550, height=500, bargap=0.10)
        fig2.update_traces(textposition="bottom right")
        st.write(fig2)

    with col8:
       # st.write('Cost and Revenue From Each Age Group')
        data_group = df.groupby(['age_group'])['Cost','Revenue'].apply(pd.Series.mean)
        data_group = data_group.sort_values(['Revenue'], ascending=[True])
        data_group  = data_group.reset_index()
        #data_group = df.groupby(['age_group'])['Cost','Revenue'].apply(pd.Series.mean)
        #df_items['Order'] = df_items['Order'] * -1

        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
        fig.append_trace(go.Bar(x= -data_group.Cost, y= data_group.age_group,
                                orientation='h', showlegend=True,
                                name='Cost',text = round(data_group.Cost,2),
                                marker_color='#221f1f'), 1, 1)

        fig.append_trace(go.Bar(x= data_group.Revenue, y= data_group.age_group,
                                orientation='h', showlegend=True,text = round(data_group.Revenue,2),
                                name='Revenue' ,marker_color='#b20710'), 1, 2)
        fig.update_layout(width=600, height=500, bargap=0.10)

        st.write(fig)

    data_product = df.groupby('Product Category')['Cost','Revenue'].apply(pd.Series.mean)
    data_product = data_product.reset_index()
    data_product = data_product.sort_values(['Revenue'], ascending=[False])
    data_product['ratio_cost_revenue'] = ((data_product['Revenue'] - data_product['Cost']) / data_product['Cost']) * 100
    data_product['revenue_percentage'] = (data_product['Revenue'] / data_product['Revenue'].sum()) * 100


    data_product_sub = df.groupby('Sub Category')['Cost', 'Revenue'].apply(pd.Series.mean)
    data_product_sub = data_product_sub.reset_index()
    data_product_sub= data_product_sub.sort_values(['Revenue'], ascending=[False])
    data_product_sub['ratio_cost_revenue'] = ((data_product_sub['Revenue'] - data_product_sub['Cost']) / data_product_sub['Cost']) * 100
    data_product_sub ['revenue_percentage'] = (data_product_sub['Revenue'] / data_product_sub['Revenue'].sum()) * 100
    col1,col2,col3,col4 = st.columns(4)

    with col1:
        with st.container():
            fig = px.line(x=data_product['Product Category'], y=data_product['Revenue'],title='Product Category and Revenue',color=px.Constant("This year"),
                          labels=dict(x="Product Category", y="Amount", color="Time Period"))
            fig.add_bar(x=data_product['Product Category'], y=data_product['Revenue'], name="Trends")
            fig.update_layout(width=650, height=600, bargap=0.10)
            st.write(fig)

        with st.container():
            fig = px.line(data_product, x='Product Category', y=['ratio_cost_revenue', 'revenue_percentage'],
                          title='Ratio and Percentage of Cost and Revenue of Product',labels={'value': 'Ratio and Percentage of Cost and Revenue'})
            fig.update_layout(width=650, height=600, bargap=0.10)
            st.write(fig)

    with col4:
        fig = px.line(x=data_product_sub['Sub Category'], y=data_product_sub['Revenue'], color=px.Constant("This year"),
                      title='Product Sub Category and Revenue',labels=dict(x="Sub Category", y="Amount", color="Time Period"))
        fig.add_bar(x=data_product_sub['Sub Category'], y=data_product_sub['Revenue'], name="Trends")
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig)

        with st.container():
            fig = px.line(data_product_sub, x='Sub Category', y=['ratio_cost_revenue', 'revenue_percentage'],
                          title='Ratio and Percentage of Cost and Revenue of Sub Product',labels={'value': 'Ratio and Percentage of Cost and Revenue'})
            fig.update_layout(width=650, height=600, bargap=0.10)
            st.write(fig)
