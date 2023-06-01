import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from calendar import month_name

def Visualization():
    month_df = pd.read_csv('data_store/holidays/SalesForCourse_quizz_table.csv')
    #droping unnecessay value
    month_df = month_df.drop('Column1', axis=1)
    month_df.dropna(subset=['Date'], inplace=True)

    # spliting year/months/dates from main dataset
    month_df[["month", "date", "year"]] = month_df['Date'].str.split("/", expand=True)
    #chaning datatype of the date
    month_df['date'] = month_df['date'].astype(int)
    month_df['month'] = month_df['month'].astype(int)

    month_list = []
    for i in range(len(month_df['Month'].value_counts())):
        month_list.append(month_df['Month'].value_counts().index[i])

    month_lookup = list(month_name)
    month_list = sorted(month_list, key=month_lookup.index)



    month_list.insert(0, 'None')

    start_Month, end_Month = st.select_slider(
        'Select expected Month',
        options=month_list,
        value=('None', 'None'))
    st.write('You selected month between', start_Month, 'and', end_Month)


    date_list = []
    for i in range(len(month_df['date'].value_counts())):
        date_list.append(month_df['date'].value_counts().index[i])

    date_list.insert(0, 0)
    date_list.sort()

    start_date, end_date = st.select_slider(
        'Select expected date',
        options=date_list,
        value=(0,0))
    st.write('You selected date between', start_date, 'and', end_date)

    if ((start_Month !='None') | (end_Month !='None')) & ((start_date > 0) | (end_date > 0)):
        filter_time = month_df[(month_df['Month'] == start_Month) | (month_df['Month'] == end_Month)]
        filter_time =  filter_time[(filter_time['date'] >= start_date) & (filter_time['date'] <=end_date)]
        filter_time = filter_time[['Product Category','Sub Category','Cost','Revenue']]

        #Base product
        filter_time_Product = filter_time.groupby(['Product Category'])['Cost', 'Revenue'].apply(pd.Series.mean)
        filter_time_Product = filter_time_Product.reset_index()
        filter_time_Product['ratio_cost_revenue'] = ((filter_time_Product['Revenue'] - filter_time_Product['Cost']) / filter_time_Product['Cost']) * 100
        filter_time_Product['revenue_percentage'] = (filter_time_Product['Revenue'] / filter_time_Product['Revenue'].sum()) * 100
        filter_time_Product['Profit'] = filter_time_Product['Revenue'] - filter_time_Product['Cost']


        #sub category

        data_product_sub = filter_time.groupby('Sub Category')['Cost', 'Revenue'].apply(
            pd.Series.mean)
        data_product_sub = data_product_sub.reset_index()
        data_product_sub['ratio_cost_revenue'] = ((data_product_sub['Revenue'] - data_product_sub['Cost']) /
                                                  data_product_sub['Cost']) * 100
        data_product_sub['revenue_percentage'] = (data_product_sub['Revenue'] / data_product_sub[
            'Revenue'].sum()) * 100
        data_product_sub['Profit'] = data_product_sub['Revenue'] - data_product_sub['Cost']

        #
        # Base product
        filter_time_individual = filter_time.groupby(['Product Category','Sub Category'])['Cost', 'Revenue'].apply(pd.Series.mean)
        filter_time_individual = filter_time_individual.reset_index()

       # filter bike
        filter_bike = filter_time_individual[filter_time_individual['Product Category'] == 'Bikes']
        filter_bike['ratio_cost_revenue'] = ((filter_bike['Revenue'] - filter_bike['Cost']) /
                                                     filter_bike['Cost']) * 100
        filter_bike['revenue_percentage'] = (filter_bike['Revenue'] / filter_bike[
            'Revenue'].sum()) * 100
        filter_bike['Profit'] = filter_bike['Revenue'] - filter_bike['Cost']

        #Accesories

        filterAccesories = filter_time_individual[filter_time_individual['Product Category'] == 'Accessories']
        filterAccesories['ratio_cost_revenue'] = ((filterAccesories ['Revenue'] - filterAccesories ['Cost']) /
                                             filterAccesories['Cost']) * 100
        filterAccesories ['revenue_percentage'] = (filterAccesories ['Revenue'] / filter_bike[
            'Revenue'].sum()) * 100
        filterAccesories ['Profit'] = filterAccesories ['Revenue'] - filterAccesories ['Cost']


        #filter Clothing
        filterClothing = filter_time_individual[filter_time_individual['Product Category'] == 'Clothing']
        filterClothing ['ratio_cost_revenue'] = ((filterClothing ['Revenue'] - filterClothing['Cost']) /
                                                  filterClothing ['Cost']) * 100
        filterClothing ['revenue_percentage'] = (filterClothing ['Revenue'] / filter_bike[
            'Revenue'].sum()) * 100
        filterClothing ['Profit'] = filterClothing ['Revenue'] - filterClothing ['Cost']


        col1, col2, col3, col4,col5 ,col6,col7,col8 = st.columns(8)
        with col1:
            with st.container():
                filter_time_Product = filter_time_Product.sort_values(['Revenue'], ascending=[True])
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=-filter_time_Product.Cost, y=filter_time_Product['Product Category'],
                                        orientation='h', showlegend=True,
                                        name='Cost', text=round(filter_time_Product.Cost, 2),
                                        marker_color='#221f1f'), 1, 1)

                fig.append_trace(go.Bar(x=filter_time_Product.Revenue, y=filter_time_Product['Product Category'],
                                        orientation='h', showlegend=True, text=round(filter_time_Product.Revenue, 2),
                                        name='Revenue', marker_color='#b20710'), 1, 2)

                fig.update_layout(width=600, height=350, bargap=0.10)
                st.write(fig)

            with st.container():
                data_product_sub = data_product_sub.sort_values(['Revenue'], ascending=[False])
                fig = px.line(x=data_product_sub['Sub Category'], y=data_product_sub['Revenue'],
                              color=px.Constant("This year"),
                              title='Product Sub Category and Revenue',
                              labels=dict(x="Sub Category", y="Amount", color="Time Period"))
                fig.add_bar(x=data_product_sub['Sub Category'], y=data_product_sub['Revenue'], name="Trends")
                fig.update_layout(width=500, height=600, bargap=0.10)
                st.write(fig)



        with col8:
            with st.container():
                filter_time_Product = filter_time_Product.sort_values(['Profit'], ascending=[True])
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=filter_time_Product.Profit, y=filter_time_Product['Product Category'],
                                        orientation='h', showlegend=True, text=round(filter_time_Product.Profit, 2),
                                        name='Profit', marker_color='#FFBF00'), 1, 1)
                fig.update_layout(width=500, height=350, bargap=0.10)
                st.write(fig)

            with st.container():


                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(
                    go.Bar(x=-filter_time_Product.ratio_cost_revenue, y=filter_time_Product['Product Category'],
                           orientation='h', showlegend=True,
                           name='ratio_cost_revenue', text=round(filter_time_Product.ratio_cost_revenue, 2),
                           marker_color='#90EE90'), 1, 1)

                fig.append_trace(
                    go.Bar(x=filter_time_Product.revenue_percentage, y=filter_time_Product['Product Category'],
                           orientation='h', showlegend=True,
                           text=round(filter_time_Product.revenue_percentage, 2),
                           name='revenue_percentage', marker_color='#b20710'), 1, 2)
                fig.update_layout(width=500, height=350, bargap=0.10)
                st.write(fig)

        col1, col2, col3, col4,col5 ,col6,col7,col8 = st.columns(8)
        with col1:


            with st.container():
                filter_bike = filter_bike.sort_values(['Revenue'], ascending=[True])
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=-filter_bike.Cost, y=filter_bike['Sub Category'],
                                        orientation='h', showlegend=True,
                                        name='Cost', text=round(filter_bike.Cost, 2),
                                        marker_color='#221f1f'), 1, 1)

                fig.append_trace(go.Bar(x=filter_bike.Revenue, y=filter_bike['Sub Category'],
                                        orientation='h', showlegend=True, text=round(filter_bike.Revenue, 2),
                                        name='Revenue', marker_color='#b20710'), 1, 2)

                fig.update_layout(width=600, height=350, bargap=0.10,title = 'Bike Categories Details')
                st.write(fig)
            with st.container():
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(
                    go.Bar(x=-filter_bike.ratio_cost_revenue, y=filter_bike['Sub Category'],
                           orientation='h', showlegend=True,
                           name='ratio_cost_revenue', text=round(filter_bike.ratio_cost_revenue, 2),
                           marker_color='#90EE90'), 1, 1)

                fig.append_trace(
                    go.Bar(x=filter_bike.revenue_percentage, y=filter_bike['Sub Category'],
                           orientation='h', showlegend=True,
                           text=round(filter_bike.revenue_percentage, 2),
                           name='revenue_percentage', marker_color='#b20710'), 1, 2)
                fig.update_layout(width=550, height=400, bargap=0.10)
                st.write(fig)
            with st.container():
                filter_bike = filter_bike.sort_values(['Profit'], ascending=[True])
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=filter_bike.Profit, y=filter_bike['Sub Category'],
                                        orientation='h', showlegend=True, text=round(filter_bike.Profit, 2),
                                        name='Profit', marker_color='#FFBF00'), 1, 1)
                fig.update_layout(width=500, height=350, bargap=0.10)
                st.write(fig)

        with col8:
            with st.container():
                filterAccesories = filterAccesories.sort_values(['Revenue'], ascending=[True])
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=-filterAccesories.Cost, y=filterAccesories['Sub Category'],
                                        orientation='h', showlegend=True,
                                        name='Cost', text=round(filterAccesories.Cost, 2),
                                        marker_color='#221f1f'), 1, 1)

                fig.append_trace(go.Bar(x=filterAccesories.Revenue, y=filterAccesories['Sub Category'],
                                        orientation='h', showlegend=True, text=round(filterAccesories.Revenue, 2),
                                        name='Revenue', marker_color='#b20710'), 1, 2)

                fig.update_layout(width=750, height=350, bargap=0.10,title = 'Accessories Categories Details')
                st.write(fig)
            with st.container():
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(
                    go.Bar(x=-filterAccesories.ratio_cost_revenue, y=filterAccesories['Sub Category'],
                           orientation='h', showlegend=True,
                           name='ratio_cost_revenue', text=round(filterAccesories.ratio_cost_revenue, 2),
                           marker_color='#90EE90'), 1, 1)

                fig.append_trace(
                    go.Bar(x=filterAccesories.revenue_percentage, y=filterAccesories['Sub Category'],
                           orientation='h', showlegend=True,
                           text=round(filterAccesories.revenue_percentage, 2),
                           name='revenue_percentage', marker_color='#b20710'), 1, 2)
                fig.update_layout(width=750, height=400, bargap=0.10)
                st.write(fig)
            with st.container():
                filter_bike = filterAccesories.sort_values(['Profit'], ascending=[True])
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=filterAccesories.Profit, y=filterAccesories['Sub Category'],
                                        orientation='h', showlegend=True, text=round(filterAccesories.Profit, 2),
                                        name='Profit', marker_color='#FFBF00'), 1, 1)
                fig.update_layout(width=600, height=350, bargap=0.10)
                st.write(fig)

        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        with col1:
            with st.container():
                filterClothing = filterClothing.sort_values(['Revenue'], ascending=[True])
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=-filterClothing.Cost, y=filterClothing['Sub Category'],
                                        orientation='h', showlegend=True,
                                        name='Cost', text=round(filterClothing.Cost, 2),
                                        marker_color='#221f1f'), 1, 1)

                fig.append_trace(go.Bar(x=filterClothing.Revenue, y=filterClothing['Sub Category'],
                                        orientation='h', showlegend=True, text=round(filterClothing.Revenue, 2),
                                        name='Revenue', marker_color='#b20710'), 1, 2)

                fig.update_layout(width=600, height=350, bargap=0.10, title='Clothing Categories Details')
                st.write(fig)
            with st.container():
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(
                    go.Bar(x=-filterClothing.ratio_cost_revenue, y=filterClothing['Sub Category'],
                           orientation='h', showlegend=True,
                           name='ratio_cost_revenue', text=round(filterClothing.ratio_cost_revenue, 2),
                           marker_color='#90EE90'), 1, 1)

                fig.append_trace(
                    go.Bar(x=filterClothing.revenue_percentage, y=filterClothing['Sub Category'],
                           orientation='h', showlegend=True,
                           text=round(filterClothing.revenue_percentage, 2),
                           name='revenue_percentage', marker_color='#b20710'), 1, 2)
                fig.update_layout(width=550, height=400, bargap=0.10)
                st.write(fig)
            with st.container():
                filterClothing = filterClothing.sort_values(['Profit'], ascending=[True])
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=filterClothing.Profit, y=filterClothing['Sub Category'],
                                        orientation='h', showlegend=True, text=round(filterClothing.Profit, 2),
                                        name='Profit', marker_color='#FFBF00'), 1, 1)
                fig.update_layout(width=500, height=350, bargap=0.10)
                st.write(fig)

    else:
        st.write('Both Month and data must be selected')

