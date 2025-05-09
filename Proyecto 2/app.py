import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la app
st.set_page_config(page_title="Predicción de Demanda", layout="centered")
st.title("📈 Predicción con GradientBoostingRegressor")

# Parámetros
ip_api = "http://<TU_IP_PUBLICA>:8000/predict"

# Slider de periodos
n = st.slider("Selecciona cuántos períodos quieres predecir", min_value=1, max_value=30, value=10)

# Opcional: valores iniciales
default_input = [100.0] * 10
user_input = st.text_area("Valores iniciales (opcional, 10 valores separados por coma)", value=", ".join(map(str, default_input)))

try:
    initial_values = [float(x.strip()) for x in user_input.split(",")]
    if len(initial_values) != 10:
        st.warning("Debes ingresar exactamente 10 valores.")
        st.stop()
except ValueError:
    st.error("Entrada inválida. Asegúrate de que todos los valores sean numéricos.")
    st.stop()

# Botón de predicción
if st.button("Predecir"):
    with st.spinner("Consultando modelo..."):
        response = requests.post(ip_api, json={
            "n_periods": n,
            "initial_values": initial_values
        })

        if response.status_code == 200:
            data = response.json()
            preds = data["predictions"]

            st.success("✅ Predicción exitosa")
            st.write("### Predicciones:")
            st.write(preds)

            df = pd.DataFrame({"Periodo": list(range(1, n + 1)), "Valor": preds})

            st.line_chart(df.set_index("Periodo"))
        else:
            st.error(f"X Error {response.status_code}: {response.json()['detail']}")
