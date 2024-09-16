import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Caching Example - Without Caching (for speed/responsiveness comparison)")

st.write(
    """
    While the improvement in speed with caching isn't as apparent in this example as it is in
    some other cases (where the dataset being loaded in is bigger), you will hopefully notice
    that the example *with* caching is a bit more responsive - the new graph will appear a bit
    quicker and you don't see the 'loading' message appearing at the top of the screen
    quite so much.
    """
)

# Here we just load in our data in the usual way
# But note that because we're NOT caching the data, a few things are true:
# - The dataset will be reloaded EVERY time something changes in the app (e.g. a value
#   is chosen from a dropdown)
# - The dataset will be loaded in separately for every single user, which can cause you
#   to start exceeding memory limits on your hosting if you have lots of
#   simultaneous users
athlete_statistics = pd.read_csv("athlete_details_eventwise.csv")


# The code that follows
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
