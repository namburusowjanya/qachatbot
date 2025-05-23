from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image as pi
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input_text,pdf_content,prompt):
    model=genai.GenerativeModel("models/gemini-1.5-flash")
    response=model.generate_content([
        {"text":input_text},
        pdf_content[0],
        {"text":prompt}
    ])
    return response.text

def pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images=pi.convert_from_bytes(uploaded_file.read())
        first=images[0]
        img=io.BytesIO()
        first.save(img,format='JPEG')
        img=img.getvalue()
        pdf_parts=[
            {
                "inline_data":{
                    "mime_type":"image/jpeg",
                    "data":base64.b64encode(img).decode()
                }
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file is uploaded")

st.set_page_config(page_title="ATS Resume :")
st.header("Application Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload a file(resume-PDF)")

sub1=st.button("Tell me about the resue")
sub2=st.button("Persentage Mathch of the resume to post")
sub3=st.button("How can I improvise my skills")

prompt1="""
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""
prompt2="""
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. 
Give the percentage of match, list missing keywords, and provide final thoughts.
"""
prompt3="""
You are an expert ATS scanner. Review the resume and job description, and suggest how the candidate can improve their skills 
to match the job requirements better. Include technologies or certifications that would help.
"""

if uploaded_file is not None:
    pdf_content=pdf_setup(uploaded_file)
    if sub1:
        st.write(get_response(input_text,pdf_content,prompt1))
    elif sub2:
        st.write(get_response(input_text,pdf_content,prompt2))
    elif sub3:
        st.write(get_response(input_text,pdf_content,prompt3))
else:
    st.warning("Please upload a PDF resume file to proceed.")
