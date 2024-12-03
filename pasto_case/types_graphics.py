import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Datos de ejemplo
aspects = ['Costo', 'Eficiencia', 'Impacto Ambiental', 'Aceptación Social']
options = ['Opción A', 'Opción B', 'Opción C']
data = np.array([
    [8, 7, 6, 9],  # Opción A
    [6, 8, 7, 7],  # Opción B
    [7, 6, 8, 6]   # Opción C
])

# Configuración para las gráficas
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
bar_width = 0.2
x_indexes = np.arange(len(aspects))

# Corregir dimensiones para la gráfica de radar
angles = np.linspace(0, 2 * np.pi, len(aspects), endpoint=False).tolist()
angles += angles[:1]  # Cerrar el gráfico radial

# Crear nueva figura para asegurar visualización clara
fig, axs = plt.subplots(5, 2, figsize=(16, 20))
axs = axs.ravel()

# Gráfica 1: Radar (ajustada)
axs[0] = plt.subplot(5, 2, 1, polar=True)  # Configurar gráfico polar

for i, option in enumerate(options):
    values = np.append(data[i], data[i][0])  # Añadir el primer valor al final para cerrar el radar
    axs[0].plot(angles, values, label=option, color=colors[i])
    axs[0].fill(angles, values, alpha=0.25, color=colors[i])
axs[0].set_xticks(angles[:-1])
axs[0].set_xticklabels(aspects)
axs[0].set_title('Gráfica de Radar')
axs[0].legend()

# Gráfica 2: Barras agrupadas
for i, option in enumerate(options):
    axs[1].bar(x_indexes + i * bar_width, data[i], bar_width, label=option, color=colors[i])
axs[1].set_xticks(x_indexes + bar_width)
axs[1].set_xticklabels(aspects)
axs[1].set_title('Gráfica de Barras Agrupadas')
axs[1].legend()

# Gráfica 3: Barras apiladas
for i in range(len(options)):
    axs[2].bar(aspects, data[i], label=options[i], bottom=np.sum(data[:i], axis=0), color=colors[i])
axs[2].set_title('Gráfica de Barras Apiladas')
axs[2].legend()

# Gráfica 4: Líneas múltiples
for i, option in enumerate(options):
    axs[3].plot(aspects, data[i], marker='o', label=option, color=colors[i])
axs[3].set_title('Gráfica de Líneas Múltiples')
axs[3].legend()

# Gráfica 5: Dispersión
for i, option in enumerate(options):
    axs[4].scatter(range(len(aspects)), data[i], label=option, color=colors[i])
axs[4].set_xticks(range(len(aspects)))
axs[4].set_xticklabels(aspects)
axs[4].set_title('Gráfica de Dispersión')
axs[4].legend()

# Gráfica 6: Burbujas
for i, option in enumerate(options):
    axs[5].scatter(range(len(aspects)), data[i], s=data[i] * 100, label=option, alpha=0.6, color=colors[i])
axs[5].set_xticks(range(len(aspects)))
axs[5].set_xticklabels(aspects)
axs[5].set_title('Gráfica de Burbujas')
axs[5].legend()

# Gráfica 7: Heatmap
heatmap_data = pd.DataFrame(data, index=options, columns=aspects)
axs[6].imshow(data, cmap='coolwarm', aspect='auto')
axs[6].set_xticks(range(len(aspects)))
axs[6].set_xticklabels(aspects)
axs[6].set_yticks(range(len(options)))
axs[6].set_yticklabels(options)
axs[6].set_title('Gráfica de Calor')

# Gráfica 8: Pirámide
y = np.arange(len(aspects))
axs[7].barh(y, data[0], label='Opción A', color=colors[0])
axs[7].barh(y, -data[1], label='Opción B', color=colors[1])
axs[7].set_yticks(y)
axs[7].set_yticklabels(aspects)
axs[7].set_title('Gráfica de Pirámide')
axs[7].legend()

# Gráfica 9: Pastel Comparativo (solo aspecto 1)
axs[8].pie(data[:, 0], labels=options, autopct='%1.1f%%', colors=colors, startangle=140)
axs[8].set_title('Gráfica de Pastel Comparativa (Costo)')

# Gráfica 10: Tabla con formato condicional
axs[9].axis('tight')
axs[9].axis('off')
table_data = np.vstack([['Aspectos'] + aspects] + [[options[i]] + list(data[i]) for i in range(len(options))])
axs[9].table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.15] * (len(aspects) + 1))
axs[9].set_title('Tabla Formato Condicional')

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import networkx as nx

# Datos de la matriz de comparación
criteria = [
    "Availability factor",
    "Driving range",
    "Accumulated cost",
    "Incentives",
    "Emissions"
]

# Matriz de comparación
matrix = [
    [1.00, 4.00, 5.00, 6.00, 7.00],
    [0.25, 1.00, 2.00, 3.00, 4.00],
    [0.20, 0.50, 1.00, 2.00, 3.00],
    [0.17, 0.33, 0.50, 1.00, 2.00],
    [0.14, 0.25, 0.33, 0.50, 1.00]
]

# Crear el grafo
G = nx.DiGraph()

# Añadir nodos
for criterion in criteria:
    G.add_node(criterion)

# Añadir aristas con pesos
for i, source in enumerate(criteria):
    for j, target in enumerate(criteria):
        if i != j:  # No incluir auto-conexiones
            G.add_edge(source, target, weight=matrix[i][j])

# Posiciones de los nodos en forma circular
pos = nx.circular_layout(G)

# Dibujar nodos
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue", alpha=0.8)

# Dibujar etiquetas de los nodos
nx.draw_networkx_labels(G, pos, font_size=10, font_color="black", font_weight="bold")

# Dibujar aristas con ancho proporcional al peso
edges = G.edges(data=True)
weights = [edge[2]['weight'] for edge in edges]
nx.draw_networkx_edges(G, pos, edgelist=edges, width=[w * 0.5 for w in weights], edge_color="gray", alpha=0.6, arrows=True)

# Añadir etiquetas a las aristas (valores de la matriz)
edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Título del gráfico
plt.title("Network Graph: Pair-wise Comparison Matrix", fontsize=12)
plt.axis("off")
plt.show()
