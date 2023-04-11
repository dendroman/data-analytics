import openai
import base64
import yt_dlp
import time
import streamlit as st
import os
import glob
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi

# define openai api key and stuff
openai.api_key = (st.secrets["OPENAPI_TOKEN"])

def download_audio(url, output_file='output.mp3'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_file,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_metadata(url):
    ydl_opts = {
        'quiet': True,  # Don't print output to the console
        'no_warnings': True,  # Don't print warnings to the console
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url, download=False)
        return video_info

def transcribe_audio(file_path, sample_rate=16000):
    with open(file_path, "rb") as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")

    response = openai.Audio.create(
        audio=audio_base64,
        model="whisper",
        sample_rate=sample_rate,
        format="mp3",
        transcription_format="text",
    )

    return response['transcription']

def get_sample_rate(file_path):
    audio = AudioSegment.from_file(file_path)
    return audio.frame_rate


def summarize_text(text):
    # OpenAI summary
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a assistant who is excellent of making summaries. You only respond with bullet-points and nothing else."},
            {"role": "user", "content": text + " create a summary of the text above with key insights and bullet points."},
        ]
    )

    print(response)
    print(response.choices[0].message.content)

    return response.choices[0].message.content

def download_audio_from_video(video_url):
    # Download audio
    current_milli_time = int(round(time.time() * 1000))
    output_file = "audio" + str(current_milli_time)
    download_audio(video_url, output_file)

    return output_file

def get_transcript(output_file):
    # OpenAI
    filename = output_file + ".mp3"
    print(filename)
    audio_file= open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    return transcript.text

def concat_transcripts(transcripts):
    concatted_transcript = ""

    for line in transcripts:
        concatted_transcript += line['text'] + " "

    return concatted_transcript.strip()

def get_concatted_transcript(url):
    video_id = url.split('watch?v=')[-1]
    transcripts = get_transcript_by_id(video_id)
    concatted_transcripts = concat_transcripts(transcripts)

    return concatted_transcripts

def do_the_thing(url):
    transcript = get_concatted_transcript(url)

    if transcript is None:
        print("No transcript found, downloading audio from video")
        output_file = download_audio_from_video(url)
        transcript = get_transcript(output_file)
    else:
        print("Found transcript")

    summary = summarize_text(transcript)
    delete_mp3_files()

    return summary

def get_title(url):
    video_info = get_metadata(url)
    print(video_info)

    return video_info['title']

def get_transcript_by_id(video_id, language_code='en'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        return transcript
    except Exception as e:
        print(f"Error getting transcript: {e}")
        return None
    

def delete_mp3_files():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    mp3_files = glob.glob(os.path.join(current_directory, '*.mp3'))

    for mp3_file in mp3_files:
        try:
            os.remove(mp3_file)
            print(f"Deleted {mp3_file}")
        except Exception as e:
            print(f"Error deleting {mp3_file}: {e}")
