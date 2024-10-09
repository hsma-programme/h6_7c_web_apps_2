import streamlit as st

# Initialise session state variable
if 'walk_in_demand' not in st.session_state:
    st.session_state.walk_in_demand = 150
    st.session_state.calls_demand = 50

pg = st.navigation(
    [st.Page("homepage.py", title="Welcome!", icon=":material/add_circle:"),
     st.Page("lsoa_map.py", title="Set Up Demand", icon=":material/people:"), ## NEW
     st.Page("des.py", title="Run Simulation", icon=":material/public:"),
     ]
     )

pg.run()
