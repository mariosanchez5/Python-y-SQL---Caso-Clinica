# Tarea 4 - Grupo 29
## Integrantes
- Richard Torres
- Yeycol Leiva
- Francisco Gálvez
- Nicolás Hermosilla
- Mario Sánchez

## Estructura del proyecto
El proyecto se compone de los siguientes archivos:
- `main.py`: Archivo principal del programa, donde se encuentra la lógica principal.
- `src/`: Carpeta que contiene los archivos de código fuente. En ella se encuentran los diferentes módulos que componen el programa. Hay una carpeta dentro:
    - `implementaciones`: Contiene la implementación de las funciones que se utilizan para acceder a la base de datos. Son reemplazables entre si, ya que todas tienen la misma interfaz. La que se debe usar para la ejecución del programa es la `sql`.
- `config.yml`: Archivo de configuración del programa. En él se encuentran los parámetros de configuración del programa, como la base de datos a la que se conectará. Su estructura es la siguiente:

```yaml
repositorio: sql # Nombre de la implementación de la base de datos a utilizar
sql: # Configuración de la base de datos PostgreSQL
    conexion:
        host: localhost # Host de la base de datos
        port: 5432 # Puerto de la base de datos
        dbname: clinica # Nombre de la base de datos
        user: postgres # Usuario de la base de datos
        password: postgres # Contraseña de la base de datos
schemas_dir: schemas # Directorio donde se encuentran los archivos de esquema de la base de datos
schemas: # Archivos de esquema de la base de datos
    - clinica
```
## Consideraciones previas
El programa fue desarrollado para Python 3.10 o superior. Para su correcto funcionamiento, se debe instalar el paquete `psycopg2`.

Además, se debe tener una base de datos PostgreSQL en ejecución, no es necesario que tenga datos, ya que el programa se encargará de crear las tablas necesarias. **Si se encuentra una tabla con el mismo nombre, el programa la eliminará y creará una nueva**, con el objeto de garantizar la integridad de los datos.

## Instrucciones para ejecución
Para ejecutar el programa, se debe correr el archivo `main.py` con el siguiente comando:
```bash

python3 main.py

```