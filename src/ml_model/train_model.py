import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os


def train_model():
    # Ruta correcta al archivo CSV
    csv_path = os.path.join(os.path.dirname(__file__), "../../data/simulated_metrics.csv")

    # Leer datos desde la carpeta "data"
    df = pd.read_csv(csv_path)
    X = df[["cpu_usage"]]
    y = df["cost_usd"]

    # Entrenar el modelo
    model = LinearRegression()
    model.fit(X, y)

    # Guardar el modelo en la carpeta "src/ml_model"
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    joblib.dump(model, model_path)
    print("✅ Modelo entrenado y guardado en 'src/ml_model/model.pkl'")


if __name__ == "__main__":
    train_model()