### Stable but can not develop on Web

import streamlit as st
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage,AIMessage,SystemMessage
import time

def is_key_valid():
    st.session_state.ObtainedValidKey = True

def obtain_valid_API_Key():
    # slide Bar
    with st.sidebar:
        st.markdown("<h1 style='text-align: left; color: white;'>Welcome Using GPT ChatBot</h1>", unsafe_allow_html=True)
        # st.markdown("<h2 style='text-align: left; color: grey;'>Press the Button to start</h1>", unsafe_allow_html=True)
        # st.text_input("Ensure the Key is valid (Enter: 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)", key="OPENAI_API_KEY", on_change=is_key_valid)
        st.button("Press to Start", on_click=is_key_valid)

    # main frame
    st.chat_message("assistant").write("Hi! What can I help you today?")
    st.chat_input("Enter your message", disabled=True)

    if st.session_state.ObtainedValidKey == False:
        st.stop()
    st.write("Welcome to the ChatBot")
    return True

def reset_chat_history():
    st.session_state.chat_history = []

def blank():
    if "chat_history" not in st.session_state:  
        st.session_state.chat_history = []

    ## Slide Bar Design
    with st.sidebar:
        st.title("Parameter")
        st.selectbox('Model', ('ChatGPT-3.5',))

        st.slider("Temperatiure", 0.0, 2.0, 0.98, 0.01)
        st.slider("Top P", 0.0, 1.0, 1.0, 0.01)
        st.slider("Frequency penalty", 0.0, 2.0, 0.0, 0.01)
        st.slider("Presence penalty", 0.0, 2.0, 0.0, 0.01)
        st.info("Keep setting if not sure")
        st.button("Reset Chat", help="This will restart the conversation", on_click=reset_chat_history)
    
    ## main frame
    st.chat_message("assistant").write("Hi! What can I help you today?")
    for message in st.session_state.chat_history:
        match type(message):
            case langchain.schema.messages.AIMessage:
                st.chat_message("assistant").write(message.content)
            case langchain.schema.messages.HumanMessage:
                st.chat_message("user").write(message.content)

    if prompt := st.chat_input("Enter your message"):
        chat = ChatOpenAI(openai_api_key="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")
        st.chat_message("user").write(prompt)
        st.session_state.chat_history.append(HumanMessage(content = prompt))
        with st.status("Chatting with OpenAI...") as status:
            response = chat(st.session_state.chat_history)
            status.update(label="Response Received!", state="complete")
            time.sleep(0.3)
        st.chat_message("assistant").write(response.content)
        st.session_state.chat_history.append(AIMessage(content=response.content))
        


def main():
    if "ObtainedValidKey" not in st.session_state:
        st.session_state["ObtainedValidKey"] = False
        st.session_state["chatMessage"] = []

    ## Scene 1 - Obtain a valid OpenAI API Key
    if st.session_state.ObtainedValidKey == False:
        obtain_valid_API_Key()
        
    ## Scene 2 
    blank()

if __name__ == '__main__':
    main()