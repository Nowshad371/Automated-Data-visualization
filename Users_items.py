import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
placeholder = st.empty()

def Visualization():
    #importing  items list
    store_df = pd.read_csv ('data_store/item_details/store.csv')
    #Sorting Users
    UserId = store_df.user_Id.unique()
    UserId = map(str,UserId)
    UserId = np.insert(list(UserId),0,"")
    users = UserId



    #importing order dataset

    Order_df = pd.read_csv (r'data_store/dashboard/orders.csv',sep='\t')
    Order_df.rename(columns={'date|userID|itemID|order': 'data'}, inplace=True)
    Order_df[['date', 'user_Id','item_Id','Order']] = Order_df['data'].str.split('|', expand=True)
    Order_df.drop('data', axis=1, inplace=True)
    Order_df['Order'] = Order_df['Order'].astype(int)







    #Grouping order and userId using sum function overall
    df= Order_df.groupby('user_Id').agg({'Order':'sum'})
    df  = df.reset_index()

    df = df.sort_values(['Order'], ascending=[False])

    # display the dataframe
    df['user_Id'] = df['user_Id'].astype(str)
    df['user_Id'] = 'UserId' + " " + df['user_Id']
    df = df.head(20)
    df = df.sort_values(['Order'], ascending=[True])

    ####
    df_items = Order_df.groupby('item_Id').agg({'Order':'sum'})
    df_items = df_items.reset_index()
    df_items = df_items.sort_values(['Order'], ascending=[False])
    df_items['item_Id'] = df_items['item_Id'].astype(str)
    df_items['item_Id'] = 'item_Id' + " " + df_items['item_Id']






    top_df_items = df_items.head(20)
    top_df_items = top_df_items.sort_values(['Order'], ascending=[True])


    st.markdown(
            "<h4 style='text-align: center; color: #FAF9F6;'>TOP RETAILERS AND INVIDIDUAL RETAILERS BUYING HISTORY </h4>",
            unsafe_allow_html=True)
    # users history
    selected_user = st.selectbox(
        "Type or Select User Id",
        users
    )

    if (selected_user != ""):
        st.write('User ID: ', selected_user)

    col1, col2, col3, col4,col5,col6,col7,col8 = st.columns(8)
    with col1:
            fig = px.bar(df, x='Order', y='user_Id', title="Top retailers", text_auto='.2s', color='Order',
                         color_continuous_scale='RdBu')
            # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='orange')
            fig.update_layout(width=600, height=600, bargap=0.10)
            st.write(fig)

    with col7:

        # filtering individual history
        individual_df = Order_df[Order_df['user_Id'] == selected_user]
        # grouping individual history
        individual_df = individual_df.groupby('item_Id').agg({'Order': 'sum'})
        individual_df = individual_df.reset_index()
        individual_df_top_items = individual_df.sort_values(['Order'], ascending=[False])
        individual_df_top_items = individual_df_top_items.head(20)
        individual_df_top_items = individual_df_top_items.sort_values(['Order'], ascending=[True])

        # turning id into string
        individual_df_top_items['item_Id'] = individual_df_top_items['item_Id'].astype(str)
        individual_df_top_items['item_Id'] = 'item_Id' + " " + individual_df_top_items['item_Id']

        # visualize
        fig = px.bar(individual_df_top_items, x='Order', y='item_Id', title="Top Items", text_auto='.2s', color='Order',
                     color_continuous_scale='RdBu')
        # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='orange')
        fig.update_layout(width=600, height=600, bargap=0.10)
        st.write(fig)



    st.write('\n\n\n')
    st.markdown(
            "<h5 style='text-align: center; color: #FAF9F6;'>MOST & LESS DEMANDED PRODUCT (SURGE PRICE) MIGHT BE APPLY USING THIS HISTORY OF ITEMS </h5>",
            unsafe_allow_html=True)


    #Viualize using barplot
    option = st.radio(
            "CLICK OPTION THAT YOU WANT TO KNOW",
            ('NONE', 'WEEK 1', 'WEEK 2', 'WEEK3','WEEK4'))

    col1, col2, col3, col4,col5,col6,col7,col8 = st.columns(8)

    with col1:

        fig = px.bar(top_df_items, x='Order', y='item_Id', title="Top Items", text_auto='.2s', color='Order',
                     color_continuous_scale='RdBu')
        # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='orange')
        fig.update_layout(width=600, height=600, bargap=0.10)
        st.write(fig)
    with col7:
        # spliting date

        Order_df[["year", "month", "day"]] = Order_df['date'].str.split("-", expand=True)
        Order_df['day'] = Order_df['day'].astype(int)
        if option == 'NONE':
            st.write("")

        elif option == 'WEEK 1':
            filter_week = Order_df[(Order_df['day'] >= 1) & (Order_df['day'] <= 7)]
            # grouping individual history
            filter_week = filter_week.groupby('item_Id').agg({'Order': 'sum'})
            filter_week = filter_week.reset_index()
            filter_week = filter_week.sort_values(['Order'], ascending=[False])
            filter_week = filter_week.head(20)
            filter_week = filter_week.sort_values(['Order'], ascending=[True])
            # turning id into string
            filter_week['item_Id'] = filter_week['item_Id'].astype(str)
            filter_week['item_Id'] = 'item_Id' + " " + filter_week['item_Id']
            # visualize
            fig = px.bar(filter_week, x='Order', y='item_Id', title="Top Items in Week 1", text_auto='.2s', color='Order',
                         color_continuous_scale='RdBu')
            # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='orange')
            fig.update_layout(width=600, height=600, bargap=0.10)
            st.write(fig)


        elif option == 'WEEK 2':
            filter_week = Order_df[(Order_df['day'] >= 8) & (Order_df['day'] <= 15)]
            # grouping individual history
            filter_week = filter_week.groupby('item_Id').agg({'Order': 'sum'})
            filter_week = filter_week.reset_index()
            filter_week = filter_week.sort_values(['Order'], ascending=[False])
            filter_week = filter_week.head(20)
            filter_week = filter_week.sort_values(['Order'], ascending=[True])
            # turning id into string
            filter_week['item_Id'] = filter_week['item_Id'].astype(str)
            filter_week['item_Id'] = 'item_Id' + " " + filter_week['item_Id']
            # visualize
            fig = px.bar(filter_week, x='Order', y='item_Id', title="Top Items in Week 2", text_auto='.2s', color='Order',
                         color_continuous_scale='RdBu')
            # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='orange')
            fig.update_layout(width=650, height=600, bargap=0.10)
            st.write(fig)

        elif option == 'WEEK 3':
            filter_week = Order_df[(Order_df['day'] >= 16) & (Order_df['day'] <= 21)]
            # grouping individual history
            filter_week = filter_week.groupby('item_Id').agg({'Order': 'sum'})
            filter_week = filter_week.reset_index()
            filter_week = filter_week.sort_values(['Order'], ascending=[False])
            filter_week = filter_week.head(20)
            filter_week = filter_week.sort_values(['Order'], ascending=[True])
            # turning id into string
            filter_week['item_Id'] = filter_week['item_Id'].astype(str)
            filter_week['item_Id'] = 'item_Id' + " " + filter_week['item_Id']
            # visualize
            fig = px.bar(filter_week, x='Order', y='item_Id', title="Top Items in Week 3", text_auto='.2s', color='Order',
                         color_continuous_scale='RdBu')
            # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='orange')
            fig.update_layout(width=650, height=600, bargap=0.10)
            st.write(fig)

        else:
            filter_week = Order_df[Order_df['day'] >= 22]
            # grouping individual history
            filter_week = filter_week.groupby('item_Id').agg({'Order': 'sum'})
            filter_week = filter_week.reset_index()
            filter_week = filter_week.sort_values(['Order'], ascending=[False])
            filter_week = filter_week.head(20)
            filter_week = filter_week.sort_values(['Order'], ascending=[True])
            # turning id into string
            filter_week['item_Id'] = filter_week['item_Id'].astype(str)
            filter_week['item_Id'] = 'item_Id' + " " + filter_week['item_Id']
            # visualize
            fig = px.bar(filter_week, x='Order', y='item_Id', title="Top Items in Week 4", text_auto='.2s', color='Order',
                         color_continuous_scale='RdBu')
            # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='orange')
            fig.update_layout(width=650, height=600, bargap=0.10)
            st.write(fig)




    #visualize using table
    #low demanded items
    low_df_items = df_items[df_items['Order'] <= 100]
    def highlight_lowest(p):
        return ['background-color: green'] * len(p) if p.Order > 80 else ['background-color: blue'] * len(
            p) if p.Order > 50 else ['background-color: red'] * len(p)
    st.markdown(
            "<h6 style='text-align: left; color: #FAF9F6;'>LOW DEMANDED ITEMS</h6>",
            unsafe_allow_html=True)


    st.dataframe(low_df_items.style.apply(highlight_lowest, axis=1),width=700, height=None, use_container_width=False)





