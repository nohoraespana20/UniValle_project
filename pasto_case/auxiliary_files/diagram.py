import pandas as pd
import sqlite3

# Cargar el archivo Excel
file_path = "C:/Users/noluc/OneDrive/Escritorio/clasificacion.xlsx"  # Asegúrate de usar la ruta correcta

xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name="Hoja1")

# Reemplazar nombres de PAPER por números
paper_mapping = {paper: f"P{idx+1}" for idx, paper in enumerate(df["PAPER"].dropna().unique())}
df["PAPER"] = df["PAPER"].map(paper_mapping)

# Crear conexión a SQLite
db_path = "relations.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tablas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Papers (
    id TEXT PRIMARY KEY
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Factors (
    id TEXT PRIMARY KEY
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Stakeholders (
    id TEXT PRIMARY KEY
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Relations (
    source TEXT,
    target TEXT,
    weight INTEGER,
    FOREIGN KEY(source) REFERENCES Papers(id),
    FOREIGN KEY(target) REFERENCES Factors(id),
    FOREIGN KEY(target) REFERENCES Stakeholders(id)
);
""")

# Insertar datos en las tablas
papers = [(p,) for p in paper_mapping.values()]
factors = [(f,) for f in df["FACTORS"].dropna().unique()]
stakeholders = [(s,) for s in df["STAKEHOLDERS"].dropna().unique()]

cursor.executemany("INSERT OR IGNORE INTO Papers (id) VALUES (?)", papers)
cursor.executemany("INSERT OR IGNORE INTO Factors (id) VALUES (?)", factors)
cursor.executemany("INSERT OR IGNORE INTO Stakeholders (id) VALUES (?)", stakeholders)

# Insertar relaciones con pesos
from collections import Counter

relations = []
for _, row in df.dropna().iterrows():
    paper = str(row["PAPER"]).strip()
    factor = str(row["FACTORS"]).strip()
    stakeholder = str(row["STAKEHOLDERS"]).strip()
    
    if paper and factor:
        relations.append((paper, factor))
    if factor and stakeholder:
        relations.append((factor, stakeholder))
    if paper and stakeholder:
        relations.append((paper, stakeholder))
    
    if paper and factor and stakeholder:
        relations.append((paper, stakeholder))
        relations.append((factor, paper))
        relations.append((stakeholder, paper))
        relations.append((stakeholder, factor))

relations_count = Counter(relations)
relations_data = [(src, tgt, weight) for (src, tgt), weight in relations_count.items()]

cursor.executemany("INSERT INTO Relations (source, target, weight) VALUES (?, ?, ?)", relations_data)

# Guardar y cerrar conexión
conn.commit()
conn.close()

print("Base de datos creada exitosamente en 'relations.db'")
