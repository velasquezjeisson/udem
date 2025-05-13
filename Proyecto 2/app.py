import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import boto3

# Función para detectar la IP pública desde metadata EC2
def get_ec2_public_ip():
    try:
        response = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4", timeout=2)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return "localhost"

def get_backend_ip_from_tags():
    try:
        # Obtener credenciales temporales de la instancia EC2
        session = boto3.Session()
        ec2 = session.client("ec2", region_name="us-east-1")  # Ajusta región

        # Obtener el ID de la propia instancia
        instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=2).text

        # Obtener información de la VPC
        reservations = ec2.describe_instances(
            Filters=[
                {"Name": "tag:Name", "Values": ["*-backend"]}
            ]
        )

        for reservation in reservations["Reservations"]:
            for instance in reservation["Instances"]:
                if instance["State"]["Name"] == "running":
                    return instance["PublicIpAddress"]
    except Exception as e:
        print("Fallo detectando backend IP:", e)
        return "localhost"

# Construcción dinámica de la URL de la API
#ip_address = get_ec2_public_ip()
#ip_api = f"http://{ip_address}:8000/predict"

ip_api = f"http://{get_backend_ip_from_tags()}:8000/predict"


# Configuración de la app
st.set_page_config(page_title="Predicción de Demanda", layout="centered")
st.title("📈 Predicción con GradientBoostingRegressor")

# Slider de periodos
n = st.slider("Selecciona cuántos períodos quieres predecir", min_value=1, max_value=30, value=10)

# Entrada de valores iniciales
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

# Botón para enviar la predicción
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
            st.error(f"❌ Error {response.status_code}: {response.json()['detail']}")
