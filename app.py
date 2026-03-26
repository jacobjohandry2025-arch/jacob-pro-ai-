import streamlit as st
import google.generativeai as genai

# Configuración básica
st.set_page_config(page_title="Jacob Pro IA", page_icon="🤖")
st.title("JACOB PRO AI v.1.0")

# Cargar la llave desde los Secrets (Misterios)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("api_key")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error de configuración: {e}")
else:
    st.warning("⚠️ Falta la API Key en Secrets.")

# Chat
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
                # Intentar generar respuesta
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.info("Sin conexión a la llave.")
