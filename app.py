import streamlit as st
import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Set your Gemini API key
GOOGLE_API_KEY = "AIzaSyBdryy1A2mZ31BRMwMUL1dj5rT7-GUsRRg"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to extract website content
def extract_website_content(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "iframe"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:15000]
    except Exception as e:
        return f"Error fetching website: {e}"

# Function to get response from Gemini
def chat_about_website(url, user_question):
    content = extract_website_content(url)
    prompt = f"Website content:\n{content}\n\nUser question: {user_question}"
    response = model.generate_content(prompt)
    return response.text

# --- ✨ White Background CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    .stApp {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Poppins', sans-serif;
    }

    .title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 20px;
    }

    .stTextInput input {
        background-color: #f2f2f2;
        color: #333333;
        border: 1px solid #cccccc;
    }

    .stButton button {
        background-color: #0052cc;
        color: white;
        font-weight: bold;
        border-radius: 25px;
        padding: 0.5em 2em;
        transition: 0.3s ease;
    }

    .stButton button:hover {
        background-color: #003d99;
        box-shadow: 0 0 10px rgba(0, 82, 204, 0.3);
    }

    .stSpinner {
        color: #0052cc;
    }
    </style>
""", unsafe_allow_html=True)

# --- 🖼️ Logo & Title ---
st.image("tech intelleon.png", width=250)
st.markdown("<div class='title'>TechIntelleon AI Assistant</div>", unsafe_allow_html=True)
st.markdown("### 🤖 Ask anything about the TechIntelleon website")

# --- 🗨️ Chat Interface ---
url = "https://techintelleon.com/"
question = st.text_input("🔍 Enter your question here:")

if st.button("Ask the AI"):
    if question:
        with st.spinner("Thinking... 💭"):
            answer = chat_about_website(url, question)
        st.success("Here’s what I found:")
        st.markdown(f"<div style='background:#f9f9f9;padding:15px;border-radius:10px;border:1px solid #e0e0e0;'>{answer}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a question.")
