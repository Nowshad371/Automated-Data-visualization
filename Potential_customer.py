import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

def Visualization():
    solution = pd.read_csv('data_store/solution/soluton_df.csv')

    #previous
    solution2022 = pd.read_csv('data_store/solution/solution_2022.csv')
    solution2022.rename(columns={'userID|itemID|prediction': 'data'}, inplace=True)
    solution2022[['user_Id', 'item_Id', 'prediction']] = solution2022['data'].str.split('|', expand=True)
    solution2022.drop('data', axis=1, inplace=True)

    solution2022['prediction'] = solution2022['prediction'].astype(int)
    for i in range(len(solution2022)):
        if (solution['prediction'].iloc[i] > 4 ):
            solution['prediction'].iloc[i] = 4

    view = pd.DataFrame()
    view[['index','values']] = ''

    viewpre = pd.DataFrame()
    viewpre[['index','values']] = ''
    for index in range(len(solution.prediction.value_counts())):
        view.loc[len(view.index)] = [solution.prediction.value_counts().index[index],
                                     solution.prediction.value_counts().values[index]]

    for index in range(len(solution2022.prediction.value_counts())):
        viewpre.loc[len(viewpre.index)] = [solution2022.prediction.value_counts().index[index],
                                           solution2022.prediction.value_counts().values[index]]


    view['values'] = view['values'].astype(int)
    view['index'] = view['index'].astype(str)
    view['index'] = 'Index  ' + view['index']


    viewpre['values'] = viewpre['values'].astype(int)
    viewpre['index'] = viewpre['index'].astype(str)
    viewpre['index'] = 'Index  ' + viewpre['index']


    view = view.sort_values(['values'], ascending=[False])
    viewpre =viewpre.sort_values(['values'], ascending=[False])


    st.markdown(
        "<h5 style='text-align: center; color: #FAF9F6;'>Predicted Value</h5>",
        unsafe_allow_html=True)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        fig = px.bar(view, x= 'values', y= 'index',text_auto='.2s',color='values',
                                 labels={'Revenue':'Revenue in Each Product'},color_continuous_scale='RdBu')
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig)


    with col5:
        fig = px.line(x=view['index'], y=viewpre['values'], color=px.Constant("Actual Prediction"),
                      labels=dict(x="Category", y="Total values", color="Time Period"))
        fig.add_bar(x=view['index'], y=view['values'], name="Prediction for next month")
        fig.update_layout(width=650, height=600, bargap=0.10)
        st.write(fig)



    solution = solution.sort_values(['prediction'], ascending=[True])
    inconsistentCustomer = solution[solution['prediction'] == 0]
    inconsistentCustomer['user_Id'] = inconsistentCustomer['user_Id'].astype(str)


    def highlight_Table(data):
        return ['background-color: green'] * len(data)


    st.markdown(
        "<h6 style='text-align: center; color: #FAF9F6;'>Customer who likely to not buy any product next month</h6>",
        unsafe_allow_html=True)
    st.dataframe(inconsistentCustomer.style.apply(highlight_Table, axis=1), width=700, height=None, use_container_width=False)




