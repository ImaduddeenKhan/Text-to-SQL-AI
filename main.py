import os
import sqlite3
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found! Make sure it's set in your .env file.")

# ✅ FIXED: Direct emoji instead of Unicode escape
st.set_page_config(page_title="AI Chat SQL", page_icon="🌍", layout="wide")

# Custom CSS for improved UI
st.markdown("""
    <style>
        body { background-color: #000014; color: white; }
        .stApp { background-color: #000014; }
        .title { text-align: center; font-size: 3.2rem; font-weight: bold; color: #00f2ff; margin-bottom: 5px; font-family: 'Arial', sans-serif; }
        .subtitle { text-align: center; font-size: 1.5rem; opacity: 0.9; color: #00e6ff; margin-bottom: 30px; font-family: 'Arial', sans-serif; }
        .query-box { background-color: #12172b; padding: 15px; border-radius: 10px; font-family: monospace; color: #ffffff; }
        .result-box { background-color: #10172d; padding: 15px; border-radius: 10px; margin-top: 10px; color: #ffffff; }
        .ask-button { background-color: #00d9ff; color: white; font-weight: bold; padding: 12px 20px; border-radius: 8px; transition: 0.3s; font-size: 1.1rem; }
        .ask-button:hover { background-color: #00aaff; }
        .toggle-button { background-color: #ff914d; padding: 10px 18px; border-radius: 8px; font-size: 1rem; font-weight: bold; color: white; border: none; cursor: pointer; }
        .toggle-button:hover { background-color: #ff7b2e; }
        .glowing-lines { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: url('https://i.imgur.com/NM1rfGn.png'); opacity: 0.2; }
    </style>
""", unsafe_allow_html=True)

# Background animation effect
st.markdown('<div class="glowing-lines"></div>', unsafe_allow_html=True)


# Function to convert user query to SQL
def get_sql_query(user_query):
    prompt_template = ChatPromptTemplate.from_template("""
        You are an expert at converting English questions into SQL queries.
        The database STUDENT has columns: NAME, COURSE, SECTION, MARKS.

        Example 1: "How many records exist?"  
        → Query: SELECT COUNT(*) FROM STUDENT;

        Example 2: "Show all students in Data Science."  
        → Query: SELECT * FROM STUDENT WHERE COURSE = 'Data Science';

        Ensure output is valid SQL, without "sql" keyword or triple backticks.
        Convert this question to SQL: {user_query}
    """)

    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-8b-8192")
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"user_query": user_query})

# Function to execute SQL query
def return_sql_response(sql_query):
    with sqlite3.connect("student.db") as conn:
        return conn.execute(sql_query).fetchall()


# UI Elements
st.markdown('<p class="title">🌍 AI-Powered SQL Chat</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ask anything, and I will fetch data for you!</p>', unsafe_allow_html=True)

user_query = st.text_input("💬 Type your question:", placeholder="e.g., Show all students with marks above 80")

if st.button("Ask AI", key="ask_button", help="Click to get SQL Query & Data", use_container_width=True):
    sql_query = get_sql_query(user_query)

    # Toggle state persistence
    toggle_state = st.session_state.get("toggle_sql", False)
    if st.toggle("🔍 Show SQL Query", key="toggle_sql", value=toggle_state):
        st.markdown('<p class="query-box">📎 SQL Query Generated:</p>', unsafe_allow_html=True)
        st.code(sql_query, language="sql")

    retrieved_data = return_sql_response(sql_query)

    st.markdown('<p class="query-box">📊 Query Results:</p>', unsafe_allow_html=True)
    for row in retrieved_data:
        st.markdown(f'<div class="result-box">{row}</div>', unsafe_allow_html=True)