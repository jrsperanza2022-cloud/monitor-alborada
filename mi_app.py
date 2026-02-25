import streamlit as st
import requests

st.set_page_config(page_title="Monitor Alborada Pro", layout="wide")

# 1. FUNCIÓN PARA DÓLARES AUTOMÁTICOS
def obtener_dolares():
    try:
        url = "https://criptoya.com/api/dolar"
        datos = requests.get(url).json()
        return {
            "Oficial": datos['oficial']['price'],
            "Mayorista": datos['mayorista']['price'],
            "Blue Pizarra": datos['blue']['ask'],
            "Blue Real": datos['blue']['ask'] + 20
        }
    except:
        return {"Oficial": 1000.0, "Mayorista": 1000.0, "Blue Pizarra": 1100.0, "Blue Real": 1120.0}

precios_dolar = obtener_dolares()

st.title("🌾 Monitor Comercial: Granos y Divisas")

# 2. SECCIÓN DE GRANOS (CARGA MANUAL RÁPIDA)
st.sidebar.header("⚙️ Actualizar Granos/Aceites")
soja = st.sidebar.number_input("Soja Rosario (USD)", value=285.0)
maiz = st.sidebar.number_input("Maíz Rosario (USD)", value=175.0)
trigo = st.sidebar.number_input("Trigo Rosario (USD)", value=210.0)
girasol = st.sidebar.number_input("Aceite Girasol (USD)", value=1050.0)

# 3. MONITOR VISUAL
st.subheader("💵 Divisas en Tiempo Real")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Blue Pizarra", f"${precios_dolar['Blue Pizarra']}")
c2.metric("Blue Real", f"${precios_dolar['Blue Real']}")
c3.metric("Oficial BNA", f"${precios_dolar['Oficial']}")
c4.metric("Mayorista", f"${precios_dolar['Mayorista']}")

st.subheader("🚜 Precios de Referencia (Granos/Aceites)")
g1, g2, g3, g4 = st.columns(4)
g1.metric("Soja", f"{soja} USD")
g2.metric("Maíz", f"{maiz} USD")
g3.metric("Trigo", f"{trigo} USD")
g4.metric("Aceite Girasol", f"{girasol} USD")

st.divider()

# 4. CALCULADORA MULTI-MONEDA
st.subheader("🧮 Calculadora de Negocios")
col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    st.markdown("### 📥 Entrada (Costo)")
    opciones_dolar = {
        "Dólar Blue Real": precios_dolar['Blue Real'],
        "Dólar Mayorista": precios_dolar['Mayorista'],
        "Dólar Oficial": precios_dolar['Oficial']
    }
    moneda_costo = st.selectbox("¿En qué moneda pagás el costo?", list(opciones_dolar.keys()))
    valor_costo = st.number_input("Monto del Costo (USD)", value=1000.0)

    st.markdown("### 📤 Salida (Venta)")
    moneda_venta = st.selectbox("¿En qué moneda cobrás?", list(opciones_dolar.keys()), index=1)
    ganancia_pct = st.slider("Margen de Ganancia (%)", 0, 30, 5)

with col_calc2:
    costo_pesos = valor_costo * opciones_dolar[moneda_costo]
    piso_equilibrio = costo_pesos / opciones_dolar[moneda_venta]
    precio_final = piso_equilibrio * (1 + (ganancia_pct / 100))

    st.write(f"### Precio sugerido en **{moneda_venta}**:")
    st.header(f"{round(precio_final, 2)} USD")
