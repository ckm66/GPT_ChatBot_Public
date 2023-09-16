import langchain
import streamlit as st
from config import *
from bot_setting import * 

def side_bar():
    def reset_chat():
        bot[bot_symbol[bot_selection]](command="reset") 

    if "token" not in st.session_state:
        st.session_state.token = 0
        st.session_state.addtoken = 0
        
    with st.sidebar:
        bot_selection = st.selectbox("Who do you want to chat with ", ("Doris - General (Default)","Emily - Grammar Checker", "Alex - Email Assistant", "Jerry - Senior Programmer", "Jeff - Knowledge Manager"))
        bot[bot_symbol[bot_selection]]() # initalise Bot and set current_bot as selected

        st.title("Description")
        st.write(bot_description[st.session_state.current_bot])

        st.button("Reset Chat", on_click=reset_chat)
        st.metric("Total Token used", st.session_state.token, st.session_state.addtoken)


def main_frame():
    def introduce_bot():
        st.chat_message("assistant").write(bot_introduction[st.session_state.current_bot])

    def display_chat_history():
        chat_history = bot[st.session_state.current_bot](command="get history")
        for message in chat_history:
            if (type(message) is langchain.schema.messages.AIMessage):
                st.chat_message("assistant").write(message.content)
            elif (type(message) is langchain.schema.messages.HumanMessage):
                st.chat_message("user").write(message.content)
    
    def upload_file():
        upload_file = st.file_uploader("Choose a file")
        if upload_file is not None:
            bot[st.session_state.current_bot]("upload_pdf", "", upload_file)

    def get_user_message():
        if user_message := st.chat_input("Enter your message"):
            st.chat_message("user").write(user_message)
            with st.status("Chatting with OpenAI...") as status:
                response = bot[st.session_state.current_bot]("chat", user_message)
                if type(response) is not str:
                    status.update(label=response, state="error")
                    st.stop()
                status.update(label="Response Received!", state="complete")
                time.sleep(0.1)
            st.experimental_rerun()
    
    introduce_bot()
    if st.session_state.current_bot == "Jeff":
        upload_file()
    display_chat_history()
    get_user_message()



def run_chat_app():
    side_bar()
    main_frame()


if __name__ == '__main__':
    run_chat_app()
    pass