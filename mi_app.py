import streamlit as st
import requests

st.set_page_config(page_title="Monitor Alborada Pro", layout="wide")

def obtener_datos():
    p = {
        "Oficial": 1400.0, "Mayorista": 1380.5, "Blue Pizarra": 1430.0, 
        "Soja": 285.0, "Maiz": 178.0, "Trigo": 215.0, "Girasol": 300.0,
        "Aceite Girasol": 1050.0, "Aceite Soja": 980.0, "Aceite Maiz": 1100.0
    }
    try:
        r_dolar = requests.get("https://criptoya.com/api/dolar", timeout=5).json()
        p["Oficial"] = r_dolar['oficial']['price']
        p["Mayorista"] = r_dolar['mayorista']['price']
        p["Blue Pizarra"] = r_dolar['blue']['ask']
        
        r_granos = requests.get("https://api.argentinadatos.com/v1/cotizaciones/granos", timeout=5).json()
        for g in r_granos:
            if g['especie'] == 'soja': p["Soja"] = g['valor']
            if g['especie'] == 'maiz': p["Maiz"] = g['valor']
            if g['especie'] == 'trigo': p["Trigo"] = g['valor']
            if g['especie'] == 'girasol': p["Girasol"] = g['valor']
    except:
        pass 
    p["Blue Real"] = p["Blue Pizarra"] + 20
    return p

d = obtener_datos()

st.title("🌾 Monitor Alborada")

# FILAS DE MERCADO (TODAS TIENEN EL MISMO TAMAÑO)
st.markdown("### 💵 Divisas")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Blue Real", f"${d['Blue Real']}")
c2.metric("Blue Pizarra", f"${d['Blue Pizarra']}")
c3.metric("Oficial BNA", f"${d['Oficial']}")
c4.metric("Mayorista", f"${d['Mayorista']}")

st.markdown("### 🚜 Granos (USD/Tn)")
g1, g2, g3, g4 = st.columns(4)
g1.metric("Soja Rosario", f"{d['Soja']} USD")
g2.metric("Maíz Rosario", f"{d['Maiz']} USD")
g3.metric("Trigo Rosario", f"{d['Trigo']} USD")
g4.metric("Girasol", f"{d['Girasol']} USD")

st.markdown("### 🧪 Aceites (USD/Tn)")
a1, a2, a3 = st.columns(3)
a1.metric("Aceite de Soja", f"{d['Aceite Soja']} USD")
a2.metric("Aceite de Maíz", f"{d['Aceite Maiz']} USD")
a3.metric("Aceite de Girasol", f"{d['Aceite Girasol']} USD")

st.divider()

# CALCULADORA CON RESULTADO GIGANTE UNIFICADO
st.subheader("🧮 Calculadora de Conversión")
with st.container(border=True):
    # Dividimos la pantalla: 3 partes para botones, 1 parte para el número grande
    col_izq, col_der = st.columns([3, 1.5]) 
    
    with col_izq:
        c_a, c_b = st.columns(2)
        monedas = {"Blue Real": d['Blue Real'], "Mayorista": d['Mayorista'], "Oficial": d['Oficial'], "Blue Pizarra": d['Blue Pizarra']}
        with c_a:
            monto = st.number_input("Monto USD", value=1000.0)
            m_costo = st.selectbox("Desde:", list(monedas.keys()))
        with c_b:
            margen = st.slider("Ganancia %", 0, 30, 5)
            m_venta = st.selectbox("A:", list(monedas.keys()), index=1)

    with col_der:
        # AQUÍ ESTÁ EL CAMBIO: El resultado ahora es una métrica igual a las de arriba
        res = (monto * monedas[m_costo] / monedas[m_venta]) * (1 + margen/100)
        st.write("## ") # Espacio para alinear
        st.metric(label="PRECIO FINAL", value=f"{round(res, 2)} USD")

    st.caption(f"Conversión: {m_costo} (${monedas[m_costo]}) a {m_venta} (${monedas[m_venta]})")
