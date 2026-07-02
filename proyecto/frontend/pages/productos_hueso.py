import streamlit as st
import requests

st.title("Productos Hueso")

data = requests.get(
    "http://localhost:8000/api/dashboard/productos-hueso"
).json()["data"]

st.table(data)