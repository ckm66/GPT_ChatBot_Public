import streamlit as st
import time
import langchain
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
import config

def validate_and_set_api_key(api_key, correctness):
    st.session_state.OPENAI_API_KEY = api_key
    st.session_state["obtained_api_key"] = correctness

def check_api_key(api_key):
    with st.status("Chatting with OpenAI...") as status:
        chat = ChatOpenAI(openai_api_key=api_key)
        test_message = [HumanMessage(content="hi!")]
        try:
            chat(test_message)
            status.update(label="Response Received!", state="complete")
        except Exception:
            status.update(label="Invalid/ Wrong Key!", state="error")
            st.stop()

        validate_and_set_api_key(api_key=api_key, correctness=True)    
        st.experimental_rerun()

def get_api_key():
    if "obtained_api_key" not in st.session_state:
        validate_and_set_api_key(api_key="", correctness=False)    

    if st.session_state["obtained_api_key"] is True:
        return

    # layout
    st.markdown("<h1>💭 Welcome Using GPT ChatBot</h1>", unsafe_allow_html=True)
    if (api_key := st.text_input("Enter OpenAI API Key")):
            check_api_key(api_key)
    st.stop()

def reset_chat():
    st.session_state["token"] = 0
    st.session_state.addtoken = 0
    if "bot" and "chat_history" not in st.session_state:
        st.session_state["bot"] = "Stephen - General (Default)"
        st.session_state.chat_history = []
        return
    set_bot(st.session_state.bot)
    print(st.session_state.chat_history)

def set_bot(bot):
    st.session_state.bot = bot
    st.session_state.chat_history = config.predefinedMessage[bot]
    return

def set_chat_parameters():
    with st.sidebar:
        bot = st.selectbox("Who you want to chat with?", ("Stephen - General (Default)", "Emily - Grammar Checker", "Alex - Email Assistant", "Jerry - Senior Programmer"))
        if bot != st.session_state.bot:
            set_bot(bot)
        st.header("Description")
        st.write(config.botDescription[st.session_state.bot])
        st.session_state.parameter = st.header("Parameter")
        st.session_state.temperature = st.slider("Temperatiure", 0.0, 2.0, 0.98, 0.01)
        st.session_state.topP = st.slider("Top P", 0.0, 1.0, 1.0, 0.01)
        st.session_state.frequencyPenalty = st.slider("Frequency penalty", 0.0, 2.0, 0.0, 0.01)
        st.session_state.presencePenalty = st.slider("Presence penalty", 0.0, 2.0, 0.0, 0.01)
    

def display_dialogue(role, dialogue):
    st.chat_message(role).write(dialogue)

def display_chat_history():
    bot = st.session_state.bot[0: st.session_state.bot.index("-") - 1]
    st.chat_message("assistant").write(f"Hi! I am {bot}. How can I help you today?")

    for messaage in st.session_state["chat_history"]:
        if (type(messaage) is langchain.schema.messages.AIMessage):
            display_dialogue("assistant", messaage.content)
        elif (type(messaage) is langchain.schema.messages.HumanMessage):
            display_dialogue("user", messaage.content)


def display_reset_chat_button():
    with st.sidebar:
        st.button("Reset Chat", on_click=reset_chat, key="button")

def display_token():
    with st.sidebar:
        token_widget = st.empty()
        token_widget.metric("Total token used", st.session_state.token, st.session_state.addtoken)
        return token_widget

def send_message_to_openai(token_widget):
    if (prompt := st.chat_input("Enter your message")):
        # chat = ChatOpenAI(openai_api_key=st.session_state.OPENAI_API_KEY)
        chat = ChatOpenAI(openai_api_key="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")
        display_dialogue("user", prompt)
        st.session_state["chat_history"].append(HumanMessage(content=prompt))
        with st.status("Chatting with OpenAI...") as status:
            with get_openai_callback() as cb:
                response = chat(st.session_state.chat_history)
                st.session_state.addtoken = cb.total_tokens
                st.session_state.token += cb.total_tokens
            status.update(label="Response Received!", state="complete")
            time.sleep(0.3)
            token_widget.empty()
        display_dialogue("assistant", response.content)
        st.session_state.chat_history.append(AIMessage(content=response.content))
        display_token()


def start_chat():
    if "token" and "chat_history" not in st.session_state:
        reset_chat()

    set_chat_parameters()
    display_chat_history()
    display_reset_chat_button()
    token_widget = display_token()
    send_message_to_openai(token_widget)

def run_chat_app():
    get_api_key()
    start_chat()

if __name__ == '__main__':
    run_chat_app()
    pass