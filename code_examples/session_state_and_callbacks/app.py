import streamlit as st

pg = st.navigation([
        st.Page("page_1.py", title="Start here!"),
        st.Page("page_2.py", title="Now go here")
     ])

pg.run()
