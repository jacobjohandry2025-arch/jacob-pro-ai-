import streamlit as st

st.set_page_config(page_title="JACOB PRO WEB")
st.title("JACOB PRO AI v.1.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta
    if "1+1" in prompt:
        res = "El resultado es 2."
    else:
        res = "IA de Jacob Online."
    
    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})


