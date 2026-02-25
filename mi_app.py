import streamlit as st
import requests

st.set_page_config(page_title="Monitor Alborada Pro", layout="wide")

# 1. FUNCIÓN MAESTRA DE PRECIOS AUTOMÁTICOS
def obtener_datos_mercado():
    # Precios por defecto por si falla la conexión
    precios = {
        "Oficial": 0.0, "Mayorista": 0.0, "Blue Pizarra": 0.0, "Blue Real": 0.0,
        "Soja": 285.0, "Maiz": 178.0, "Trigo": 215.0, "Aceite Girasol": 1050.0
    }
    try:
        # Traer Dólares
        res_dolar = requests.get("https://criptoya.com/api/dolar").json()
        precios["Oficial"] = res_dolar['oficial']['price']
        precios["Mayorista"] = res_dolar['mayorista']['price']
        precios["Blue Pizarra"] = res_dolar['blue']['ask']
        precios["Blue Real"] = res_dolar['blue']['ask'] + 20
        
        # Traer Granos (Referencia Matba-Rofex vía API pública)
        res_granos = requests.get("https://api.argentinadatos.com/v1/cotizaciones/granos").json()
        # Buscamos las últimas cotizaciones disponibles
        for g in res_granos:
            if g['especie'] == 'soja': precios["Soja"] = g['valor']
            if g['especie'] == 'maiz': precios["Maiz"] = g['valor']
            if g['especie'] == 'trigo': precios["Trigo"] = g['valor']
    except:
        st.warning("⚠️ Usando precios de referencia. Verifique conexión.")
    return precios

datos = obtener_datos_mercado()

st.title("🌾 Monitor Comercial: Granos y Divisas")
st.caption("Actualización automática en cada carga")

# 2. MONITOR VISUAL
st.subheader("💵 Divisas en Tiempo Real")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Blue Pizarra", f"${datos['Blue Pizarra']}")
c2.metric("Blue Real", f"${datos['Blue Real']}")
c3.metric("Oficial BNA", f"${datos['Oficial']}")
c4.metric("Mayorista", f"${datos['Mayorista']}")

st.subheader("🚜 Granos y Aceites (USD/Tn)")
g1, g2, g3, g4 = st.columns(4)
g1.metric("Soja Rosario", f"{datos['Soja']} USD")
g2.metric("Maíz Rosario", f"{datos['Maiz']} USD")
g3.metric("Trigo Rosario", f"{datos['Trigo']} USD")
g4.metric("Aceite Girasol", f"{datos['Aceite Girasol']} USD")

st.divider()

# 3. CALCULADORA INTELIGENTE
st.subheader("🧮 Calculadora de Negocios")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Entrada (Costo)")
    monedas = {"Blue Real": datos['Blue Real'], "Mayorista": datos['Mayorista'], "Oficial": datos['Oficial']}
    sel_costo = st.selectbox("Moneda de pago", list(monedas.keys()))
    monto_costo = st.number_input("Monto (USD)", value=1000.0)

    st.markdown("### 📤 Salida (Venta)")
    sel_venta = st.selectbox("Moneda de cobro", list(monedas.keys()), index=1)
    margen = st.slider("Margen (%)", 0, 30, 5)

with col2:
    v_costo = monedas[sel_costo]
    v_venta = monedas[sel_venta]
    precio_sugerido = (monto_costo * v_costo / v_venta) * (1 + margen/100)
    
    st.write(f"### Precio sugerido en **{sel_venta}**:")
    st.header(f"{round(precio_sugerido, 2)} USD")
