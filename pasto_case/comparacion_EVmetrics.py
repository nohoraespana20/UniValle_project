#C:/Users/noluc/OneDrive/Escritorio/multiobjetivo/

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def grafica_barras(df, path):
    # Extraer métricas y tecnologías
    metrics = df['Metrics']
    technologies = df.columns.drop('Metrics')

    # Configurar figura
    plt.figure(figsize=(12, 6))
    bar_width = 0.1
    x = np.arange(len(metrics))
    
    colors = ['#620062', '#a4165f', '#d54855', '#f4814b', '#ffbc4f', '#f9f871', '#00b6d6', '#006cbe']

    # Graficar barras por tecnología
    for i, tech in enumerate(technologies):
        bar_data = df[tech].values
        plt.bar(x + i * bar_width, bar_data, bar_width, label=tech, color=colors[i % len(colors)])

    # Ejes y etiquetas
    plt.ylabel('Valor normalizado')
    plt.xticks(x + bar_width * (len(technologies) - 1) / 2, metrics, rotation=0)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(path + "EVmetrics.jpg")

def normalize_dataframe(df):
    df = df.copy()
    df_metrics = df['Metrics']  # Guardar la columna de métricas
    df = df.drop('Metrics', axis='columns')  # Eliminarla temporalmente

    df_max = df.max(axis=1).replace(0, 1)  # Máximo por fila, evitando divisiones por cero
    df_normalized = df.div(df_max, axis=0)  # Dividir cada fila por su propio máximo

    df_normalized["Metrics"] = df_metrics  # Restaurar la columna de métricas
    return df_normalized

df_EVmetrics = pd.read_csv(f"C:/Users/noluc/OneDrive/Escritorio/EV_metrics.csv")

row1 = df_EVmetrics.iloc[[0]]
row2 = df_EVmetrics.iloc[[1]]
row3 = df_EVmetrics.iloc[[-1]]
df_technical = pd.concat([row1, row2, row3], ignore_index=True)
df_technical.drop('Criteria', axis='columns', inplace=True)
df_technical.head()
print(df_technical)
print('')
df_technical_normalized = normalize_dataframe(df_technical)
print(df_technical_normalized)
grafica_barras(df_technical_normalized, path='C:/Users/noluc/OneDrive/Escritorio/')