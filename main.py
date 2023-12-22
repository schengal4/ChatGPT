import streamlit as st
import os 
import openai
import pandas as pd
from streamlit_chat import message

st.set_page_config(page_title="ChatGPT", layout="centered", initial_sidebar_state="auto",)

st.title('ChatGPT 4.0 Turbo Vision Preview')
st.write('128,000 token context window. Ability to understand images. Returns a maximum of 4,096 output tokens.')

# TODO: What if someone enters the same key for the secrets in Health Universe's secret manager?
openai.api_key = os.environ.get('OPENAI-KEY')

CONTENT = open('resources/system_prompt.txt', 'r').read()

def get_response():
    message_placeholder = st.empty()
    full_response = ""
    messages = [{"role": "system", "content": CONTENT}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    st.session_state["app"] = messages[-1]['content']
    
    for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages= messages,
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
    message_placeholder.markdown(full_response + "▌")
    return full_response

def main():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-1106-preview"

    # load previous messages, or empty list if there are no previous messages
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content":"Hi! How can I help you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # chatting part
    if prompt := st.chat_input("How can I help you?"):
        # user input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # response
        with st.chat_message("assistant"):
            full_response = get_response()
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
