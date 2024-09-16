import streamlit as st
import pandas as pd

############
# NEW      #
############
from des_classes import g, Trial
############
# END NEW  #
############

st.title("Simple One-Step DES")

st.write("In this discrete event simulation, patients arrive")

patient_iat_slider = st.slider("What is the average length of time between patients arriving?",
                               min_value=1, max_value=30, value=5)

patient_consult_slider = st.slider("What is the mean length of time (in minutes) for a consultation?",
                                   min_value = 3, max_value=60, value=6)

num_nurses_slider = st.slider("What is the number of nurses in the system?",
                              min_value=1, max_value=10, value=1)

sim_duration_input = st.number_input("How long should the simulation run for (minutes)?",
                                      min_value=60, max_value=480, value=480)

num_runs_input = st.number_input("How many runs of the simulation should be done?",
                                  min_value=1, max_value=100, value=100)

############
# NEW      #
############
g.patient_inter = patient_iat_slider
g.mean_n_consult_time = patient_consult_slider
g.number_of_nurses = num_nurses_slider
g.sim_duration = sim_duration_input
g.number_of_runs = num_runs_input

############
# END NEW  #
############

# A user must press a streamlit button to run the model
button_run_pressed = st.button("Run simulation")

if button_run_pressed:
    with st.spinner('Simulating the system...'):
        results_df = Trial().run_trial()

        st.dataframe(results_df)
