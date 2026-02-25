def obtener_datos_mercado():
    precios = {"Oficial": 0, "Mayorista": 0, "Blue Pizarra": 0, "Blue Real": 0, "Soja": 285, "Maiz": 178, "Trigo": 215, "Aceite Girasol": 1050}
    try:
        # Dólares (Esta fuente es muy estable)
        res_dolar = requests.get("https://criptoya.com/api/dolar", timeout=10).json()
        precios["Oficial"] = res_dolar['oficial']['price']
        precios["Mayorista"] = res_dolar['mayorista']['price']
        precios["Blue Pizarra"] = res_dolar['blue']['ask']
        precios["Blue Real"] = res_dolar['blue']['ask'] + 20
        
        # Granos (Fuente alternativa)
        res_granos = requests.get("https://api.argentinadatos.com/v1/cotizaciones/granos", timeout=10).json()
        for g in res_granos:
            if g['especie'] == 'soja': precios["Soja"] = g['valor']
            if g['especie'] == 'maiz': precios["Maiz"] = g['valor']
            if g['especie'] == 'trigo': precios["Trigo"] = g['valor']
    except Exception as e:
        # Si ves el cartel amarillo, es que falló la conexión arriba
        st.warning("⚠️ El sistema no pudo conectar con el mercado. Usando precios de referencia.")
    return precios
