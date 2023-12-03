import openai
import streamlit as st

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = st.text_area("Tell me about your important person", height=200)
openai.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.6,
                top_p = 0.6,
                max_tokens = 450,
                messages=[
                    {"role": "system", "content": f"You are flowers reccomendation bot. You will help users to find the best flowers for their important person."},
                    {"role": "user", "content": f"You will help users to find the best flowers from {prompt}."},
                    ]
                )
            
