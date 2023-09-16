import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage,AIMessage,SystemMessage
import time

if "noAPIKey" not in st.session_state:
    st.session_state.noAPIKey = True
    st.session_state.messages = []

st.sidebar.text_input("Enter your OpenAI API Key", key = "OPENAI_API_KEY")

if len(st.session_state.OPENAI_API_KEY) == 0:
    st.chat_input("Please enter your API Key before using the Chatbot", disabled=st.session_state.noAPIKey)
    st.write("fuck")

else:
    st.session_state.noAPIKey = False
    st.chat_input("Enter your message", key="userInput", disabled=st.session_state.noAPIKey)
    st.write(st.session_state.userInput)
time.sleep(5)

# st.session_state.messages.append(HumanMessage(st.session_state.userInput))
