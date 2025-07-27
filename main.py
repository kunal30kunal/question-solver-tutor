import os
import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# ✅ Load environment variable
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if api_key is None:
    st.error("API Key not found. Check your .env file.")
    raise ValueError("API Key not found in environment variables.")

# ✅ Initialize OpenAI client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# ✅ Initialize pyttsx3 engine (TTS)
engine = pyttsx3.init()

# ✅ Streamlit UI
st.set_page_config(page_title="Mini AI Teacher", layout="centered")
st.title("🧠 AI Teacher for Class 5 Students")
st.write("Ask anything you'd like to learn!")

# ✅ User Input
user_input = st.text_input("📚 Ask me anything:")

if user_input:
    with st.spinner("AI is thinking..."):
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[
                    {"role": "system", "content": "You are a kind school teacher explaining things in a simple and fun way for 5th-grade students."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content
            st.success(answer)

            # ✅ Text-to-Speech Output
            if st.button("🔊 Speak"):
                engine.say(answer)
                engine.runAndWait()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
