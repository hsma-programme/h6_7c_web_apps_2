import streamlit as st
import geopandas
import pandas as pd
import folium
import random
from streamlit_folium import st_folium
import time

st.set_page_config(layout="wide")

st.logo("hsma_logo.png")

# Here I'm initialising a session state variable that will be used to store the selected regions.
# We only use this on this page - but it will stop the selected values from resetting if the user
# moves away from and then back to this page.
if 'selected_regions' not in st.session_state:
    st.session_state.selected_regions = ['Exeter']

# While we will set some more session state variables here, I have opted to initialise them in the
# app.py file instead of in here. This is a neat trick in multipage apps that prevents you from
# having to repeat the initialisation code in multiple places.
# Take a look at the app.py file for full details!
# If I had initialised them here, I would have used the code
#
# if 'walk_in_demand' not in st.session_state:
#     st.session_state.walk_in_demand = 150
# if 'calls_demand' not in st.session_state:
#     st.session_state.calls_demand = 50

# Import custom css for using a Google font
with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.title("Clinic Demand Estimator")

st.warning("This is just a sample app for demonstration purposes!")

# Here I have cached and processed the data all in one go
# An alternative would have been
#
# @st.cache_data
# def load_map_data():
#    return geopandas.read_file("lsoa_demand_demographics.geojson")
#
# lsoa_demographics = load_map_data()
#
# and this would have been absolutely fine!
# However, as the modifications to include the region and tidy up the dataframe for display also
# only need to run once, it's a bit more efficient to also include them in our cached function
# We could also split that into it's own cached function, but it involves a bit more passing
# around of variables to function which is just a bit more faff
@st.cache_data
def load_map_data():
    lsoa_demographics = geopandas.read_file("lsoa_demand_demographics.geojson")
    lsoa_demographics["Region"] = lsoa_demographics["LSOA21NM"].str.replace("( \d{3})\w", "", regex=True).str.strip()

    new_col = True

    df_display = lsoa_demographics.drop(
        columns = ["BNG_E", "BNG_N", "LONG", "LAT", "GlobalID", "geometry"]
    )

    df_display.insert(loc=2, column='Include', value=new_col)

    return lsoa_demographics, df_display

# Notice that here we have run load_map_data() within the fragment.
# This ensures that the lsoa_demographics and df_display variables are available to the rest of
# the code in the fragment
# The fragment can't access variables that are defined outside of the fragment, so you will need to
# pass them in to the function or define them within the function (as we've done here)
@st.fragment
def get_map():

    lsoa_demographics, df_display = load_map_data()

    st.session_state.selected_regions = st.multiselect(
        "Select Regions to Include",
        lsoa_demographics["Region"].drop_duplicates().sort_values().tolist(),
        default=st.session_state.selected_regions
    )

    edited_df = st.data_editor(
        df_display[df_display["Region"].isin(st.session_state.selected_regions)]
        )

    lsoa_demographics = pd.merge(
        lsoa_demographics,
        edited_df[edited_df["Include"] == True][["LSOA21CD"]],
        how="inner"
        )

    demand_calls = lsoa_demographics['Projected Average Daily Demand'].sum()*0.2
    demand_walkins = lsoa_demographics['Projected Average Daily Demand'].sum()*0.8

    # Here we are storing the demand and
    st.session_state.calls_demand = demand_calls
    st.session_state.walk_in_demand = demand_walkins

    iat_calls = 480/(lsoa_demographics['Projected Average Daily Demand'].sum()*0.2)
    iat_walkins = 480/(lsoa_demographics['Projected Average Daily Demand'].sum()*0.8)

    st.write(f"Projected Daily Demand - Calls: {demand_calls:.1f}")
    st.write(f"Average IAT: {iat_calls:.1f} minutes (assuming 480 minute day)")

    st.write(f"Projected Daily Demand - Walk-ins: {demand_walkins:.1f}")
    st.write(f"Average IAT - Walk-ins: {iat_walkins:.1f} minutes (assuming 480 minute day)")

    #create base map
    demand_demographic_map_interactive = folium.Map(
        location=[50.71671, -3.50668],
        zoom_start=9,
        tiles='cartodbpositron'
        )

    # create and add choropleth map
    choropleth = folium.Choropleth(
        geo_data=lsoa_demographics, # dataframe with geometry in it
        data=lsoa_demographics, # dataframe with data in - may be the same dataframe or a different one
        columns=['LSOA21CD', 'Projected Average Daily Demand'], # [key (field for geometry), field to plot]
        key_on='feature.properties.LSOA21CD',
        fill_color='OrRd',
        fill_opacity=0.4,
        line_weight=0.3,
        legend_name='Projected Average Daily Demand',
        highlight=True, # highlight the LSOA shape when mouse pointer enters it
        smooth_factor=0
        )

    choropleth = choropleth.add_to(demand_demographic_map_interactive)

    choropleth = choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ['LSOA21CD', 'Projected Average Daily Demand'],
            labels=True
            )
    )

    st_folium(demand_demographic_map_interactive,
            use_container_width=True)

# Here we call our fragment function to get it to display on the page
get_map()


# Notice that we haven't put the long-running calculation in a fragment
# The map is the thing that will change when a user interacts with the page - so that's
# what we want to wrap in a fragment! This will ensure that when the user changes the regions
# selected, the map updates - but other parts of the page don't. This means that the
# long-running calculation won't rerun even though it is not itself wrapped in a fragment.
# It will only rerun if users refresh the page or move to a different page in the app and then
# come back here.
st.divider()

st.subheader("Complex Calculation Unrelated to the Map!")

st.write("Long-running calculation being calculated...")

time.sleep(3)

st.write("Long-running calculation complete!")

st.write(f"The answer is {random.randint(100, 500)}")
