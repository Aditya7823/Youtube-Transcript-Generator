import streamlit as st

# Title of the app
st.title('Hello, Streamlit!')

# Interactive input
name = st.text_input("What's your name?", "John Doe")
st.write(f"Hello, {name}!")

# Plotting a chart
st.line_chart([1, 2, 3, 4, 5])
