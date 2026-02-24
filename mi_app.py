import streamlit as st  # <--- ESTA LÍNEA ARREGLA EL ERROR

st.set_page_config(page_title="Monitor Alborada Pro", layout="wide")

# 1. VALORES DE MERCADO (Los que ya vimos en tus capturas)
precios_base = {
    "Dólar Blue": 1430.0 + 20, # Incluye tus $20 de cueva
    "Dólar Oficial": 1400.0,
    "Dólar Mayorista (Divisa)": 1380.5 #
}

st.title("🌾 Monitor Comercial: Granos y Divisas")

# 2. MONITOR VISUAL
st.subheader("💵 Referencias actuales")
col_d1, col_d2, col_d3 = st.columns(3)
col_d1.metric("Blue Real (Cueva)", f"${precios_base['Dólar Blue']}")
col_d2.metric("Oficial BNA", f"${precios_base['Dólar Oficial']}")
col_d3.metric("Mayorista / Divisa", f"${precios_base['Dólar Mayorista (Divisa)']}")

st.divider()

# 3. CALCULADORA MULTI-MONEDA PROFESIONAL
st.subheader("🧮 Calculadora de Negocios Multi-Moneda")
c1, c2 = st.columns(2)

with c1:
    st.markdown("### 📥 Entrada (Costo)")
    moneda_costo = st.selectbox("¿En qué moneda pagás el costo?", ["Dólar Blue", "Dólar Mayorista (Divisa)", "Dólar Oficial"])
    valor_costo = st.number_input("Monto del Costo (USD)", value=980.0)
    
    st.markdown("### 📤 Salida (Venta)")
    moneda_venta = st.selectbox("¿En qué moneda vas a cobrar la venta?", ["Dólar Mayorista (Divisa)", "Dólar Oficial", "Dólar Blue"])
    
    ganancia_pct = st.slider("Margen de Ganancia deseado (%)", 0, 30, 5)

with c2:
    # --- EL CEREBRO DEL CÁLCULO ---
    # Convertimos costo a pesos argentinos reales
    costo_en_pesos = valor_costo * precios_base[moneda_costo]
    
    # Calculamos el piso en la moneda que vas a cobrar
    piso_equilibrio = costo_en_pesos / precios_base[moneda_venta]
    
    # Aplicamos tu ganancia
    precio_final = piso_equilibrio * (1 + (ganancia_pct / 100))
    
    st.write(f"### Precio a cobrar en **{moneda_venta}**:")
    st.header(f"{round(precio_final, 2)} USD")
    
    with st.expander("📝 Detalle técnico de la operación"):
        st.write(f"• Valor de reposición (Costo): ${precios_base[moneda_costo]}")
        st.write(f"• Valor de liquidación (Venta): ${precios_base[moneda_venta]}")
        st.write(f"• Punto muerto (0% ganancia): {round(piso_equilibrio, 2)} USD")
        if moneda_costo == "Dólar Blue":
            st.info("💡 Este cálculo ya contempla los $20 de recargo sobre el Blue de pizarra.")