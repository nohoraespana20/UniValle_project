import pandas as pd
import numpy as np
import os
from enum import Enum

class Performance(Enum):
    EXCELLENT = "Excelente"
    GOOD = "Bueno" 
    ACCEPTABLE = "Aceptable"
    POOR = "Malo"

class PerformanceEvaluator:
    """
    Evaluador automático de rendimiento para algoritmos de optimización multiobjetivo.
    """
    
    def __init__(self, problem_type="engineering"):
        """
        Inicializa el evaluador con umbrales específicos del tipo de problema.
        
        Args:
            problem_type: "benchmark" para problemas de prueba estándar, 
                         "engineering" para problemas de ingeniería real
        """
        self.problem_type = problem_type
        self.thresholds = self._get_thresholds()
        
    def _get_thresholds(self):
        """Define umbrales según el tipo de problema."""
        if self.problem_type == "benchmark":
            return {
                'igd': {'excellent': 0.005, 'good': 0.02, 'acceptable': 0.05},
                'gd': {'excellent': 0.001, 'good': 0.005, 'acceptable': 0.02},
                'hypervolume': {'excellent': 0.95, 'good': 0.85, 'acceptable': 0.70},
                'spacing': {'excellent': 0.05, 'good': 0.1, 'acceptable': 0.2},
                'n_solutions': {'excellent': 100, 'good': 50, 'acceptable': 20},
                'execution_time': {'excellent': 10, 'good': 30, 'acceptable': 60}
            }
        else:  # engineering
            return {
                'igd': {'excellent': 0.01, 'good': 0.05, 'acceptable': 0.1},
                'gd': {'excellent': 0.005, 'good': 0.02, 'acceptable': 0.05},
                'hypervolume': {'excellent': 0.80, 'good': 0.60, 'acceptable': 0.40},
                'spacing': {'excellent': 0.1, 'good': 0.5, 'acceptable': 1.0},
                'n_solutions': {'excellent': 50, 'good': 30, 'acceptable': 15},
                'execution_time': {'excellent': 30, 'good': 60, 'acceptable': 120}
            }
    
    def evaluate_metric(self, metric_name, value):
        """
        Evalúa una métrica individual.
        
        Args:
            metric_name: Nombre de la métrica
            value: Valor de la métrica
            
        Returns:
            Performance enum indicating the performance level
        """
        if metric_name not in self.thresholds or value is None or pd.isna(value):
            return Performance.POOR
            
        thresholds = self.thresholds[metric_name]
        
        # Métricas donde menor es mejor
        if metric_name in ['igd', 'gd', 'igd_plus', 'gd_plus', 'spacing', 'execution_time']:
            if value <= thresholds['excellent']:
                return Performance.EXCELLENT
            elif value <= thresholds['good']:
                return Performance.GOOD
            elif value <= thresholds['acceptable']:
                return Performance.ACCEPTABLE
            else:
                return Performance.POOR
                
        # Métricas donde mayor es mejor
        elif metric_name in ['hypervolume', 'n_solutions', 'diversity']:
            if value >= thresholds['excellent']:
                return Performance.EXCELLENT
            elif value >= thresholds['good']:
                return Performance.GOOD
            elif value >= thresholds['acceptable']:
                return Performance.ACCEPTABLE
            else:
                return Performance.POOR
        
        return Performance.POOR
    
    def evaluate_overall_performance(self, metrics_dict):
        """
        Evalúa el rendimiento general basado en múltiples métricas.
        
        Args:
            metrics_dict: Diccionario con valores de métricas
            
        Returns:
            Tuple with (overall_performance, detailed_evaluation)
        """
        evaluations = {}
        scores = {'Excelente': 4, 'Bueno': 3, 'Aceptable': 2, 'Malo': 1}
        weights = {
            'hypervolume': 0.25,
            'igd': 0.20,
            'spacing': 0.15,
            'gd': 0.15,
            'n_solutions': 0.10,
            'execution_time': 0.10,
            'diversity': 0.05
        }
        
        total_score = 0
        total_weight = 0
        
        for metric, value in metrics_dict.items():
            if metric in weights:
                evaluation = self.evaluate_metric(metric, value)
                evaluations[metric] = evaluation.value
                
                score = scores[evaluation.value]
                weight = weights[metric]
                total_score += score * weight
                total_weight += weight
        
        # Calcular puntuación promedio ponderada
        if total_weight > 0:
            avg_score = total_score / total_weight
            if avg_score >= 3.5:
                overall = Performance.EXCELLENT
            elif avg_score >= 2.5:
                overall = Performance.GOOD
            elif avg_score >= 1.5:
                overall = Performance.ACCEPTABLE
            else:
                overall = Performance.POOR
        else:
            overall = Performance.POOR
            
        return overall.value, evaluations
    
    def generate_performance_report(self, metrics_df, output_path=None):
        """
        Genera un reporte completo de rendimiento.
        
        Args:
            metrics_df: DataFrame con métricas por año
            output_path: Ruta para guardar el reporte (opcional)
            
        Returns:
            DataFrame with performance evaluations
        """
        report_data = []
        
        for index, row in metrics_df.iterrows():
            year = row.get('Año', index + 1)
            
            # Evaluar cada métrica
            overall_perf, detailed_eval = self.evaluate_overall_performance(row.to_dict())
            
            report_row = {
                'Año': year,
                'Rendimiento_General': overall_perf,
                'Puntuacion_Numerica': self._get_numeric_score(overall_perf),
                'HV_Evaluacion': detailed_eval.get('hypervolume', 'N/A'),
                'IGD_Evaluacion': detailed_eval.get('igd', 'N/A'),
                'GD_Evaluacion': detailed_eval.get('gd', 'N/A'),
                'Spacing_Evaluacion': detailed_eval.get('spacing', 'N/A'),
                'Tiempo_Evaluacion': detailed_eval.get('execution_time', 'N/A'),
                'NSol_Evaluacion': detailed_eval.get('n_solutions', 'N/A'),
                'Recomendaciones': self._generate_recommendations(detailed_eval, row.to_dict())
            }
            
            report_data.append(report_row)
        
        report_df = pd.DataFrame(report_data)
        
        if output_path:
            report_df.to_csv(output_path, index=False)
            
        return report_df
    
    def _get_numeric_score(self, performance_text):
        """Convierte evaluación textual a puntuación numérica."""
        scores = {'Excelente': 4, 'Bueno': 3, 'Aceptable': 2, 'Malo': 1}
        return scores.get(performance_text, 1)
    
    def _generate_recommendations(self, detailed_eval, metrics):
        """Genera recomendaciones específicas basadas en las evaluaciones."""
        recommendations = []
        
        # Recomendaciones por métrica
        if detailed_eval.get('igd') == 'Malo':
            recommendations.append("Mejorar convergencia: aumentar generaciones o ajustar mutación")
            
        if detailed_eval.get('spacing') == 'Malo':
            recommendations.append("Mejorar diversidad: aumentar población o parámetros de diversidad")
            
        if detailed_eval.get('execution_time') == 'Malo':
            recommendations.append("Optimizar eficiencia: reducir población o generaciones")
            
        if detailed_eval.get('n_solutions') == 'Malo':
            recommendations.append("Obtener más soluciones: ajustar parámetros de selección")
            
        if detailed_eval.get('hypervolume') == 'Malo':
            recommendations.append("Mejorar calidad general: revisar formulación del problema")
        
        return "; ".join(recommendations) if recommendations else "Rendimiento satisfactorio"
    
    def compare_algorithms(self, metrics_dict_list, algorithm_names):
        """
        Compara múltiples algoritmos basado en sus métricas.
        
        Args:
            metrics_dict_list: Lista de diccionarios con métricas de cada algoritmo
            algorithm_names: Lista con nombres de los algoritmos
            
        Returns:
            DataFrame with comparison results
        """
        comparison_data = []
        
        for i, (metrics, name) in enumerate(zip(metrics_dict_list, algorithm_names)):
            overall_perf, detailed_eval = self.evaluate_overall_performance(metrics)
            
            comparison_row = {
                'Algoritmo': name,
                'Rendimiento_General': overall_perf,
                'Puntuacion': self._get_numeric_score(overall_perf),
                'HV': metrics.get('hypervolume', 'N/A'),
                'IGD': metrics.get('igd', 'N/A'),
                'Spacing': metrics.get('spacing', 'N/A'),
                'Tiempo': metrics.get('execution_time', 'N/A')
            }
            
            comparison_data.append(comparison_row)
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('Puntuacion', ascending=False)
        
        return comparison_df

def analyze_performance_trends(metrics_csv_path):
    """
    Analiza tendencias de rendimiento a lo largo del tiempo.
    
    Args:
        metrics_csv_path: Ruta al archivo CSV con métricas
        
    Returns:
        Dictionary with trend analysis
    """
    df = pd.read_csv(metrics_csv_path)
    
    trends = {}
    
    # Analizar tendencias para métricas clave
    key_metrics = ['hypervolume', 'igd', 'spacing', 'execution_time']
    
    for metric in key_metrics:
        if metric in df.columns:
            values = df[metric].dropna()
            if len(values) > 1:
                # Calcular tendencia (correlación con el tiempo)
                years = df['Año'][:len(values)]
                correlation = np.corrcoef(years, values)[0, 1]
                
                trend_direction = "Mejorando" if (
                    (metric in ['hypervolume', 'diversity'] and correlation > 0.1) or
                    (metric in ['igd', 'spacing', 'execution_time'] and correlation < -0.1)
                ) else "Empeorando" if (
                    (metric in ['hypervolume', 'diversity'] and correlation < -0.1) or
                    (metric in ['igd', 'spacing', 'execution_time'] and correlation > 0.1)
                ) else "Estable"
                
                trends[metric] = {
                    'direction': trend_direction,
                    'correlation': correlation,
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'best_year': df.loc[values.idxmax() if metric in ['hypervolume', 'diversity'] 
                                      else values.idxmin(), 'Año']
                }
    
    return trends

# Ejemplo de uso
def evaluate_algorithm_performance(metrics_csv_path, output_dir):
    """
    Función principal para evaluar el rendimiento del algoritmo.
    """
    # Cargar métricas
    metrics_df = pd.read_csv(metrics_csv_path)
    
    # Crear evaluador
    evaluator = PerformanceEvaluator(problem_type="engineering")
    
    # Generar reporte de rendimiento
    report_path = os.path.join(output_dir, "reporte_rendimiento.csv")
    performance_report = evaluator.generate_performance_report(metrics_df, report_path)
    
    # Analizar tendencias
    trends = analyze_performance_trends(metrics_csv_path)
    
    # Generar resumen
    print("=== RESUMEN DE RENDIMIENTO ===")
    print(f"Años analizados: {len(metrics_df)}")
    print(f"Rendimiento promedio: {performance_report['Rendimiento_General'].mode().iloc[0]}")
    print(f"Mejor año: {performance_report.loc[performance_report['Puntuacion_Numerica'].idxmax(), 'Año']}")
    print(f"Peor año: {performance_report.loc[performance_report['Puntuacion_Numerica'].idxmin(), 'Año']}")
    
    print("\n=== TENDENCIAS ===")
    for metric, trend_data in trends.items():
        print(f"{metric}: {trend_data['direction']} (correlación: {trend_data['correlation']:.3f})")
    
    print(f"\nReporte detallado guardado en: {report_path}")
    
    return performance_report, trends

# Ejecutar evaluación (descomenta las siguientes líneas para usar)
metrics_path = "C:/Nohora/UniValle_project/pasto_case/metricas_rendimiento.csv"
output_dir = "C:/Nohora/UniValle_project/pasto_case/"
report, trends = evaluate_algorithm_performance(metrics_path, output_dir)