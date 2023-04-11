import streamlit as st
from sumsum import do_the_thing, get_title, is_youtube_url


st.markdown("## SumSum - A YouTube Summarizer :movie_camera:")
st.write("Enter a YouTube URL to get started!")

url = st.text_input("URL")

if st.button("Summarize"):
    if is_youtube_url(url):
        st.write("Summarizing " + get_title(url) + "")
        st.write(do_the_thing(url))
    else:
        st.error("Invalid YouTube URL. Please enter a valid YouTube URL.")

st.markdown("Made by [@dendroman](https://github.com/dendroman/)")