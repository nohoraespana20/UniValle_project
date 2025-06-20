#C:/Users/noluc/OneDrive/Escritorio/multiobjetivo/

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def get_last_row_aligned(df, columns_reference):
    last_row = df.iloc[[-1]]  # Esto mantiene el DataFrame con forma

    # Reindexar las columnas al esquema de df_problem3, llenando faltantes con 0
    return last_row.reindex(columns=columns_reference, fill_value=0)

def plot_radar(df, variables, title, ax, colors, show_legend=True):
    df_plot = df[['problema'] + variables].copy()

    labels = variables
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    for i, row in df_plot.iterrows():
        values = row[labels].tolist()
        values += values[:1]
        color = colors[i % len(colors)]
        ax.plot(angles, values, label=row['problema'], color=color)
        ax.fill(angles, values, color=color, alpha=0.1)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title(title, size=14)

    if show_legend:
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

def grafica_barras(df, path):
    variables = ['x1', 'x2', 'x3', 'f1', 'f2', 'f3', "f4", "f5", "f6"]

    plt.figure(figsize=(10, 6))
    colors = ['#b62c6e', '#ffcb56', '#00b1a9']
    bar_width = 0.15
    x = range(len(variables))

    for i, solution in enumerate(df['problema']):
        bar_data = df[variables].iloc[i].values
        plt.bar([p + bar_width * i for p in x], bar_data, bar_width, label=solution, color=colors[i % len(colors)])

    plt.title('Comparison of decision variables and objective functions', fontsize=16)
    plt.ylabel('Normalized value')
    plt.xticks([p + bar_width * (len(df['problema']) - 1) / 2 for p in x], variables, rotation=0)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(path)

def normalize_dataframe(df):
    df_max = df.max()
    df_max = df_max.where(df_max != 0, 1)  
    df_normalized = df / df_max
    return df_normalized

df_problem1 = pd.read_csv(f"C:/Users/noluc/OneDrive/Escritorio/multiobjetivo/problem1_solucion_1.csv")
df_problem2 = pd.read_csv(f"C:/Users/noluc/OneDrive/Escritorio/multiobjetivo/problem2_solucion_1.csv")
df_problem3 = pd.read_csv(f"C:/Users/noluc/OneDrive/Escritorio/multiobjetivo/problem3_solucion_1.csv")

columns_reference = df_problem3.columns
row1 = get_last_row_aligned(df_problem1, columns_reference)
row2 = get_last_row_aligned(df_problem2, columns_reference)
row3 = get_last_row_aligned(df_problem3, columns_reference)

path = 'C:/Users/noluc/OneDrive/Escritorio/radar1.jpg'
df_resultado = pd.concat([row1, row2, row3], ignore_index=True)
df_normalized = normalize_dataframe(df_resultado)
df_resultado["problema"] = ["Problem 1", "Problem 2", "Problem 3"]
df_normalized["problema"] = ["Problem 1", "Problem 2", "Problem 3"]
print(df_resultado)

path = 'C:/Users/noluc/OneDrive/Escritorio/radar1_barras.jpg'
grafica_barras(df_normalized, path)

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), subplot_kw=dict(polar=True))
# plot_radar(df_normalized, ['x1', 'x2', 'x3'], 'Variables de decisión', ax1, colors=['#b62c6e', '#ffcb56', '#00b1a9'], show_legend=True)
# plot_radar(df_normalized, ['f1', 'f2', 'f3', 'f4','f5'], 'Funciones objetivo optimizadas', ax2, colors=['#b62c6e', '#ffcb56', '#00b1a9'], show_legend=False)
# plt.tight_layout()
# plt.savefig('C:/Users/noluc/OneDrive/Escritorio/multiobjetivo/radar1.jpg')

# # df_resultado = pd.concat([row2, row3], ignore_index=True)
# # df_normalized = normalize_dataframe(df_resultado)
# # df_resultado["problema"] = ["Problema 2", "Problema 3"]
# # df_normalized["problema"] = ["Problema 2", "Problema 3"]
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), subplot_kw=dict(polar=True))
# plot_radar(df_normalized, ['x1', 'x2', 'x3'], 'Variables de decisión', ax1, colors=['#b62c6e', '#ffcb56', '#00b1a9'], show_legend=True)
# plot_radar(df_normalized, ['f1', 'f2', 'f3', 'f4','f5','f6'], 'Funciones objetivo optimizadas', ax2, colors=['#b62c6e', '#ffcb56', '#00b1a9'], show_legend=False)
# plt.tight_layout()
# plt.savefig('C:/Users/noluc/OneDrive/Escritorio/multiobjetivo/radar2.jpg')