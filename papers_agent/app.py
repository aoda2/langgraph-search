import streamlit as st
from graphs import getGraph

st.title("ChatGPT-like 論文検索")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):

        question = st.session_state.messages[-1]["content"]
        graph = getGraph()
        result = graph.invoke(
            {"question": question},
            debug=True,
        )
        st.markdown(result["answer"])

    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
