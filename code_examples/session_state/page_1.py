import streamlit as st

if 'your_number' not in st.session_state:
    st.session_state.your_number = None
if 'button_click_count' not in st.session_state:
    st.session_state.button_click_count = 0

st.title("Session State Example")

st.session_state.your_number = st.number_input(
    "Pick a number between 1 and 100",
    min_value=1, max_value=100, value=None
    )

name_input = st.text_input("Enter Your Name")

def button_action():
    st.session_state.button_click_count += 1

add_number_button = st.button("Click me!",
                              on_click=button_action)

st.write(f"You've clicked the button {st.session_state.button_click_count} times")
