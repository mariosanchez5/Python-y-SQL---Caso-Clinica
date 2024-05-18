# Módulo de configuración
# Este sencillo módulo lee la configuración de la applicación desde un archivo de configuración.
import os


CONFIG_FILES = ['config.yml', 'config.json', 'config.toml']

# Identificar el tipo de archivo de configuración
def identificar_tipo_config():
    for archivo in CONFIG_FILES:
        if os.path.exists(archivo):
            return archivo
    raise FileNotFoundError("No se encontró un archivo de configuración")

# Leer la configuración
def leer_config():
    archivo = identificar_tipo_config()
    if archivo.endswith('.yml'):
        import yaml
        with open(archivo) as f:
            return yaml.safe_load(f)
    elif archivo.endswith('.json'):
        import json
        with open(archivo) as f:
            return json.load(f)
    elif archivo.endswith('.toml'):
        import toml
        with open(archivo) as f:
            return toml.load(f)