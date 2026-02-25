import streamlit as st

st.set_page_config(page_title="Monitor Alborada Pro", layout="wide")

# 1. VALORES DE MERCADO
precios_base = {
    "Dólar Blue Pizarra": 1430.0,
    "Dólar Blue Real": 1430.0 + 20, 
    "Dólar Oficial": 1400.0,
    "Dólar Mayorista (Divisa)": 1380.5
}

st.title("🌾 Monitor Comercial: Granos y Divisas")

# 2. MONITOR VISUAL
st.subheader("💵 Referencias actuales")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Blue Pizarra", f"${precios_base['Dólar Blue Pizarra']}")
col2.metric("Blue Real", f"${precios_base['Dólar Blue Real']}")
col3.metric("Oficial BNA", f"${precios_base['Dólar Oficial']}")
col4.metric("Mayorista / Divisa", f"${precios_base['Dólar Mayorista (Divisa)']}")

st.divider()

# 3. CALCULADORA MULTI-MONEDA
st.subheader("🧮 Calculadora de Negocios Multi-Moneda")
c1, c2 = st.columns(2)

with c1:
    st.markdown("### 📥 Entrada (Costo)")
    moneda_costo = st.selectbox("¿En qué moneda pagás el costo?", ["Dólar Blue Real", "Dólar Mayorista (Divisa)", "Dólar Oficial", "Dólar Blue Pizarra"])
    valor_costo = st.number_input("Monto del Costo (USD)", value=980.0)

    st.markdown("### 📤 Salida (Venta)")
    moneda_venta = st.selectbox("¿En qué moneda vas a cobrar la venta?", ["Dólar Mayorista (Divisa)", "Dólar Oficial", "Dólar Blue Real", "Dólar Blue Pizarra"])
    ganancia_pct = st.slider("Margen de Ganancia deseado (%)", 0, 30, 5)

with c2:
    # --- CÁLCULO ---
    costo_en_pesos = valor_costo * precios_base[moneda_costo]
    piso_equilibrio = costo_en_pesos / precios_base[moneda_venta]
    precio_final = piso_equilibrio * (1 + (ganancia_pct / 100))

    st.write(f"### Precio a cobrar en **{moneda_venta}**:")
    st.header(f"{round(precio_final, 2)} USD")

    with st.expander("📝 Detalle técnico de la operación"):
        st.write(f"• Valor de reposición (Costo): ${precios_base[moneda_costo]}")
        st.write(f"• Valor de liquidación (Venta): ${precios_base[moneda_venta]}")
        st.write(f"• Punto muerto (0% ganancia): {round(piso_equilibrio, 2)} USD")
