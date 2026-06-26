import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

st.title("Dashboard de Ventas")
st.write("Visualiza productos, clasificación y productos 'Hueso' desde el backend.")


def fetch_data(path):
    try:
        response = requests.get(f"{BASE_URL}{path}", timeout=5)
        response.raise_for_status()
        return response.json().get("data", []), None
    except requests.RequestException as error:
        return [], str(error)


productos, err_productos = fetch_data("/api/productos")
clasificacion, err_clasificacion = fetch_data("/api/dashboard/clasificacion")
hueso, err_hueso = fetch_data("/api/dashboard/productos-hueso")

if err_productos or err_clasificacion or err_hueso:
    st.error("No se pudo conectar con el backend. Asegúrate de que FastAPI esté ejecutándose en http://127.0.0.1:8000")
    if err_productos:
        st.write("Productos:", err_productos)
    if err_clasificacion:
        st.write("Clasificación:", err_clasificacion)
    if err_hueso:
        st.write("Productos Hueso:", err_hueso)
    st.stop()

estrellas = sum(1 for item in clasificacion if item.get("clasificacion") == "Estrella")
huesos = sum(1 for item in clasificacion if item.get("clasificacion") == "Hueso")

with st.expander("Resumen rápido", expanded=True):
    col1, col2, col3 = st.columns(3)
    col1.metric("Productos registrados", len(productos))
    col2.metric("Productos Hueso", len(hueso))
    col3.metric("Productos Estrella", estrellas)

    if len(clasificacion) > 0:
        top_participacion = max(clasificacion, key=lambda x: x.get("participacion", 0))
        st.write("**Producto con mayor participación:**", top_participacion.get("nombre"), "(", top_participacion.get("participacion"), "% )")

st.markdown("---")

tabs = st.tabs(["Productos", "Clasificación", "Productos Hueso"])

with tabs[0]:
    st.subheader("Lista de productos")
    st.dataframe(productos, use_container_width=True)

with tabs[1]:
    st.subheader("Clasificación de productos")
    st.dataframe(clasificacion, use_container_width=True)

with tabs[2]:
    st.subheader("Productos Hueso")
    st.dataframe(hueso, use_container_width=True)

st.markdown("---")
st.write("Si quieres hacer pruebas de venta, utiliza el endpoint `POST /api/ventas` desde el backend.")
