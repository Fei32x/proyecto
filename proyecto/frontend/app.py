import streamlit as st
import requests

st.title("🚀 Smoke Test - Conexión Exitosa")
st.write("Consultando datos desde la Base de Datos a través del Backend...")

try:
    response = requests.get("http://localhost:8000/api/productos")
    if response.status_code == 200:
        data = response.json()["data"]
        st.success("✅ ¡Conexión UI -> API -> DB establecida con éxito!")
        st.table(data)
    else:
        st.error("Error al conectar con el Backend")
except:
    st.error("No se pudo conectar. ¿Está corriendo el Backend (uvicorn)?")