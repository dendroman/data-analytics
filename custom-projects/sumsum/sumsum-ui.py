import streamlit as st
from sumsum import do_the_thing, get_title

st.title("Hello, World!")

st.write("This is SumSum, a audio/video summarizer!")

st.write("Enter a YouTube URL to get started!")

url = st.text_input("URL")

if st.button("Summarize"):
    st.write("Summarizing " + get_title(url) + "")
    st.write(do_the_thing(url))

st.write("Made by @dendroman")