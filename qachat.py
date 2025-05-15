from dotenv import load_dotenv
load_dotenv() 

import streamlit as st
import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question) 
    return response

st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    st.write(response.text)
    st.session_state['chat_history'].append(("Bot", response.text))

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")