import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Control de Ventas", layout="centered")
st.title("📊 Registro de Ventas Diarias")

# Configurar API de Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Falta configurar la API Key de Gemini en los Secrets.")

# Formulario de entrada
fecha_seleccionada = st.date_input("Fecha de la venta", datetime.now())
archivo_imagen = st.file_uploader("Sube la imagen del reporte", type=["jpg", "jpeg", "png"])

if archivo_imagen and st.button("Procesar y Guardar"):
    with st.spinner("Analizando imagen con IA..."):
        try:
            imagen = Image.open(archivo_imagen)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "Busca la sección 'Total de Ventas' en este ticket/pantalla y devuelve ÚNICAMENTE el número entero sin símbolos de moneda, ni puntos, ni comas."
            
            respuesta = model.generate_content([prompt, imagen])
            monto_venta = int(''.join(filter(str.isdigit, respuesta.text)))
            
            st.success(f"✅ Venta detectada: ${monto_venta:,}")
            
        except Exception as e:
            st.error(f"No se pudo extraer el monto automáticamente. Revisa la foto. Error: {e}")
