import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Caching Example - With Caching")

st.write(
    """
    While the improvement in speed with caching isn't as apparent in this example as it is in
    some other cases (where the dataset being loaded in is bigger), you will hopefully notice
    that the example *with* caching is a bit more responsive - the new graph will appear a bit
    quicker and you don't see the 'loading' message appearing at the top of the screen
    quite so much.
    """
)

# To use streamlit's caching features, we need to do three main things:
# 1. Add the @st.cache_data decorator
# 2. Directly below this (i.e. no blank line first), define a function that loads in your
#    dataset (from a relative path or from the web - either will work!) and make sure that
#    it *returns* your dataset
@st.cache_data
def load_data():
    return pd.read_csv("athlete_details_eventwise.csv")

# 3. Finally, call this function and save the output to a variable with a name of your choosing
# You can then use this like a standard dataframe throughout the rest of your script - Streamlit
# handles the rest
athlete_statistics = load_data()

selected_sport = st.selectbox("Select a sport",
                              athlete_statistics["Sport"].drop_duplicates().tolist())

athlete_statistics_sport = athlete_statistics[athlete_statistics["Sport"] == selected_sport]

events_per_year_by_sport = (
    athlete_statistics_sport[['Year', 'Event']]
    .drop_duplicates()
    .value_counts(['Year'])
    .reset_index()
)

st.plotly_chart(
    px.line(events_per_year_by_sport.sort_values("Year"),
            x="Year", y="count",
            markers=True,
            title=f"{selected_sport} Events Per Olympics",
            range_x=[athlete_statistics.Year.min(), athlete_statistics.Year.max()])
)

st.dataframe(
    events_per_year_by_sport
)
