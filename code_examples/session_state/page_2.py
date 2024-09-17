import streamlit as st

if 'your_number' not in st.session_state:
        st.session_state.your_number = None
if 'button_click_count' not in st.session_state:
    st.session_state.button_click_count = 0

if st.session_state.your_number is None:
    st.write("Go back to the previous page and enter a number!")
else:
    st.write(f"I remember your number! It's {st.session_state.your_number}")

st.divider()

st.write(f"You clicked the button on the other page {st.session_state.button_click_count} times")

st.divider()

st.write("Your name? Let me look up what your name is.")

try:
    st.write(name_input)
except:
    st.write("I don't seem to remember your name...")
