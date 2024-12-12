import matplotlib.pyplot as plt
import numpy as np

# Datos
categories = ['Production', 'Utilization', 'Recycling']
technologies = ['ICEV', 'EV', 'NGV', 'PHEV']
data = {
    'Production': [4076.64, 34281.9, 4076.64, 13490.4],
    'Utilization': [267691.0, 28178.0, 183157.0, 58018.5],
    'Recycling': [2619.42, 20341.6, 2619.42, 8290.0]
}

# Función para mostrar porcentaje y valor real
def autopct_with_values(pct, all_vals):
    total = sum(all_vals)
    value = int(round(pct * total / 100.0))  # Calcular el valor real
    return f'{pct:.2f}%\n{value}'

# Crear subplots
fig, axs = plt.subplots(1, 3, figsize=(18, 7))

# Colores personalizados
colors = ['#620062', '#f4814b', '#ffbc4f', '#006cbe']

# Generar gráficos de pie
for i, category in enumerate(categories):
    wedges, texts, autotexts = axs[i].pie(
        data[category], 
        labels=technologies, 
        autopct=lambda pct: autopct_with_values(pct, data[category]),
        startangle=90, 
        colors=colors
    )
    axs[i].set_title(category+' [kg CO2−eq.]')
    for text in autotexts:
        text.set_color('black')  # Ajustar color de los valores

# Mostrar el gráfico
plt.tight_layout()
plt.show()
