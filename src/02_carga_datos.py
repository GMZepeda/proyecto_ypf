import pandas as pd
from sqlalchemy import create_engine
import urllib

# 1. Configuración de la conexión
# Reemplazá 'TU_SERVIDOR' por el nombre de tu servidor SQL (ej. 'localhost\\SQLEXPRESS')
server = r'LAPTOP-KM7AEC0L\SQLEXPRESS' 
database = 'DATAFUEL_SA'
driver = 'ODBC Driver 17 for SQL Server' # Verificá si tenés esta versión u otra (ej. 18)

# 2. Crear el motor de conexión con SQLAlchemy
params = urllib.parse.quote_plus(f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

def cargar_datos():
    try:
        print("Conectando a la base de datos...")
        
        # 3. Extracción (Extract)
        df_categorias = pd.read_csv('data/raw/Categorias.csv', encoding='latin-1')
        
        # Transformación (Transform): Pandas ya infirió los tipos en el EDA, 
        # asumiendo que los nombres de columnas del CSV coinciden con los de SQL.
        
        # 4. Carga (Load)
        print("Cargando Dim_Categorias...")
        df_categorias.to_sql('Dim_Categorias', con=engine, if_exists='append', index=False)
        
        print("Carga finalizada con éxito.")
        
    except Exception as e:
        print(f"Error durante la carga: {e}")

if __name__ == '__main__':
    cargar_datos()