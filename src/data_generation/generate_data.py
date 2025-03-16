import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_data():
    # Simular 12 semanas de datos (84 días)
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(84)]  # 84 días

    # Patrón semanal realista (valores en float)
    base_cpu = np.array([60.0, 70.0, 75.0, 80.0, 85.0, 65.0, 55.0])  # <-- Usar float

    # Repetir el patrón para 12 semanas y convertir a float
    cpu = np.tile(base_cpu, 12).astype(np.float64)  # <-- Asegurar tipo float

    # Añadir fluctuación
    cpu += np.random.normal(0, 3, len(cpu))  # Ahora es compatible (float + float)
    cpu = np.clip(cpu, 40.0, 95.0)  # Limitar entre 40% y 95%

    # Calcular costos (float)
    cost = (cpu * 1.8) + np.random.normal(0, 5, len(cpu))

    # Crear DataFrame
    df = pd.DataFrame({
        "fecha": dates,
        "cpu_promedio": np.round(cpu, 1),
        "costo_total": np.round(cost, 2)
    })

    # Guardar datos
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/simulated_metrics.csv", index=False)
    print("✅ Datos generados exitosamente en 'data/simulated_metrics.csv'")


if __name__ == "__main__":
    generate_data()