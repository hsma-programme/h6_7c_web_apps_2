import streamlit as st

pg = st.navigation(
    [st.Page("homepage.py", title="Welcome!", icon=":material/add_circle:"),
     st.Page("des.py", title="Run Simulation"),
     ]
     )

pg.run()
