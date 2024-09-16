import streamlit as st
from palmerpenguins import load_penguins
import plotly.express as px
import time

st.title("Example Without Partial Reruns/no use of @st.fragment")

penguins = load_penguins()

app_column_1, app_column_2 = st.columns(2)

with app_column_1:
    # This just pauses the app to make the effect of the use of @st.fragment a bit more obvious
    # You don't need to use this in your own apps!
    time.sleep(3)
    # Put our inputs and outputs into the first column
    species = st.selectbox("Select a penguin species to filter by", ["Adelie", "Gentoo", "Chinstrap"])
    filtered_df_species = penguins[penguins['species'] == species]
    st.plotly_chart(px.bar(filtered_df_species['sex'].value_counts(), y='count'))

with app_column_2:
    # Again, this just pauses the app to make the effect of the use of @st.fragment a bit more obvious
    # You don't need to use this in your own apps!
    time.sleep(3)

    # Here we put a second set of inputs and outputs into our app, this time in the second column
    axis_options = ['bill_length_mm', 'bill_depth_mm',
                    'flipper_length_mm', 'body_mass_g']

    col_1 = st.selectbox("Select the column to use for the x axis", axis_options)
    axis_options.remove(col_1)

    col_2 = st.selectbox("Select the column to use for the y axis", axis_options)

    color_factor = st.selectbox("Select the column to colour the chart by",
    ["species", "sex", "island"])

    fig = px.scatter(penguins, x=col_1, y=col_2, color=color_factor,
    title=f"Penguins Dataset - {col_1} vs {col_2}, coloured by {color_factor}")

    st.plotly_chart(fig)
