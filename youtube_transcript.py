from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi as yta

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please set GOOGLE_API_KEY in your .env file.")
    st.stop()
genai.configure(api_key=api_key)

def transcript_details(youtube_link):
    try:
        if "v=" not in youtube_link:
            st.error("Please enter a valid YouTube video link.")
            return None
        video_id = youtube_link.split("v=")[1].split("&")[0]
        transcript_text = yta.get_transcript(video_id)
        l = ""
        for i in transcript_text:
            l += " "+i["text"]
        return l
    except Exception as ex:
        st.error(f"Error fetching transcript: {ex}")
        return None

def generate(transcript_text,prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt+transcript_text)
    return response.text

st.title("Youtube Videos to Detailed Notes Converter")
youtube_link = st.text_input("Enter a like of the Youtube video")
if youtube_link and "v=" in youtube_link:
    video_id = youtube_link.split("v=")[1].split("&")[0]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

prompt="""You will take the transcript text and summarizinng the entire video and providing the important summary in points within 250 or 500 words.Please provide the summary of the youtube video"""  
  
if st.button("Generate Notes"):
    if not youtube_link or "v=" not in youtube_link:
        st.error("Please enter a YouTube video link to get the summary. (or) The link you provided is invalid")
    else:
        transcript_text = transcript_details(youtube_link)
        if transcript_text:
            summary = generate(transcript_text, prompt)
            st.markdown("Detailed Notes: ")
            st.write(summary)