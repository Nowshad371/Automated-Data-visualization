import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

st.set_page_config(
page_title = "Real-Time Data Science Dashboard",
page_icon = "✅",
layout = "wide",
)





df = pd.read_csv(r'movies_metadata.csv')
# dashboard title
st.title("Real-Time / Live Data Science Dashboard")

# top-level filters
job_filter = st.selectbox("Select the Job", pd.unique(df["title"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["title"] == job_filter]
df['vote_count'] = df['vote_count'].astype(int)
df['runtime'] = df['runtime'].astype(int)
df['revenue'] = df['revenue'].astype(int)
# near real-time / live feed simulation
for seconds in range(200):
    df["vote_count_new"] = df["vote_count"] * np.random.choice(range(1, 5))

    df["revenue_new"] = df["revenue"] * np.random.choice(range(1, 5))

    # creating KPIs
    avg_vote_count = np.mean(df["vote_count_new"])

    count_married = int(
        df[(df["original_language"] == "en")]["original_language"].count()
        + np.random.choice(range(1, 30))
    )

    balance = np.mean(df["revenue_new"])

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Age ⏳",
            value=round(avg_vote_count),
            delta=round(avg_vote_count) - 10,
        )

        kpi2.metric(
            label="Married Count 💍",
            value=int(count_married),
            delta=-10 + count_married,
        )

        kpi3.metric(
            label="A/C Balance ＄",
            value=f"$ {round(balance, 2)} ",
            delta=-round(balance / count_married) * 100,
        )

        # create two columns for charts
        fig_col1, fig_col2,fig_col3 = st.columns(3)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(
                data_frame=df, y="vote_count_new", x="original_language"
            )
            st.write(fig)

        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame=df, x="vote_count_new")
            st.write(fig2)

        with fig_col3:
            st.markdown("### third Chart")
            fig3 = px.line(df, x="runtime", y="vote_count",color='original_language', title='days vs vote')
            st.write(fig3)




        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)