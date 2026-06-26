import streamlit as st
import requests

st.title("Clasificación de Productos")

datos = requests.get(
    "http://localhost:8000/api/dashboard/clasificacion"
).json()["data"]

st.table(datos)