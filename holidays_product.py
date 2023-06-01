import pandas as pd
import numpy as np
import calendar
from datetime import date
from datetime import datetime
import datetime
import holidays
import re
import streamlit as st
import time
import plotly.express as px
placeholder = st.empty()
import random
# Select country


def Visualization():
    uk_holidays = holidays.UnitedKingdom()


    pattern = '\d{4}-\d{1,2}-\d{1,2}'

    flag = True

    while(flag == True):
        from datetime import datetime
        date = datetime.today().strftime('%Y-%m-%d')
        list_date = []
        Upcoming_holidays = []
        i = 0
        # Importing Pandas to create DataFrame


        current_time = time.strftime("%H:%M:%S")


        # Creating Empty DataFrame and Storing it in variable df
        df_holidays = pd.DataFrame()
        df_holidays['date_string'] = ''
        df_holidays['holidays'] = ''
        #getting current year
        Current_Year = datetime.today().strftime('%Y')
        # Print all the holidays in UnitedKingdom in year 2018
        for ptr in holidays.UnitedKingdom(years=int(Current_Year)).items():
            list_date.append(ptr[0])
            Upcoming_holidays.append(ptr[1])
            m = re.findall(pattern, str(list_date[i]))
            date_string = (m[0])
            Upcoming_h = (Upcoming_holidays[i])
            df_holidays.loc[len(df_holidays.index)] = [date_string, Upcoming_h]
            i = i + 1
        df_holidays.sort_values(by='date_string', ascending=True, inplace=True)
        #Drop passed holidays from dataframe
        rslt_df = df_holidays[df_holidays['date_string'] > date]
        with placeholder.container():
            # create three columns
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label="Time",
                value= current_time,
                #delta=round(n) - 10,
            )

            kpi2.metric(
                label="Today is ",
                value=date
            )


            # create two columns for charts
            fig_col1, fig_col2,fig_col3 = st.columns(3)
            if (rslt_df['date_string'].iloc[0] == date):
                with fig_col1:
                    with st.container():
                        st.markdown("##### Going on: ")
                        st.write("#####   '",rslt_df['holidays'].iloc[0], "' on ",rslt_df['date_string'].iloc[0])

            elif (rslt_df['date_string'].iloc[0] >= date):
                with fig_col1:
                    with st.container():
                        st.markdown("##### Upcoming holidays:")
                        st.write("#####   '", rslt_df['holidays'].iloc[0], "' on ",rslt_df['date_string'].iloc[0])
            progress_text = "Operation in progress. Please wait."


            st.write("\n\n\n")

            #storing upcoming holidays date
            up_h = rslt_df['date_string'].iloc[0]

            import datetime
            #turning string into datatime (listed date)
            entered_date = datetime.datetime.strptime(up_h, '%Y-%m-%d')
            entered_date = entered_date.date()

            #taking estimated days around holidays
            last_10days = entered_date - datetime.timedelta(days=15)
            next_7days = entered_date + datetime.timedelta(days=10)


            #Spliting dates
            pre_sell = str(last_10days).split("-")
            post_sell = str(next_7days).split("-")

            #importing previous dataset
            df = pd.read_csv('data_store/holidays/SalesForCourse_quizz_table.csv')

            #droping unnecessay value
            df = df.drop('Column1', axis=1)
            df.dropna(subset=['Month'], inplace=True)

            #spliting year/months/dates from main dataset
            df[["month", "date", "year"]] = df['Date'].str.split("/", expand=True)

            #chaning datatype of the date
            df['date'] = df['date'].astype(int)
            df['month'] = df['month'].astype(int)

            #filtering dataset to take previous sold product on these estimated dates
            #filter = df[((df['month'] == int(pre_sell[1])) | (df['month'] == int(post_sell[1])))]

            demanded_product = df[
                    (df['date'] >= int(pre_sell[2])) & (df['month'] == int(pre_sell[1])) | (df['date'] <= int(post_sell[2])) & (df['month'] == int(post_sell[1]))]


            #grouping product in decending order to see most sold product
            demanded_product_quantity = demanded_product.groupby(['Product Category','Sub Category'])['Quantity'].apply(pd.Series.mean)
            demanded_product_quantity = demanded_product_quantity.reset_index()
            demanded_product_quantity = demanded_product_quantity.sort_values(['Quantity'], ascending=[False])
            demanded_product_quantity['Quantity'] = round(demanded_product_quantity.Quantity, 2)
            #demanded_product_quantity['Text'] = demanded_product_quantity['Sub Category'] + " Avg :" + demanded_product_quantity['Quantity'].astype(str)

            #Visualization
            st.markdown("<h4 style='text-align: center; color: white;'>PRODUCT THAT LIKELY TO SELL MORE (B-C)</h4>",
                        unsafe_allow_html=True)
            st.markdown(
                "<h5 style='text-align: center; color: #FAF9F6;'>Accessories/Clothing/Bike Product</h5>",
                unsafe_allow_html=True)
            col1,col2 = st.columns(2)
            with col1:
                fig = px.treemap(demanded_product_quantity, path=[px.Constant('Average Quantity - Each Customer'), 'Product Category', 'Sub Category'], values='Quantity',
                                 color='Quantity', hover_data=['Quantity'],color_continuous_scale='RdBu',
                          color_continuous_midpoint=np.average(df['Quantity'], weights=df['Quantity']))
                fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
                st.write(fig)




            ###wholesalers

            st.markdown("<h4 style='text-align: center; color: #FAF9F6;'>PROBABLY DEMANDING PRODUCT FROM ONLINR STORE TO WHOLESALERS (B-B)</h4>",
                        unsafe_allow_html=True)

            #Importing dataset
            df_online_retail = pd.read_csv('data_store/holidays/data 2.csv', encoding='unicode_escape')

            #cleaning
            df_online_retail['Description'].replace('?', np.nan, inplace=True)
            df_online_retail['Description'].replace('missing', np.nan, inplace=True)
            df_online_retail['Description'].replace('sold as set on dotcom', np.nan, inplace=True)
            df_online_retail['Description'].replace('sold as set on dotcom and amazon', np.nan, inplace=True)
            df_online_retail['Description'].replace('mystery! Only ever imported 1800', np.nan, inplace=True)
            df_online_retail['Description'].replace('POSSIBLE DAMAGES OR LOST?', np.nan, inplace=True)
            df_online_retail['Description'].replace('wet damaged', np.nan, inplace=True)
            df_online_retail['Description'].replace('on cargo order', np.nan, inplace=True)
            df_online_retail['Description'].replace('damages', np.nan, inplace=True)
            df_online_retail['Description'].replace('damages/dotcom?', np.nan, inplace=True)
            df_online_retail['Description'].replace('incorrectly credited C550456 see 47', np.nan, inplace=True)
            df_online_retail['Description'].replace('reverse previous adjustment', np.nan, inplace=True)
            df_online_retail['Description'].replace('sold as set/6 by dotcom', np.nan, inplace=True)
            df_online_retail['Description'].replace('damages/dotcom?', np.nan, inplace=True)
            df_online_retail['CustomerID'] = df_online_retail['CustomerID'].fillna(df_online_retail['CustomerID'].mode()[0])
            df_online_retail.dropna(subset=['Description'], inplace=True)

            #Spliting data and time
            df_online_retail[['Date', 'time']] = df_online_retail['InvoiceDate'].str.split(" ", expand=True)
            df_online_retail[["month", "date", "year"]] = df_online_retail['Date'].str.split("/", expand=True)

            #converting number into integer from string
            df_online_retail['month'] = df_online_retail['month'].astype(int)
            df_online_retail['date'] = df_online_retail['date'].astype(int)
            df_online_retail['Quantity'] = df_online_retail['Quantity'].astype(int)
            df_online_retail['Quantity'] = abs(df_online_retail.Quantity)

            #filtering data
            #filter_online_retail = df_online_retail[((df_online_retail['month'] == int(pre_sell[1])) | (df_online_retail['month'] == int(post_sell[1])))]

            demanded_product_online_retail = df_online_retail[
                (df_online_retail['date'] >= int(pre_sell[2])) & (df_online_retail['month'] == int(pre_sell[1])) | (df_online_retail['date'] <= int(post_sell[2])) & (
                            df_online_retail['month'] == int(post_sell[1]))]

            demanded_product_up = demanded_product_online_retail.groupby(['Description'])['Quantity'].apply(pd.Series.mean)
            demanded_product_up = demanded_product_up.reset_index()
            demanded_product_up = demanded_product_up.sort_values(['Quantity'], ascending=[False]).head(20)
            fig = px.bar(demanded_product_up, x='Quantity', y='Description', title="Most demanded product", text_auto='.2s')
            fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='orange')
            fig.update_layout(width=900, height=600, bargap=0.10)
            st.write(fig)




    ########## WORK LEFT (FILTERING)





