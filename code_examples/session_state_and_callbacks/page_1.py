import streamlit as st

if 'your_number' not in st.session_state:
    st.session_state.your_number = None
if 'button_click_count' not in st.session_state:
    st.session_state.button_click_count = 0
if 'the_final_answer' not in st.session_state:
    st.session_state.the_final_answer = None

st.title("Session State Example")

st.session_state.your_number = st.number_input(
    "Pick a number between 1 and 100",
    min_value=1, max_value=100, value=None
    )

if st.session_state.the_final_answer is None:
    "Enter a number and then go to the next page to calculate the final answer"
else:
    f"Your answer is {st.session_state.the_final_answer} - but what was the question?"

st.divider()

name_input = st.text_input("Enter Your Name")

st.divider()

def button_action():
    st.session_state.button_click_count += 1

add_number_button = st.button("Click me!",
                              on_click=button_action)

st.write(f"You've clicked the button {st.session_state.button_click_count} times")
