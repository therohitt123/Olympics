import pandas as pd
import streamlit as st
import plotly.express as px

import preprocesser
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# ================= LOAD DATA =================
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocesser.preprocess(df, region_df)


# ================= SIDEBAR =================
st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://www.nicepng.com/png/detail/177-1776002_olympic-logo-with-sports-summer-olympic-games.png",
                     )
user_menu = st.sidebar.radio(
    "Select an option:",
    (
        "Medal Tally",
        "Overall Analysis",
        "Country-wise Analysis",
        "Athlete-wise Analysis"
    )
)


# ================= MEDAL TALLY =================
if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")

    years, countries = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Medal Tally")
    elif selected_year != "Overall" and selected_country == "Overall":
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == "Overall" and selected_country != "Overall":
        st.title(f"Medal Tally of {selected_country} in Olympics")
    else:
        st.title(f"Medal Tally of {selected_country} in {selected_year} Olympics")

    st.dataframe(medal_tally)


# ================= OVERALL ANALYSIS =================
elif user_menu == "Overall Analysis":
    st.title("Overall Analysis")

    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.subheader("Top Statistics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Editions", editions)
    col2.metric("Hosts", cities)
    col3.metric("Sports", sports)

    col1, col2, col3 = st.columns(3)
    col1.metric("Events", events)
    col2.metric("Nations", nations)
    col3.metric("Athletes", athletes)

    # -------- Nations over time --------
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(
        nations_over_time,
        x='Edition',
        y='region',
        markers=True
    )
    st.subheader("Participating Nations Over the Years")
    st.plotly_chart(fig, use_container_width=True)

    # -------- Events over time --------
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(
        events_over_time,
        x='Edition',
        y='Event',
        markers=True
    )
    st.subheader("Events Over the Years")
    st.plotly_chart(fig, use_container_width=True)
    # -------- Athletes over time --------
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title("Athletes Over the Years")
    st.plotly_chart(fig)

    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(
            index='Sport',
            columns='Year',
            values='Event',
            aggfunc='count'
        ).fillna(0).astype(int),
        annot=True
    )
    st.pyplot(fig)


    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()

    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox("Select a Sport", sport_list)
    x= helper.most_successful(df, selected_sport)
    st.dataframe(x)

# ================= PLACEHOLDERS =================
if user_menu == "Country-wise Analysis":
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(f"{selected_country} Medal Tally Over the Years")
    st.plotly_chart(fig)

    st.title(f"{selected_country} Excels in Following Sports")
    heatmap_df = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(heatmap_df, annot=True)
    st.pyplot(fig)

    st.title(f"Top 10 Athletes of {selected_country}")
    top10_df = helper.most_successful(df, selected_country)
    st.table(top10_df)


elif user_menu == "Athlete-wise Analysis":
    st.title("Athlete-wise Analysis")
   
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


    x = []
    name = []
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
        'Art Competitions', 'Handball', 'Weightlifting',
        'Wrestling', 'Water Polo', 'Hockey', 'Rowing',
        'Boxing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports")
    st.plotly_chart(fig)



    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Weight vs Height")
    selected_sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weght_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(
        temp_df['Weight'],
        temp_df['Height'],
        hue=temp_df['Medal'],
        style=temp_df['Sex'],
        s=60
    )
    st.pyplot(fig)

    st.title("Men vs Women Participation Over the Years")
    final = helper.men_women_participation(df)
    fig = px.line(
        final,
        x='Year',
        y=['Male', 'Female']
    )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)