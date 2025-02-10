import streamlit as st

st.title("Hello World!!!!")
st.text("this is some more text", help="this is a tooltip")

selected_date = st.date_input("Choose a date", "today")
st.text(selected_date)