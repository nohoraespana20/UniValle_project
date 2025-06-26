import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configurar el estilo de matplotlib
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 9

def load_solutions(base_path="C:/Nohora/UniValle_project/pasto_case/opt_mejorado_3"):
    """Cargar todas las soluciones desde los archivos CSV"""
    solutions = {}
    
    for i in range(1, 6):
        file_path = Path(base_path) / f"solucion_{i}.csv"
        try:
            # Leer el CSV y limpiar los nombres de columnas
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()  # Eliminar espacios en blanco
            solutions[i] = df
            print(f"Solución {i} cargada: {len(df)} filas")
        except FileNotFoundError:
            print(f"Archivo no encontrado: {file_path}")
        except Exception as e:
            print(f"Error cargando solución {i}: {e}")
    
    return solutions

def create_comparison_plots(solutions):
    """Crear gráficos de comparación de soluciones"""
    
    # Crear figura con subplots
    fig = plt.figure(figsize=(17, 10))
    
    # Definir colores para cada solución
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # OPCIÓN 1: Leyenda común en la parte superior de la figura
    # Crear elementos de leyenda una sola vez
    legend_elements = []
    if 1 in solutions:
        legend_elements.append(plt.Line2D([0], [0], color=colors[0], linewidth=2, 
                                        label='Solution 1', alpha=0.9))
    
    for i in range(2, 6):
        if i in solutions:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w',
                                            markerfacecolor=colors[i-1], markersize=8,
                                            label=f'Solution {i}', alpha=0.6,
                                            linestyle='None'))
    
    # ========== SUBPLOT 1: tL2 ==========
    ax1 = plt.subplot(3, 3, 1)
    
    # Graficar solución 1 como línea principal (sin label)
    if 1 in solutions:
        ax1.plot(solutions[1]['Año'], solutions[1]['tL2'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    # Graficar otras soluciones como dispersiones (sin label)
    for i in range(2, 6):
        if i in solutions:
            ax1.scatter(solutions[i]['Año'], solutions[i]['tL2'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Time [hours]')
    ax1.set_title('Time operation for L2 type chargers')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 25)
    
    # ========== SUBPLOT 2: tL3 ==========
    ax2 = plt.subplot(3, 3, 2)
    
    if 1 in solutions:
        ax2.plot(solutions[1]['Año'], solutions[1]['tL3'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax2.scatter(solutions[i]['Año'], solutions[i]['tL3'], 
                       color=colors[i-1], alpha=0.6, s=30)
    
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Time [hours]')
    ax2.set_title('Time operation for L3 type chargers')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 25)
    
    # ========== SUBPLOT 3: Area ==========
    ax3 = plt.subplot(3, 3, 3)
    
    if 1 in solutions:
        ax3.plot(solutions[1]['Año'], solutions[1]['area'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax3.scatter(solutions[i]['Año'], solutions[i]['area'], 
                       color=colors[i-1], alpha=0.6, s=30)
    
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Area ($m^2$)')
    ax3.set_title('Total land area')
    ax3.grid(True, alpha=0.3)
    
    # ========== SUBPLOT 4: cpl2 ==========
    ax4 = plt.subplot(3, 3, 4)

    if 1 in solutions:
        ax4.plot(solutions[1]['Año'], solutions[1]['cpl2'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax4.scatter(solutions[i]['Año'], solutions[i]['cpl2'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Number of chargers')
    ax4.set_title('L2 type chargers required')
    ax4.grid(True, alpha=0.3)
    
    # ========== SUBPLOT 5: cpl3 ==========
    ax5 = plt.subplot(3, 3, 5)
    
    if 1 in solutions:
        ax5.plot(solutions[1]['Año'], solutions[1]['cpl3'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax5.scatter(solutions[i]['Año'], solutions[i]['cpl3'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax5.set_xlabel('Year')
    ax5.set_ylabel('Number of chargers')
    ax5.set_title('L3 type chargers required')
    ax5.grid(True, alpha=0.3)

    # ========== SUBPLOT 6: S_refor ==========
    ax6 = plt.subplot(3, 3, 6)
    
    if 1 in solutions:
        ax6.plot(solutions[1]['Año'], solutions[1]['S_refor'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax6.scatter(solutions[i]['Año'], solutions[i]['S_refor'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax6.set_xlabel('Year')
    ax6.set_ylabel('$S_{refor}$ (%)')
    ax6.set_title('Power grid reinforcement required')
    ax6.grid(True, alpha=0.3)

    # ========== SUBPLOT 7: Jobs ==========
    ax7 = plt.subplot(3, 3, 7)
            
    if 1 in solutions:
        ax7.plot(solutions[1]['Año'], solutions[1]['jobs'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax7.scatter(solutions[i]['Año'], solutions[i]['jobs'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax7.set_xlabel('Year')
    ax7.set_ylabel('Number of jobs')
    ax7.set_title('Jobs generated')
    ax7.grid(True, alpha=0.3)

    # ========== SUBPLOT 8: Emissions ==========
    ax8 = plt.subplot(3, 3, 8)
            
    if 1 in solutions:
        ax8.plot(solutions[1]['Año'], solutions[1]['emisiones']/1000000, 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax8.scatter(solutions[i]['Año'], solutions[i]['emisiones']/1000000, 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax8.set_xlabel('Year')
    ax8.set_ylabel('Ton CO2')
    ax8.set_title('CO2 emissions generated')
    ax8.grid(True, alpha=0.3)

    # ========== SUBPLOT 9: incentivos ==========
    ax9 = plt.subplot(3, 3, 9)
            
    if 1 in solutions:
        ax9.plot(solutions[1]['Año'], solutions[1]['incentivos']/1000000, 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax9.scatter(solutions[i]['Año'], solutions[i]['incentivos']/1000000, 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax9.set_xlabel('Year')
    ax9.set_ylabel('USD/kWh')
    ax9.set_title('Power income index')
    ax9.grid(True, alpha=0.3)
    
    # Ajustar espaciado para hacer lugar a la leyenda
    plt.tight_layout()
    
    # LEYENDA COMÚN - Agregar en la parte superior de la figura
    fig.legend(handles=legend_elements, loc='center right', 
              bbox_to_anchor=(0.98, 0.5), 
              frameon=True, fancybox=True, shadow=True)
    
    # Ajustar el espaciado superior para la leyenda
    plt.subplots_adjust(right=0.91)
    
    return fig

# ALTERNATIVA: Función con leyenda lateral
def create_comparison_plots_side_legend(solutions):
    """Crear gráficos de comparación con leyenda lateral"""
    
    # Crear figura con subplots y espacio para leyenda
    fig = plt.figure(figsize=(15, 15))  # Figura más ancha
    
    # Definir colores para cada solución
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Crear elementos de leyenda
    legend_elements = []
    if 1 in solutions:
        legend_elements.append(plt.Line2D([0], [0], color=colors[0], linewidth=2, 
                                        label='Solution 1', alpha=0.9))
    
    for i in range(2, 6):
        if i in solutions:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w',
                                            markerfacecolor=colors[i-1], markersize=8,
                                            label=f'Solution {i}', alpha=0.6,
                                            linestyle='None'))
    
    # Crear subplots (misma lógica que antes, sin labels individuales)
    # ========== SUBPLOT 1: tL2 ==========
    ax1 = plt.subplot(3, 3, 1)
    
    # Graficar solución 1 como línea principal (sin label)
    if 1 in solutions:
        ax1.plot(solutions[1]['Año'], solutions[1]['tL2'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    # Graficar otras soluciones como dispersiones (sin label)
    for i in range(2, 6):
        if i in solutions:
            ax1.scatter(solutions[i]['Año'], solutions[i]['tL2'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Time [hours]')
    ax1.set_title('Time operation for L2 type chargers')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 25)
    
    # ========== SUBPLOT 2: tL3 ==========
    ax2 = plt.subplot(3, 3, 2)
    
    if 1 in solutions:
        ax2.plot(solutions[1]['Año'], solutions[1]['tL3'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax2.scatter(solutions[i]['Año'], solutions[i]['tL3'], 
                       color=colors[i-1], alpha=0.6, s=30)
    
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Time [hours]')
    ax2.set_title('Time operation for L3 type chargers')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 25)
    
    # ========== SUBPLOT 3: Area ==========
    ax3 = plt.subplot(3, 3, 3)
    
    if 1 in solutions:
        ax3.plot(solutions[1]['Año'], solutions[1]['area'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax3.scatter(solutions[i]['Año'], solutions[i]['area'], 
                       color=colors[i-1], alpha=0.6, s=30)
    
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Area ($m^2$)')
    ax3.set_title('Total land area')
    ax3.grid(True, alpha=0.3)
    
    # ========== SUBPLOT 4: cpl2 ==========
    ax4 = plt.subplot(3, 3, 4)

    if 1 in solutions:
        ax4.plot(solutions[1]['Año'], solutions[1]['cpl2'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax4.scatter(solutions[i]['Año'], solutions[i]['cpl2'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Number of chargers')
    ax4.set_title('L2 type chargers required')
    ax4.grid(True, alpha=0.3)
    
    # ========== SUBPLOT 5: cpl3 ==========
    ax5 = plt.subplot(3, 3, 5)
    
    if 1 in solutions:
        ax5.plot(solutions[1]['Año'], solutions[1]['cpl3'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax5.scatter(solutions[i]['Año'], solutions[i]['cpl3'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax5.set_xlabel('Year')
    ax5.set_ylabel('Number of chargers')
    ax5.set_title('L3 type chargers required')
    ax5.grid(True, alpha=0.3)

    # ========== SUBPLOT 6: S_refor ==========
    ax6 = plt.subplot(3, 3, 6)
    
    if 1 in solutions:
        ax6.plot(solutions[1]['Año'], solutions[1]['S_refor'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax6.scatter(solutions[i]['Año'], solutions[i]['S_refor'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax6.set_xlabel('Year')
    ax6.set_ylabel('$S_{refor}$ (%)')
    ax6.set_title('Power grid reinforcement required')
    ax6.grid(True, alpha=0.3)

    # ========== SUBPLOT 7: Jobs ==========
    ax7 = plt.subplot(3, 3, 7)
            
    if 1 in solutions:
        ax7.plot(solutions[1]['Año'], solutions[1]['jobs'], 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax7.scatter(solutions[i]['Año'], solutions[i]['jobs'], 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax7.set_xlabel('Year')
    ax7.set_ylabel('Number of jobs')
    ax7.set_title('Jobs generated')
    ax7.grid(True, alpha=0.3)

    # ========== SUBPLOT 8: Emissions ==========
    ax8 = plt.subplot(3, 3, 8)
            
    if 1 in solutions:
        ax8.plot(solutions[1]['Año'], solutions[1]['emisiones']/1000000, 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax8.scatter(solutions[i]['Año'], solutions[i]['emisiones']/1000000, 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax8.set_xlabel('Year')
    ax8.set_ylabel('Ton CO2')
    ax8.set_title('CO2 emissions generated')
    ax8.grid(True, alpha=0.3)

    # ========== SUBPLOT 9: incentivos ==========
    ax9 = plt.subplot(3, 3, 9)
            
    if 1 in solutions:
        ax9.plot(solutions[1]['Año'], solutions[1]['incentivos']/1000000, 
                color=colors[0], linewidth=2, alpha=0.9)
    
    for i in range(2, 6):
        if i in solutions:
            ax9.scatter(solutions[i]['Año'], solutions[i]['incentivos']/1000000, 
                       color=colors[i-1], alpha=0.5, s=30)
    
    ax9.set_xlabel('Year')
    ax9.set_ylabel('USD/kWh')
    ax9.set_title('Power income index')
    ax9.grid(True, alpha=0.3)
    
    # Leyenda lateral
    fig.legend(handles=legend_elements, loc='center right', 
              bbox_to_anchor=(0.98, 0.5), frameon=True, 
              fancybox=True, shadow=True)
    
    # Ajustar espaciado
    plt.subplots_adjust(right=0.91)
    
    return fig

def generate_statistics_table(solutions):
    """Generar tabla de estadísticas comparativas"""
    stats = []
    
    for i, sol in solutions.items():
        stats.append({
            'Solución': i,
            'tL2_promedio': sol['tL2'].mean(),
            'tL2_std': sol['tL2'].std(),
            'tL3_promedio': sol['tL3'].mean(),
            'tL3_std': sol['tL3'].std(),
            'area_promedio': sol['area'].mean(),
            'area_std': sol['area'].std(),
            'cpl2_final': sol['cpl2'].iloc[-1],
            'cpl3_final': sol['cpl3'].iloc[-1],
            'S_refor_final': sol['S_refor'].iloc[-1],
            'jobs': sol['jobs'].iloc[-1],
        })
    
    return pd.DataFrame(stats)

def main():
    """Función principal para ejecutar el análisis"""
    
    # Cargar soluciones
    print("Cargando soluciones...")
    solutions = load_solutions()
    
    if not solutions:
        print("No se pudieron cargar las soluciones. Verifica las rutas de archivo.")
        return
    
    # Crear gráficos
    print("Generando gráficos...")
    fig = create_comparison_plots(solutions)
    
    # Generar estadísticas
    print("Generando estadísticas...")
    stats_df = generate_statistics_table(solutions)
    print("\nEstadísticas comparativas:")
    print(stats_df.round(2))
    
    # Análisis de convergencia
    print("\nAnálisis de convergencia:")
    for i in range(2, 6):
        if i in solutions and 1 in solutions:
            diff_tL2 = np.mean(np.abs(solutions[i]['tL2'] - solutions[1]['tL2']))
            diff_tL3 = np.mean(np.abs(solutions[i]['tL3'] - solutions[1]['tL3']))
            diff_area = np.mean(np.abs(solutions[i]['area'] - solutions[1]['area']))
            
            print(f"Solución {i} vs Solución 1:")
            print(f"  - Diferencia promedio tL2: {diff_tL2:.2f} horas")
            print(f"  - Diferencia promedio tL3: {diff_tL3:.2f} horas")
            print(f"  - Diferencia promedio área: {diff_area:.2f} m²")
    
    # Mostrar gráfico
    plt.show()
    
    # Guardar gráfico
    try:
        fig.savefig('C:/Nohora/UniValle_project/pasto_case/opt_mejorado_3/analisis_soluciones_multicriterio_3.png', 
                   dpi=300, bbox_inches='tight')
        print("\nGráfico guardado como 'analisis_soluciones_multicriterio_3.png'")
    except Exception as e:
        print(f"Error al guardar el gráfico: {e}")

if __name__ == "__main__":
    main()