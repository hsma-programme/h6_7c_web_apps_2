import streamlit as st
import geopandas
import pandas as pd
import folium
import random
from streamlit_folium import st_folium
import time

st.set_page_config(layout="wide")

st.title("Clinic Demand Estimator")

lsoa_demographics = geopandas.read_file("lsoa_demand_demographics.geojson")
lsoa_demographics["Region"] = lsoa_demographics["LSOA21NM"].str.replace("( \d{3})\w", "", regex=True).str.strip()

new_col = True

df_display = lsoa_demographics.drop(
    columns = ["BNG_E", "BNG_N", "LONG", "LAT", "GlobalID", "geometry"]
)

df_display.insert(loc=2, column='Include', value=new_col)

selected_regions = st.multiselect(
    "Select Regions to Include",
    lsoa_demographics["Region"].drop_duplicates().sort_values().tolist(),
    default=["Exeter"]
)

edited_df = st.data_editor(
    df_display[df_display["Region"].isin(selected_regions)]
    )

lsoa_demographics = pd.merge(
    lsoa_demographics,
    edited_df[edited_df["Include"] == True][["LSOA21CD"]],
    how="inner"
    )

demand_calls = lsoa_demographics['Projected Average Daily Demand'].sum()*0.2
demand_walkins = lsoa_demographics['Projected Average Daily Demand'].sum()*0.8

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



st.divider()

st.subheader("Complex Calculation Unrelated to the Map!")

st.write("Long-running calculation being calculated...")

time.sleep(10)

st.write("Long-running calculation complete!")

st.write(f"The answer is {random.randint(100, 500)}")
