import streamlit as st
from agent import ask_agent


st.set_page_config(page_title="Monday BI Agent", layout="wide")

st.title("📊 Monday.com Business Intelligence Agent")

st.write(
    "Ask questions about deals, pipeline health, sectors, and work orders."
)

# Leadership update button
if st.button("Generate Leadership Update"):

    with st.spinner("Preparing leadership update..."):
        response, steps = ask_agent("Prepare a leadership update")

    for step in steps:
        st.write(step)

    st.write(response)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


user_input = st.chat_input("Ask a business question...")


if user_input:

    with st.spinner("Analyzing monday.com data..."):

        response, steps = ask_agent(user_input)

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", response))
    
    for step in steps:
        st.write(step)


for role, message in st.session_state.chat_history:

    if role == "user":
        st.chat_message("user").write(message)

    else:
        st.chat_message("assistant").write(message)