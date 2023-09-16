import streamlit as st
import time
import langchain
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from langchain.chat_models import ChatOpenAI

def change_key_validation(api_key, correctness):
        st.session_state.OPENAI_API_KEY = api_key
        st.session_state["obtained_api_key"] = correctness

def valid_api_key(api_key):
    with st.status("Chatting with OpenAI...") as status:
        chat = ChatOpenAI(openai_api_key=api_key)
        test_message = [HumanMessage(content="hi!")]
        try:
            chat(test_message)
            status.update(label="Response Received!", state="complete")
        except Exception:
            status.update(label="Invalid/ Wrong Key!", state="error")
            st.stop()

        change_key_validation(api_key=api_key, correctness=True)    
        st.experimental_rerun()


def obtain_api_key():
    if "obtained_api_key" not in st.session_state:
        change_key_validation(api_key="", correctness=False)    
    
    if st.session_state["obtained_api_key"] is True:
        return
    
    # layout
    st.markdown("<h1>💭 Welcome Using GPT ChatBot</h1>", unsafe_allow_html=True)
    if (api_key := st.text_input("Enter OpenAI API Key")):
            valid_api_key(api_key)
    st.stop()

def reset_chat_history():
    st.session_state['qota'] = []
    st.session_state["chat_history"] = []

def show_token_usage():
    with st.sidebar:
        st.line_chart( st.session_state.qota)
        pass

def chat_parameter():
    with st.sidebar:
        st.session_state.parameter = st.header("Parameter")
        st.session_state.temperature = st.slider("Temperatiure", 0.0, 2.0, 0.98, 0.01)
        st.session_state.topP = st.slider("Top P", 0.0, 1.0, 1.0, 0.01)
        st.session_state.frequencyPenalty = st.slider("Frequency penalty", 0.0, 2.0, 0.0, 0.01)
        st.session_state.presencePenalty = st.slider("Presence penalty", 0.0, 2.0, 0.0, 0.01)

def print_dialogue(role, dialogue):
    st.chat_message(role).write(dialogue)

def print_chat_history():
    st.chat_message("assistant").write("Hi! How can I help you today?")
    
    for messaage in st.session_state["chat_history"]:
        if (type(messaage) is langchain.schema.messages.AIMessage):
            print_dialogue("assistant", messaage.content)
        else:
            print_dialogue("user", messaage.content)

def reset_chat():
    with st.sidebar:
        st.button("Reset Chat", on_click=reset_chat_history)
     
def chat_with_openai():
    if (prompt := st.chat_input("Enter your message")):
        chat = ChatOpenAI(openai_api_key=st.session_state.OPENAI_API_KEY)
        print_dialogue("user", prompt)
        st.session_state["chat_history"].append(HumanMessage(content=prompt))
        with st.status("Chatting with OpenAI...") as status:
            response = chat(st.session_state.chat_history)
            status.update(label="Response Received!", state="complete")
            time.sleep(0.3)
        print_dialogue("assistant", response.content)
        st.session_state.chat_history.append(AIMessage(content=response.content))


def chat():
    if "token" and "chat_history" not in st.session_state:
        reset_chat_history()

    # show_token_usage()

    chat_parameter()

    print_chat_history()

    reset_chat()

    chat_with_openai()



def main():
    obtain_api_key()
    chat()


if __name__ == '__main__':
    main()
    pass