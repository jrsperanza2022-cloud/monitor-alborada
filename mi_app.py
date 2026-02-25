import streamlit as st
import requests

st.set_page_config(page_title="Monitor Alborada Pro", layout="wide")

def obtener_datos():
    p = {"Oficial": 1400.0, "Mayorista": 1380.5, "Blue Pizarra": 1430.0, "Soja": 285.0, "Maiz": 178.0, "Trigo": 215.0, "Aceite": 1050.0}
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
    except:
        pass 
    p["Blue Real"] = p["Blue Pizarra"] + 20
    return p

d = obtener_datos()

st.title("🌾 Monitor Alborada")

# FILA 1: TODAS LAS DIVISAS A LA VISTA
st.subheader("💵 Divisas")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Blue Real", f"${d['Blue Real']}")
c2.metric("Blue Pizarra", f"${d['Blue Pizarra']}")
c3.metric("Oficial BNA", f"${d['Oficial']}")
c4.metric("Mayorista", f"${d['Mayorista']}")

# FILA 2: TODOS LOS GRANOS A LA VISTA
st.subheader("🚜 Granos y Aceites (USD/Tn)")
g1, g2, g3, g4 = st.columns(4)
g1.metric("Soja Rosario", f"{d['Soja']} USD")
g2.metric("Maíz Rosario", f"{d['Maiz']} USD")
g3.metric("Trigo Rosario", f"{d['Trigo']} USD")
g4.metric("Aceite Girasol", f"{d['Aceite']} USD")

st.divider()

# CALCULADORA
st.subheader("🧮 Calculadora de Conversión")
with st.container(border=True):
    col_a, col_b = st.columns(2)
    monedas = {"Blue Real": d['Blue Real'], "Mayorista": d['Mayorista'], "Oficial": d['Oficial'], "Blue Pizarra": d['Blue Pizarra']}
    
    with col_a:
        monto = st.number_input("Monto USD", value=1000.0)
        m_costo = st.selectbox("Desde:", list(monedas.keys()))
    
    with col_b:
        margen = st.slider("Ganancia %", 0, 30, 5)
        m_venta = st.selectbox("A:", list(monedas.keys()), index=1)

    res = (monto * monedas[m_costo] / monedas[m_venta]) * (1 + margen/100)
    
    st.markdown("---")
    st.markdown(f"### Precio Final Sugerido: **{round(res, 2)} USD**")
    st.info(f"Conversión de {m_costo} (${monedas[m_costo]}) a {m_venta} (${monedas[m_venta]})")
