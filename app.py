import streamlit as st
from google import genai
from PIL import Image
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Control de Ventas", layout="centered")
st.title("📊 Registro de Ventas Diarias")

# Configurar cliente de Gemini con API Key de los Secrets
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Falta configurar la API Key de Gemini en los Secrets.")
    st.stop()

# Formulario de entrada
fecha_seleccionada = st.date_input("Fecha de la venta", datetime.now())
archivo_imagen = st.file_uploader("Sube la imagen del reporte", type=["jpg", "jpeg", "png"])

if archivo_imagen and st.button("Procesar y Guardar"):
    with st.spinner("Analizando imagen con IA..."):
        try:
            imagen = Image.open(archivo_imagen)
            
            prompt = "Busca la sección 'Total de Ventas' en este ticket o pantalla y devuelve ÚNICAMENTE el número entero sin símbolos de moneda, ni puntos, ni comas."
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[imagen, prompt]
            )
            
            monto_venta = int(''.join(filter(str.isdigit, response.text)))
            st.success(f"✅ Venta detectada: ${monto_venta:,}")
            
        except Exception as e:
            st.error(f"Error al analizar la imagen: {e}")
