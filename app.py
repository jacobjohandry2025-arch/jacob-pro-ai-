import streamlit as st
import google.generativeai as genai

# Título de la app
st.set_page_config(page_title="Jacob Pro IA", page_icon="🤖")
st.title("JACOB PRO AI v.1.0")

# Intentar obtener la API Key de los Secrets de Streamlit
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("api_key") or st.secrets.get("google_api_key")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos el modelo 'gemini-1.5-flash' que es el más rápido y actual
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error al configurar Google AI: {e}")
else:
    st.warning("⚠️ Falta la API Key en los Secrets (Misterios) de Streamlit.")

# Historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        if api_key:
            try:
                # Generar respuesta con el modelo configurado
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
            except Exception as e:
                full_response = f"Error en la conexión: {str(e)}"
                st.error(full_response)
        else:
            full_response = "IA de Jacob Online (Sin conexión a Google. Revisa tus Secrets)."
            st.info(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
