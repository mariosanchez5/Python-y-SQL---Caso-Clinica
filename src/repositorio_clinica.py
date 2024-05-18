from src.config import leer_config

config = leer_config()

if config['repositorio'] == 'sql':
    try:
        from src.implementaciones.sql_repositorio_clinica import *
    except ImportError:
        raise ImportError("No se encontró el módulo sql_repositorio_clinica")
else:
    try:
        from src.implementaciones.dummy_repositorio_clinica import *
    except ImportError:
        raise ImportError("No se encontró el módulo dummy_repositorio_clinica")