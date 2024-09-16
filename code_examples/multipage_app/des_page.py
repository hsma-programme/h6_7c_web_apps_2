import streamlit as st
import simpy
import random
import pandas as pd

st.title("Simple One-Step DES")

# Class to store global parameter values
# class g:
#     patient_inter = 5
#     mean_n_consult_time = 6
#     number_of_nurses = 1
#     sim_duration = 120
#     number_of_runs = 5

patient_iat_slider = st.slider("What is the average length of time between patients arriving?",
                               min_value=1, max_value=30, value=5)

patient_consult_slider = st.slider("What is the mean length of time (in minutes) for a consultation?",
                                   min_value = 3, max_value=60, value=6)

num_nurses_slider = st.slider("What is the number of nurses in the system?",
                              min_value=1, max_value=10, value=1)

sim_duration_input = st.number_input("How long should the simulation run for (minutes)?",
                                      min_value=60, max_value=480, value=480) ## CHANGED - LONGER DEFAULT

num_runs_input = st.number_input("How many runs of the simulation should be done?",
                                  min_value=1, max_value=100, value=100) ## CHANGED - HIGHER DEFAULT

class g:
    patient_inter = patient_iat_slider
    mean_n_consult_time = patient_consult_slider
    number_of_nurses = num_nurses_slider
    sim_duration = sim_duration_input
    number_of_runs = num_runs_input

# Class representing patients coming in to the clinic.
# Here, patients have two attributes that they carry with them -
# their ID, and the amount of time they spent queuing for the nurse.
# The ID is passed in when a new patient is created.
class Patient:
    def __init__(self, p_id):
        self.id = p_id
        self.q_time_nurse = 0

# Class representing our model of the clinic.
class Model:
    # Constructor to set up the model for a run.  We pass in a run number when
    # we create a new model.
    def __init__(self, run_number):
        # Create a SimPy environment in which everything will live
        self.env = simpy.Environment()

        # Create a patient counter (which we'll use as a patient ID)
        self.patient_counter = 0

        # Create a SimPy resource to represent a nurse, that will live in the
        # environment created above.  The number of this resource we have is
        # specified by the capacity, and we grab this value from our g class.
        self.nurse = simpy.Resource(self.env, capacity=g.number_of_nurses)

        # Store the passed in run number
        self.run_number = run_number

        # Create a new Pandas DataFrame that will store some results against
        # the patient ID (which we'll use as the index).
        self.results_df = pd.DataFrame()
        self.results_df["Patient ID"] = [1]
        self.results_df["Q Time Nurse"] = [0.0]
        self.results_df["Time with Nurse"] = [0.0]
        self.results_df.set_index("Patient ID", inplace=True)

        # Create an attribute to store the mean queuing time for the nurse
        # across this run of the model
        self.mean_q_time_nurse = 0

    # A generator function that represents the DES generator for patient
    # arrivals
    def generator_patient_arrivals(self):
        # We use an infinite loop here to keep doing this indefinitely whilst
        # the simulation runs
        while True:
            # Increment the patient counter by 1 (this means our first patient
            # will have an ID of 1)
            self.patient_counter += 1

            # Create a new patient - an instance of the Patient Class we
            # defined above.  Remember, we pass in the ID when creating a
            # patient - so here we pass the patient counter to use as the ID.
            p = Patient(self.patient_counter)

            # Tell SimPy to start up the attend_clinic generator function with
            # this patient (the generator function that will model the
            # patient's journey through the system)
            self.env.process(self.attend_clinic(p))

            # Randomly sample the time to the next patient arriving.  Here, we
            # sample from an exponential distribution (common for inter-arrival
            # times), and pass in a lambda value of 1 / mean.  The mean
            # inter-arrival time is stored in the g class.
            sampled_inter = random.expovariate(1.0 / g.patient_inter)

            # Freeze this instance of this function in place until the
            # inter-arrival time we sampled above has elapsed.
            yield self.env.timeout(sampled_inter)

    # A generator function that represents the pathway for a patient going
    # through the clinic.
    def attend_clinic(self, patient):
        # Record the time the patient started queuing for a nurse
        start_q_nurse = self.env.now

        # Request a nurse resource, and do all of the following block of code with
        # that nurse resource held in place (and therefore not usable by another patient)
        with self.nurse.request() as req:
            # Freeze the function until the request for a nurse can be met.
            # The patient is currently queuing.
            yield req

            # When we get to this bit of code, control has been passed back to the generator
            # function, and therefore the request for a nurse has been met.
            # We now have the nurse, and have stopped queuing, so we can record the current time
            # as the time we finished queuing.
            end_q_nurse = self.env.now

            # Calculate the time this patient was queuing for the nurse, and
            # record it in the patient's attribute for this.
            patient.q_time_nurse = end_q_nurse - start_q_nurse

            # Now we'll randomly sample the time this patient with the nurse.
            # Here, we use an Exponential distribution for simplicity
            # As with sampling the inter-arrival times, we grab the mean from the g class,
            # and pass in 1 / mean as the lambda value.
            sampled_nurse_act_time = random.expovariate(1.0 /
                                                        g.mean_n_consult_time)

            # Here we'll store the queuing time for the nurse and the sampled
            # time to spend with the nurse in the results DataFrame against the
            # ID for this patient.
            self.results_df.at[patient.id, "Q Time Nurse"] = (
                patient.q_time_nurse)
            self.results_df.at[patient.id, "Time with Nurse"] = (
                sampled_nurse_act_time)

            # Freeze this function in place for the activity time we sampled
            # above.  This is the patient spending time with the nurse.
            yield self.env.timeout(sampled_nurse_act_time)

            # When the time above elapses, the generator function will return
            # here.  As there's nothing more that we've written, the function
            # will simply end.  This is a sink.  We could choose to add
            # something here if we wanted to record something - e.g. a counter
            # for number of patients that left, recording something about the
            # patients that left at a particular sink etc.

    def calculate_run_results(self):
        # Take the mean of the queuing times for the nurse across patients in
        # this run of the model.
        self.mean_q_time_nurse = self.results_df["Q Time Nurse"].mean()

    # The run method starts up the DES entity generators, runs the simulation,
    # and in turns calls anything we need to generate results for the run
    def run(self):
        # Start up our DES entity generators that create new patients.
        # We've only got one in this model, but we'd need
        # to do this for each one if we had multiple generators.
        self.env.process(self.generator_patient_arrivals())

        # Run the model for the duration specified in g class
        self.env.run(until=g.sim_duration)

        # Now the simulation run has finished, call the method that calculates
        # run results
        self.calculate_run_results()

# Class representing a Trial for our simulation - a batch of simulation runs.
class Trial:
    # The constructor sets up a pandas dataframe that will store the key
    # results from each run (just the mean queuing time for the nurse here)
    # against run number, with run number as the index.
    def  __init__(self):
        self.df_trial_results = pd.DataFrame()
        self.df_trial_results["Run Number"] = [0]
        self.df_trial_results["Mean Q Time Nurse"] = [0.0]
        self.df_trial_results.set_index("Run Number", inplace=True)

    # Method to run a trial
    def run_trial(self):
        # Run the simulation for the number of runs specified in g class.
        # For each run, we create a new instance of the Model class and call its
        # run method.  Once the run has completed, we grab out the stored run results
        # (just mean queuing time here) and store it against the run number
        # in the trial results dataframe.
        for run in range(g.number_of_runs):
            my_model = Model(run)
            my_model.run()

            self.df_trial_results.loc[run] = [my_model.mean_q_time_nurse]

        # Once the trial (ie all runs) has completed, return the final results
        return self.df_trial_results

############
# NEW      #
############
# A user must press a streamlit button to run the model
button_run_pressed = st.button("Run simulation")

if button_run_pressed:
    with st.spinner('Simulating the system...'):
        results_df = Trial().run_trial()

        st.dataframe(results_df)
############
# END NEW  #
############
