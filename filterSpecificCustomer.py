import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def highlight_Table(data):
    return ['background-color: green'] * len(data)

def Visualization():
    df = pd.read_csv('data_store/holidays/SalesForCourse_quizz_table.csv')

    data_group = df.groupby(['Customer Age','Product Category','Sub Category'])['Cost','Revenue'].apply(pd.Series.mean)
    data_group = data_group.reset_index()

    age_list = []
    for i in range(len(data_group['Customer Age'].value_counts())):
        age_list.append(data_group['Customer Age'].value_counts().index[i])

    age_list.insert(0, 0)
    age_list.sort()

    start_age, end_age = st.select_slider(
        'Select expected age',
        options= age_list,
        value=(0, 0))
    st.write('You selected age between', start_age, 'and', end_age)

    if(start_age >= 17) | (end_age >= 17):
        filter_age = data_group [(data_group ['Customer Age'] >= start_age) & (data_group ['Customer Age'] <= end_age)]
        filter_age['ratio_cost_revenue'] = ((filter_age['Revenue'] - filter_age['Cost']) / filter_age['Cost']) * 100
        filter_age['revenue_percentage'] = (filter_age['Revenue'] / filter_age['Revenue'].sum()) * 100

        col1, col2, col3, col4,col5 ,col6 = st.columns(6)
        with col1:

            # st.write('Cost and Revenue From Each Age Group')
            filter_age_into_one = filter_age[['Customer Age','Cost', 'Revenue','ratio_cost_revenue','revenue_percentage']]
            filter_age_into_one['Customer Age'] = 'Age'

            filter_age_selected = filter_age_into_one.groupby(['Customer Age'])['Cost', 'Revenue','ratio_cost_revenue','revenue_percentage'].apply(pd.Series.mean)
            filter_age_selected = filter_age_selected.reset_index()
            filter_age_selected = filter_age_selected.sort_values(['Revenue'], ascending=[True])
            filter_age_selected['Profit'] = filter_age_selected['Revenue'] - filter_age_selected['Cost']
            # data_group = df.groupby(['age_group'])['Cost','Revenue'].apply(pd.Series.mean)
            # df_items['Order'] = df_items['Order'] * -1

            with st.container():
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=-filter_age_selected.Cost, y=filter_age_selected['Customer Age'],
                                        orientation='h', showlegend=True,
                                        name='Cost', text=round(filter_age_selected.Cost, 2),
                                        marker_color='#221f1f'), 1, 1)

                fig.append_trace(go.Bar(x=filter_age_selected.Revenue, y=filter_age_selected['Customer Age'],
                                        orientation='h', showlegend=True, text=round(filter_age_selected.Revenue, 2),
                                        name='Revenue', marker_color='#b20710'), 1, 2)


                fig.update_layout(width=500, height=250, bargap=0.10)
                st.write(fig)

            with st.container():
                fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
                fig.append_trace(go.Bar(x=filter_age_selected.Profit, y=filter_age_selected['Customer Age'],
                                        orientation='h', showlegend=True, text=round(filter_age_selected.Profit, 2),
                                        name='Profit', marker_color='#FFBF00'), 1, 2)
                fig.update_layout(width=600, height=250, bargap=0.10)
                st.write(fig)

        with col6:
            fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
            fig.append_trace(go.Bar(x=-filter_age_selected.ratio_cost_revenue, y=filter_age_selected['Customer Age'],
                                    orientation='h', showlegend=True,
                                    name='ratio_cost_revenue', text=round(filter_age_selected.ratio_cost_revenue, 2),
                                    marker_color='#90EE90'), 1, 1)

            fig.append_trace(go.Bar(x=filter_age_selected.revenue_percentage, y=filter_age_selected['Customer Age'],
                                    orientation='h', showlegend=True, text=round(filter_age_selected.revenue_percentage, 2),
                                    name='revenue_percentage', marker_color='#b20710'), 1, 2)
            fig.update_layout(width=600, height=250, bargap=0.10)

            st.write(fig)


        #Base Product
        data_product = filter_age.groupby('Product Category')['Revenue','ratio_cost_revenue','revenue_percentage'].apply(pd.Series.mean)
        data_product = data_product.reset_index()
        data_product = data_product.sort_values(['Revenue'], ascending=[False])

        #Sub Product
        data_product_sub = filter_age.groupby('Sub Category')['Revenue','ratio_cost_revenue','revenue_percentage'].apply(pd.Series.mean)
        data_product_sub = data_product_sub.reset_index()
        data_product_sub = data_product_sub.sort_values(['Revenue'], ascending=[False])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container():
                fig = px.line(x=data_product['Product Category'], y=data_product['Revenue'],
                              title='Product Category and Revenue', color=px.Constant("This year"),
                              labels=dict(x="Product Category", y="Amount", color="Time Period"))
                fig.add_bar(x=data_product['Product Category'], y=data_product['Revenue'], name="Trends")
                fig.update_layout(width=650, height=600, bargap=0.10)
                st.write(fig)

            with st.container():
                fig = px.line(data_product, x='Product Category', y=['ratio_cost_revenue', 'revenue_percentage'],
                              title='Ratio and Percentage of Cost and Revenue of Product',
                              labels={'value': 'Ratio and Percentage of Cost and Revenue'})
                fig.update_layout(width=650, height=600, bargap=0.10)
                st.write(fig)

        with col4:
            fig = px.line(x=data_product_sub['Sub Category'], y=data_product_sub['Revenue'], color=px.Constant("This year"),
                          title='Product Sub Category and Revenue',
                          labels=dict(x="Sub Category", y="Amount", color="Time Period"))
            fig.add_bar(x=data_product_sub['Sub Category'], y=data_product_sub['Revenue'], name="Trends")
            fig.update_layout(width=650, height=600, bargap=0.10)
            st.write(fig)

            with st.container():
                fig = px.line(data_product_sub, x='Sub Category', y=['ratio_cost_revenue', 'revenue_percentage'],
                              title='Ratio and Percentage of Cost and Revenue of Sub Product',
                              labels={'value': 'Ratio and Percentage of Cost and Revenue'})
                fig.update_layout(width=650, height=600, bargap=0.10)
                st.write(fig)

        st.write('Database record between age: {0} - {1}'.format(start_age,end_age))
        st.dataframe(filter_age.style.apply(highlight_Table, axis=1), width=1000, height=None,use_container_width=False)
    else:
        st.write('Minimum customer age is: ',data_group['Customer Age'].min())



