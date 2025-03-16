import random
import joblib
import os


def lambda_handler():
    # Ruta correcta al archivo del modelo
    model_path = os.path.join(os.path.dirname(__file__), "../ml_model/model.pkl")

    # Cargar el modelo
    model = joblib.load(model_path)

    # Simular datos en vivo
    cpu = random.randint(40, 95)
    cost = model.predict([[cpu]])[0]

    # Lógica de alerta
    if cost > 180:
        print(f"🚨 ALERTA: Costo elevado (${cost:.2f} USD)")
    else:
        print(f"✅ Estable: ${cost:.2f} USD")


if __name__ == "__main__":
    lambda_handler()