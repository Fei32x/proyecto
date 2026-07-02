import os
import streamlit as st
import requests
import pandas as pd

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8001")

st.set_page_config(
    page_title="Dashboard de Ventas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --danger-color: #d62728;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .section-title {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .card-content {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .success-badge {
        background: #2ca02c;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        display: inline-block;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    .warning-badge {
        background: #ff7f0e;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        display: inline-block;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    .danger-badge {
        background: #d62728;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        display: inline-block;
        margin: 0.5rem 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header profesional
st.markdown("""
<div class="main-header">
    <h1>Dashboard de Ventas</h1>
    <p>Sistema de gestión y análisis de productos y ventas</p>
</div>
""", unsafe_allow_html=True)


if "current_view" not in st.session_state:
    st.session_state.current_view = "Dashboard"

# Sidebar Navegación
with st.sidebar:
    st.markdown("### Menu Principal")
    for item in ["Dashboard", "Productos Estrella", "Todos los Productos", "Clasificacion", "Productos Hueso", "Nueva Venta", "Nuevo Producto"]:
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.current_view = item
            st.rerun()
    st.markdown("---")
    st.markdown("### Informacion")
    st.info("Sistema de gestión de ventas en tiempo real. Todos los cambios se registran automáticamente en la base de datos.")

# Funciones de carga de datos
def fetch_json(path, method="get", json_body=None):
    candidates = [BASE_URL]
    if BASE_URL.endswith(":8001"):
        candidates.append("http://127.0.0.1:8000")
    elif BASE_URL.endswith(":8000"):
        candidates.append("http://127.0.0.1:8001")

    last_error = None
    for base_url in candidates:
        try:
            if method == "get":
                response = requests.get(f"{base_url}{path}", timeout=5)
            else:
                response = requests.post(f"{base_url}{path}", json=json_body, timeout=5)
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as error:
            last_error = error

    return None, str(last_error or "No se pudo conectar con el backend")


# Cargar datos
productos_data, err_productos = fetch_json("/api/productos")
dashboard_data, err_dashboard = fetch_json("/api/dashboard")
productos_estrella_data, err_estrella = fetch_json("/api/dashboard/productos-estrella")
hueso_data, err_hueso = fetch_json("/api/dashboard/productos-hueso")

if err_productos or err_dashboard or err_estrella or err_hueso:
    st.error(f"No se pudo conectar con el backend. Asegúrate de que FastAPI esté ejecutándose en {BASE_URL} o en el puerto alternativo 8000.")
    st.stop()

productos = productos_data.get("data", [])
clasificacion = dashboard_data.get("clasificacion", [])
productos_estrella = productos_estrella_data.get("data", [])
hueso = hueso_data.get("data", [])
resumen = dashboard_data.get("resumen", {})
ventas_por_producto = dashboard_data.get("ventas_por_producto", [])

menu_seleccion = st.session_state.current_view

# DASHBOARD PRINCIPAL
if menu_seleccion == "Dashboard":
    st.markdown('<div class="section-title">Resumen General</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Ventas</div>
            <div class="metric-value">${resumen.get('total_ventas', 0):.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Productos</div>
            <div class="metric-value">{len(productos)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Estrella</div>
            <div class="metric-value">{resumen.get('productos_estrella', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Hueso</div>
            <div class="metric-value">{resumen.get('productos_hueso', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_chart, col_form = st.columns([2, 1])
    
    with col_chart:
        st.markdown('<div class="section-title">Ventas por Producto</div>', unsafe_allow_html=True)
        if ventas_por_producto:
            ventas_df = pd.DataFrame(ventas_por_producto)
            st.bar_chart(ventas_df.set_index("producto")["cantidad"])
        else:
            st.info("No hay ventas registradas todavía.")
    
    with col_form:
        st.markdown('<div class="section-title">Acciones Rapidas</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-content">', unsafe_allow_html=True)
        
        if st.button("Nueva Venta", use_container_width=True):
            st.session_state.current_view = "Nueva Venta"
            st.rerun()
        
        if st.button("Nuevo Producto", use_container_width=True):
            st.session_state.current_view = "Nuevo Producto"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# PRODUCTOS ESTRELLA
elif menu_seleccion == "Productos Estrella":
    st.markdown('<div class="section-title">Productos Estrella</div>', unsafe_allow_html=True)
    st.markdown("Los productos más vendidos y rentables para tu negocio.", unsafe_allow_html=True)
    
    if productos_estrella:
        estrella_df = pd.DataFrame(productos_estrella)
        st.dataframe(
            estrella_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "nombre": st.column_config.TextColumn("Producto", width="medium"),
                "cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                "ventas": st.column_config.NumberColumn("Ventas ($)", format="$%.2f"),
                "participacion": st.column_config.NumberColumn("Participación (%)", format="%.2f%%"),
            }
        )
    else:
        st.info("No hay productos estrella aún. ¡Comienza a registrar ventas!")

# TODOS LOS PRODUCTOS
elif menu_seleccion == "Todos los Productos":
    st.markdown('<div class="section-title">Catalogo de Productos</div>', unsafe_allow_html=True)
    
    if productos:
        prod_df = pd.DataFrame(productos)
        st.dataframe(
            prod_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "nombre": st.column_config.TextColumn("Producto", width="medium"),
                "precio": st.column_config.NumberColumn("Precio ($)", format="$%.2f"),
            }
        )
    else:
        st.warning("No hay productos registrados.")

# CLASIFICACIÓN
elif menu_seleccion == "Clasificacion":
    st.markdown('<div class="section-title">Clasificacion de Productos</div>', unsafe_allow_html=True)
    
    if clasificacion:
        clasi_df = pd.DataFrame(clasificacion)
        st.dataframe(
            clasi_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "nombre": st.column_config.TextColumn("Producto", width="medium"),
                "cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                "ventas": st.column_config.NumberColumn("Ventas ($)", format="$%.2f"),
                "participacion": st.column_config.NumberColumn("Participación (%)", format="%.2f%%"),
                "clasificacion": st.column_config.TextColumn("Clasificación", width="small"),
            }
        )
    else:
        st.info("No hay datos de clasificación disponibles.")

# PRODUCTOS HUESO
elif menu_seleccion == "Productos Hueso":
    st.markdown('<div class="section-title">Productos Hueso</div>', unsafe_allow_html=True)
    st.markdown("Productos con menor venta que podrían necesitar promoción.", unsafe_allow_html=True)
    
    if hueso:
        hueso_df = pd.DataFrame(hueso)
        st.dataframe(
            hueso_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "nombre": st.column_config.TextColumn("Producto", width="medium"),
                "cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                "ventas": st.column_config.NumberColumn("Ventas ($)", format="$%.2f"),
                "participacion": st.column_config.NumberColumn("Participación (%)", format="%.2f%%"),
            }
        )
    else:
        st.success("¡No hay productos hueso! Todos tus productos venden bien.")

# NUEVA VENTA
elif menu_seleccion == "Nueva Venta":
    st.markdown('<div class="section-title">Registrar Nueva Venta</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">', unsafe_allow_html=True)
    
    productos_options = {item["nombre"]: item["id"] for item in productos}
    
    if productos_options:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_product = st.selectbox("Selecciona un producto", list(productos_options.keys()))
            cantidad = st.number_input("Cantidad", min_value=1, step=1, value=1)
        
        with col2:
            # Obtener precio del producto
            producto_seleccionado = next((p for p in productos if p["nombre"] == selected_product), None)
            if producto_seleccionado:
                precio = producto_seleccionado["precio"]
                subtotal = precio * cantidad
                st.metric("Subtotal", f"${subtotal:.2f}")
        
        st.markdown("---")
        
        if st.button("Registrar Venta", use_container_width=True):
            payload = {"productos": [{"id_producto": productos_options[selected_product], "cantidad": int(cantidad)}]}
            response, error = fetch_json("/api/ventas", method="post", json_body=payload)
            if error:
                st.error(f"Error: {error}")
            else:
                st.success(f"{response.get('mensaje', 'Venta registrada')}")
                st.balloons()
                st.rerun()
    else:
        st.warning("Agrega productos antes de registrar ventas.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# NUEVO PRODUCTO
elif menu_seleccion == "Nuevo Producto":
    st.markdown('<div class="section-title">Agregar Nuevo Producto</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nuevo_nombre = st.text_input("Nombre del producto")
    
    with col2:
        nuevo_precio = st.number_input("Precio", min_value=0.01, step=0.01, value=10.00)
    
    st.markdown("---")
    
    if st.button("Guardar Producto", use_container_width=True):
        if nuevo_nombre.strip():
            payload = {"nombre": nuevo_nombre, "precio": float(nuevo_precio)}
            response, error = fetch_json("/api/productos", method="post", json_body=payload)
            if error:
                st.error(f"Error: {error}")
            else:
                st.success(f"{response.get('mensaje', 'Producto agregado')}")
                st.balloons()
                st.rerun()
        else:
            st.warning("Por favor, ingresa un nombre para el producto.")
    
    st.markdown('</div>', unsafe_allow_html=True)

