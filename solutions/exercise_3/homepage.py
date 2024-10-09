import streamlit as st

st.logo("../../exercises/exercise_2/hsma_logo.png")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.title("Clinic Simulation App")

st.write("Welcome to the clinic simulation app!")

st.write("Head to the 'Run Simulation' page to get started.")
