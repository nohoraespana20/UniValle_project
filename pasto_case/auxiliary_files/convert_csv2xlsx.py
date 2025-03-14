import os
import pandas as pd


input_folder = "C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L1_home"  
output_folder = "C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L1_home"  

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):

    if file_name.endswith(".csv"):
        csv_path = os.path.join(input_folder, file_name)
        file_base_name = os.path.splitext(file_name)[0]
        xlsx_path = os.path.join(output_folder, f"{file_base_name}.xlsx")
        
        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                print(f"Advertencia: {file_name} está vacío. Se omite.")
                continue
            df.to_excel(xlsx_path, index=False)
            print(f"Convertido: {file_name} -> {file_base_name}.xlsx")
        
        except pd.errors.EmptyDataError:
            print(f"Error: {file_name} no contiene datos válidos. Se omite.")
        except Exception as e:
            print(f"Error inesperado al procesar {file_name}: {e}")