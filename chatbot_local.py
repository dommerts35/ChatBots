import streamlit as st
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title="Chatbot Cloud Ollama", layout="centered")
st.title("Chatbot con Modelos Cloud de Ollama")
st.caption("Usa modelos avanzados en la nube como DeepSeek, Qwen, GLM y GPT-OSS.")


st.sidebar.header("Configuración del modelo")

modelos_disponibles = [
    "deepseek-v3.1:671b-cloud",
    "qwen3-coder:480b-cloud",
    "glm-4.6:cloud",
    "gpt-oss:20b-cloud"
]

modelo_seleccionado = st.sidebar.selectbox("Selecciona el modelo:", modelos_disponibles)

st.sidebar.info("Asegúrate de que Ollama esté ejecutándose y tengas conexión con los modelos cloud.")

if st.sidebar.button("Reiniciar conversación"):
    st.session_state.clear()
    st.success("Conversación reiniciada correctamente.")


if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "contexto" not in st.session_state:
    st.session_state.contexto = ""


def generar_respuesta_ollama(contexto, modelo):

    prompt = (
        "Eres un asistente conversacional en español, amable, coherente y útil. "
        "Responde con naturalidad, sin repetir frases ni inventar información. "
        "Continúa esta conversación:\n\n"
        f"{contexto}\nBot:"
    )

    data = {"model": modelo, "prompt": prompt, "stream": False}

    try:
        respuesta = requests.post(OLLAMA_URL, json=data)
        respuesta.raise_for_status()
        salida = respuesta.json()
        return salida.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        return f"Error al conectar con Ollama: {e}"


st.markdown("---")
st.subheader("Chat")


for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"**Tú:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")


mensaje_usuario = st.text_input("Escribe tu mensaje:")


if st.button("Enviar") and mensaje_usuario:
    st.session_state.mensajes.append({"role": "user", "content": mensaje_usuario})
    st.session_state.contexto += f"Tú: {mensaje_usuario}\n"

    with st.spinner(f"El modelo '{modelo_seleccionado}' está pensando..."):
        respuesta = generar_respuesta_ollama(st.session_state.contexto, modelo_seleccionado)

    st.session_state.mensajes.append({"role": "bot", "content": respuesta})
    st.session_state.contexto += f"Bot: {respuesta}\n"
    st.rerun()
