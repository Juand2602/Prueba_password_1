import sqlite3
import csv
import os

# --- Configuración ---
db_file = 'database.sqlite'  # Nombre de tu archivo de base de datos
output_dir = 'csv_data'      # Directorio donde se guardarán los CSV
# -------------------

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Conectar a la base de datos SQLite
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Obtener la lista de todas las tablas en la base de datos
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print(f"Encontradas {len(tables)} tablas. Exportando a CSV...")

# Iterar sobre cada tabla
for table_name_tuple in tables:
    table_name = table_name_tuple[0]
    output_file = os.path.join(output_dir, f"{table_name}.csv")

    print(f"Exportando tabla '{table_name}' a '{output_file}'...")

    try:
        # Seleccionar todos los datos de la tabla
        cursor.execute(f"SELECT * FROM {table_name}")

        # Abrir el archivo CSV para escritura
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Escribir la cabecera (nombres de las columnas)
            csv_writer.writerow([description[0] for description in cursor.description])

            # Escribir todas las filas de datos
            csv_writer.writerows(cursor)

        print(f"Tabla '{table_name}' exportada con éxito.")

    except Exception as e:
        print(f"Error exportando la tabla {table_name}: {e}")

# Cerrar la conexión a la base de datos
conn.close()
print("¡Proceso completado!")
