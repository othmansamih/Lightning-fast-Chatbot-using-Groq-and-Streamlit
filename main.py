import os
import json
import streamlit as st
from groq import Groq

# loading and setting the groq api key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
os.environ["GROQ_API_KEY"] = config_data["GROQ_API_KEY"]

# client instantiation
client = Groq()

# configuring the page title
st.set_page_config(
    page_title="Llama3.1-70b",
    page_icon="🦙",
    layout="centered"
)

# setting the page title
st.title("Llama3.1-70b")

# intializing the chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# displaying the chat history in case it exists
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# getting the user's prompt
user_prompt = st.chat_input("Ask llama3.1-70b...")
if user_prompt:
    # displaying the user's prompt
    with st.chat_message("user"):
        st.markdown(user_prompt)
    # adding the user's prompt to the chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # performing a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ],
        model="llama3-8b-8192")
    response = chat_completion.choices[0].message.content

    # displaying the model's response
    with st.chat_message("assistant"):
        st.markdown(response)

    # adding the model's response to the chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})