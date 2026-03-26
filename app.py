import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Jacob Pro IA", page_icon="🤖")
st.title("JACOB PRO AI v.1.0")

# --- TRUCO PARA ELIMINAR EL ERROR 404 ---
from google.generativeai import client
client.DEFAULT_API_VERSION = 'v1'
# ---------------------------------------

# Obtener la llave
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("api_key")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos el modelo con su nombre completo y estable
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error de configuración: {e}")
else:
    st.warning("⚠️ Revisa tus Secrets en Streamlit.")

# Historial
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
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
        else:
            st.info("IA de Jacob Online (Sin conexión)")

