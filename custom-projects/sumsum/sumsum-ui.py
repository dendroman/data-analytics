import streamlit as st
import re
from urllib.parse import urlparse
from sumsum import do_the_thing, get_title

def is_youtube_url(url):
    parsed_url = urlparse(url)
    youtube_domains = ("www.youtube.com", "youtube.com", "youtu.be")

    if parsed_url.netloc not in youtube_domains:
        return False

    if parsed_url.netloc in ("www.youtube.com", "youtube.com") and re.match(r"^/watch\?v=.*", parsed_url.path):
        return True

    if parsed_url.netloc == "youtu.be" and parsed_url.path:
        return True

    return False

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