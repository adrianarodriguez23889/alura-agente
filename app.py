import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
import google.generativeai as genai

# 1. Cargar la API Key desde el archivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ No se encontró la GEMINI_API_KEY. Verifica que el archivo .env esté bien guardado.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Configuración visual de la aplicación web
st.set_page_config(page_title="Alura Agente - TechMarket", page_icon="🤖", layout="wide")

st.title("🤖 Alura Agente")
st.subheader("Asistente Virtual Corporativo de TechMarket")
st.markdown("---")

# 3. Cargar y procesar documentos de la carpeta /data
@st.cache_resource
def cargar_base_conocimiento():
    contexto = ""
    
    # Cargar PDF de políticas
    ruta_pdf = os.path.join("data", "Politicas_Tienda.pdf")
    if os.path.exists(ruta_pdf):
        try:
            reader = PdfReader(ruta_pdf)
            texto_pdf = "\n".join([pagina.extract_text() for pagina in reader.pages if pagina.extract_text()])
            contexto += f"\n=== POLÍTICAS Y FAQ (PDF) ===\n{texto_pdf}\n"
        except Exception as e:
            st.warning(f"No se pudo leer el PDF: {e}")
    
    # Cargar CSV de inventario con codificación flexible
    ruta_csv = os.path.join("data", "productos_inventario.csv")
    if os.path.exists(ruta_csv):
        df = None
        # Intentar varias codificaciones comunes en Windows
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'ISO-8859-1']:
            try:
                df = pd.read_csv(ruta_csv, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if df is not None:
            texto_csv = df.to_markdown(index=False)
            contexto += f"\n=== INVENTARIO DE PRODUCTOS (CSV) ===\n{texto_csv}\n"
        else:
            st.warning("No se pudo leer el CSV debido a la codificación del archivo.")
        
    return contexto

contexto_empresa = cargar_base_conocimiento()

# 4. Barra lateral informativa
with st.sidebar:
    st.header("📂 Documentación Cargada")
    st.success("✅ Politicas_Tienda.pdf")
    st.success("✅ productos_inventario.csv")
    st.info("💡 Pregúntame sobre envíos, garantías, productos o stock de la tienda.")

# 5. Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy el Alura Agente de TechMarket. ¿En qué te puedo ayudar hoy?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. Capturar pregunta del usuario y consultar a la IA
if prompt := st.chat_input("Escribe tu pregunta sobre la empresa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en los documentos de la empresa..."):
            system_prompt = f"""
            Eres 'Alura Agente', el asistente interno de la empresa TechMarket.
            Responde la pregunta del colaborador de forma clara y amable usando ÚNICAMENTE la siguiente información interna.
            Si la información no figura en los documentos, indica que no dispones de esa información en la base actual.

            Información corporativa disponible:
            {contexto_empresa}

            Pregunta del usuario: {prompt}
            """
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(system_prompt)
                respuesta_texto = response.text
            except Exception as e:
                respuesta_texto = f"Error al consultar la IA: {str(e)}"

            st.write(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})