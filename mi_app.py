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

# DIVISAS Y GRANOS EN COLUMNAS MÁS COMPACTAS
st.markdown("### 📊 Mercado en Vivo")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Blue Real", f"${d['Blue Real']}")
c2.metric("Soja Rosario", f"{d['Soja']} USD")
c3.metric("Maíz Rosario", f"{d['Maiz']} USD")
c4.metric("Aceite Girasol", f"{d['Aceite']} USD")

with st.expander("Ver más cotizaciones (Pizarra, Oficial, Trigo)"):
    e1, e2, e3 = st.columns(3)
    e1.write(f"**Blue Pizarra:** ${d['Blue Pizarra']}")
    e2.write(f"**Oficial BNA:** ${d['Oficial']}")
    e3.write(f"**Trigo:** {d['Trigo']} USD")

st.divider()

# CALCULADORA ENMASCARADA (DISEÑO LIMPIO)
st.subheader("🧮 Calculadora de Conversión")

with st.container(border=True):
    col_a, col_b = st.columns(2)
    monedas = {"Blue Real": d['Blue Real'], "Mayorista": d['Mayorista'], "Oficial": d['Oficial']}
    
    with col_a:
        monto = st.number_input("Monto a convertir (USD)", value=1000.0, step=100.0)
        m_costo = st.selectbox("Desde moneda:", list(monedas.keys()))
    
    with col_b:
        margen = st.slider("Margen de ganancia %", 0, 30, 5)
        m_venta = st.selectbox("A moneda:", list(monedas.keys()), index=1)

    # CÁLCULO Y RESULTADO DESTACADO
    valor_final = (monto * monedas[m_costo] / monedas[m_venta]) * (1 + margen/100)
    
    st.markdown(f"""
    <div style="background-color:#1e2129; padding:20px; border-radius:10px; text-align:center; border: 1px solid #4a4a4a;">
        <p style="margin:0; font-size:18px; color:#aaaaaa;">Precio Final Sugerido</p>
        <h1 style="margin:0; color:#2ecc71; font-size:48px;">{round(valor_final, 2)} USD</h1>
        <p style="margin:0; color:#555555; font-size:12px;">Usando {m_costo} a ${monedas[m_costo]} y {m_venta} a ${monedas[m_venta]}</p>
    </div>
    """, unsafe_allow_stdio=True, unsafe_allow_html=True)

st.caption("Actualización automática en cada carga.")
