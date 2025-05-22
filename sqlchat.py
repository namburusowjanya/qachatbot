from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(question, prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content([prompt, question])
    return response.text.strip()

def read_tab(sql, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    return rows

prompt = """
You are an expert in converting English questions to SQL queries.
The SQLite database has a table named STUDENT with the following columns: NAME, BRANCH, SECTION, MARKS.

Examples:
1. "How many student records are there?" → SELECT COUNT(*) FROM STUDENT;
2. "List all students in the IT branch" → SELECT * FROM STUDENT WHERE BRANCH = "IT";
3. "Show students who scored more than 80 marks" → SELECT * FROM STUDENT WHERE MARKS > 80;

Do not include triple quotes or the word "sql" in the output.
Only return the SQL query.
"""

st.set_page_config(page_title="I can Retrieve any SQL query")
st.header("Gemini to Retrieve SQL data.")

question = st.text_input("Enter your question:", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_response(question, prompt)
    st.text(f"Generated SQL: {response}")
    try:
        data = read_tab(response, "student.db")
        st.subheader("Query Results:")
        if data:
            for row in data:
                st.write(row)
        else:
            st.info("No results found.")
    except Exception as e:
        st.error(f"Error executing SQL: {e}")
