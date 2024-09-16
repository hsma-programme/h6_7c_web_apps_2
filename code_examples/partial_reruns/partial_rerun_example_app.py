import streamlit as st
from palmerpenguins import load_penguins
import plotly.express as px
import time

st.title("Example *With* Partial Reruns/@st.fragment")

# Let's load in our penguins dataframe. Here, it's a dataset that's actually loaded in directly
# from a function in a package, but everything in this example would be the same regardless of
# where your dataset is coming from.
penguins = load_penguins()

# Let's set up two columns for our inputs and outputs to be placed within.
app_column_1, app_column_2 = st.columns(2)

# We use the @st.fragment decorator on its own line first
# Then, instead of just creating the inputs and outputs straight in the app, we need to wrap them
# in a function. This function doesn’t need to return anything, and we can call it
# whatever we like.
# Note that there is no blank line between the @st.fragment() decorator and the function definition.
# Here, we’ve counted the select dropdown for species, the pandas dataframe filter action,
# and the creation of the barplot figure as being a single thing we want to rerun
# when any element within those three changes in a way that would trigger a rerun usually.
@st.fragment
def penguin_barchart():
    # This just pauses the app to make the effect of the use of @st.fragment a bit more obvious
    # You don't need to use this in your own apps!
    time.sleep(3)
    # Within this function we define our input - here a selection dropdown of three penguin species
    species = st.selectbox("Select a penguin species to filter by", ["Adelie", "Gentoo", "Chinstrap"])
    # We then make a new dataframe by filtering out our existing dataframes
    filtered_df_species = penguins[penguins['species'] == species]
    # Finally we make our plotly chart and wrap it in the st.plotly_chart() function to make sure it
    # will be displayed in the app
    st.plotly_chart(px.bar(filtered_df_species['sex'].value_counts(), y='count'))
    # Notice how we don't *return* anything from this function - we just write everything like normal
    # streamlit code that just happens to be indented by one level!

# We then repeat this for our next function.
@st.fragment
def penguin_scatterplot():
    axis_options = ['bill_length_mm', 'bill_depth_mm',
       'flipper_length_mm', 'body_mass_g']
    time.sleep(3)
    col_1 = st.selectbox("Select the column to use for the x axis", axis_options)
    axis_options.remove(col_1)

    col_2 = st.selectbox("Select the column to use for the y axis", axis_options)

    color_factor = st.selectbox("Select the column to colour the chart by",
    ["species", "sex", "island"])

    fig = px.scatter(
        penguins,
        x=col_1,
        y=col_2,
        color=color_factor,
        title=f"Penguins Dataset - {col_1} vs {col_2}, coloured by {color_factor}")

    st.plotly_chart(fig)

# Now we just need to call the two functions we've created.
#
#  Using the with notation with the first column we created, we then call our first function.
# (note that you don't have to put it in a column! You could just call the function, but here
# we're putting them in columns because it's easier to see the way the fragment decorator
# is working when running the app if the two bits that rerun separately are side-by-side)
with app_column_1:
   penguin_barchart()

# We then repeat this for the second column and second function.
with app_column_2:
   penguin_scatterplot()
