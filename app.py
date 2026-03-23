import streamlit as st
import google.generativeai as genai

# Título de la app
st.title("JACOB PRO AI v.1.0")

# Intentar obtener la API Key de cualquier forma posible
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("api_key") or st.secrets.get("google_api_key")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Falta la API Key en los Secrets de Streamlit")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if api_key:
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
            except Exception as e:
                full_response = f"Error: {str(e)}"
                st.markdown(full_response)
        else:
            full_response = "IA de Jacob Online (Sin conexión a Google)"
            st.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})




