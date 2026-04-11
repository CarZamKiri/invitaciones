import json
import os
from jinja2 import Environment, FileSystemLoader

# 1. Definir rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 2. Configurar Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

print("Iniciando generación masiva de invitaciones...\n")

# 3. Recorrer todos los archivos JSON en la carpeta data/
for filename in os.listdir(DATA_DIR):
    if filename.endswith('.json'):
        filepath = os.path.join(DATA_DIR, filename)
        
        # --- NUEVA DEFENSA CONTRA ERRORES AQUÍ ---
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                datos_cliente = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️  Saltando {filename}: El archivo está vacío o tiene un error de sintaxis (¿falta una coma?).")
            continue # Salta a la siguiente iteración del ciclo sin romper el script
        # -----------------------------------------

        # 4. Identificar la plantilla
        nombre_plantilla = datos_cliente.get('plantilla', 'boda.html')
        
        try:
            template = env.get_template(nombre_plantilla)
            html_final = template.render(datos_cliente)
            
            # 5. Guardar el archivo
            nombre_salida = filename.replace('.json', '.html')
            output_file = os.path.join(OUTPUT_DIR, nombre_salida)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_final)
                
            print(f"✅ Éxito: {nombre_salida} (usando la plantilla '{nombre_plantilla}')")
            
        except Exception as e:
            print(f"❌ Error al procesar {filename}: {e}")

print("\n¡Proceso finalizado! Revisa tu carpeta 'output'.")