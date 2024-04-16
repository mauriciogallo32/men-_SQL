"""
Tarea n°1 programación

Mauricio Gallo Alfano

Elaborar una aplicación de línea de comandos en Python que sirva cuyo propósito
sea mantener un libro de recetas. Las recetas, los ingredientes y los pasos deben
ser almacenadas dentro de una base de datos SQLite. Las opciones dentro del programa
deben incluir como mínimo: a) Agregar nueva receta, c) Actualizar receta existente, d)
Eliminar receta existente, e) Ver listado de recetas, f) Buscar ingredientes y pasos de receta, g) Salir

"""
import sqlite3

# Función para conectar a la base de datosgit push -u origin master SQLite
def conectar_base_datos():
    conexion = sqlite3.connect("recetas.db")
    cursor = conexion.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            pasos TEXT NOT NULL
        )
    ''')

    return conexion, cursor

# Función para agregar una nueva receta
def agregar_receta(conexion, cursor):
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos de la receta: ")

    cursor.execute('''
        INSERT INTO recetas (nombre, ingredientes, pasos)
        VALUES (?, ?, ?)
    ''', (nombre, ingredientes, pasos))

    conexion.commit()
    print("Receta agregada con éxito.")

# Función para actualizar una receta existente
def actualizar_receta(conexion, cursor):
    id_receta = input("Ingrese el ID de la receta que desea actualizar: ")

    # Verificar si la receta existe
    cursor.execute('SELECT * FROM recetas WHERE id = ?', (id_receta,))
    receta = cursor.fetchone()

    if receta:
        print(f"Receta actual: {receta}")
        nuevo_nombre = input("Nuevo nombre de la receta (deje en blanco para no cambiar): ")
        nuevo_ingredientes = input("Nuevos ingredientes (deje en blanco para no cambiar): ")
        nuevos_pasos = input("Nuevos pasos de la receta (deje en blanco para no cambiar): ")

        # Actualizar la receta con la información proporcionada
        cursor.execute('''
            UPDATE recetas
            SET nombre = COALESCE(?, nombre),
                ingredientes = COALESCE(?, ingredientes),
                pasos = COALESCE(?, pasos)
            WHERE id = ?
        ''', (nuevo_nombre, nuevo_ingredientes, nuevos_pasos, id_receta))

        conexion.commit()
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para eliminar una receta existente
def eliminar_receta(conexion, cursor):
    id_receta = input("Ingrese el ID de la receta que desea eliminar: ")

    # Verificar si la receta existe
    cursor.execute('SELECT * FROM recetas WHERE id = ?', (id_receta,))
    receta = cursor.fetchone()

    if receta:
        # Eliminar la receta
        cursor.execute('DELETE FROM recetas WHERE id = ?', (id_receta,))
        conexion.commit()
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para ver un listado de recetas
def ver_listado_recetas(cursor):
    cursor.execute('SELECT * FROM recetas')
    recetas = cursor.fetchall()

    if recetas:
        for receta in recetas:
            print(f"ID: {receta[0]}, Nombre: {receta[1]}, Ingredientes: {receta[2]}, Pasos: {receta[3]}")
    else:
        print("No hay recetas en el libro.")

# Función para buscar ingredientes y pasos
def buscar_ingredientes_pasos(cursor):
    termino_busqueda = input("Ingrese el término de búsqueda: ")

    cursor.execute('''
        SELECT * FROM recetas
        WHERE nombre LIKE ? OR ingredientes LIKE ? OR pasos LIKE ?
    ''', (f"%{termino_busqueda}%", f"%{termino_busqueda}%", f"%{termino_busqueda}%"))

    recetas_encontradas = cursor.fetchall()

    if recetas_encontradas:
        for receta in recetas_encontradas:
            print(f"ID: {receta[0]}, Nombre: {receta[1]}, Ingredientes: {receta[2]}, Pasos: {receta[3]}")
    else:
        print("No se encontraron recetas que coincidan con la búsqueda.")

# Función principal
def main():
    conexion, cursor = conectar_base_datos()

    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("c) Actualizar receta existente")
        print("d) Eliminar receta existente")
        print("e) Ver listado de recetas")
        print("f) Buscar ingredientes y pasos de receta")
        print("g) Salir")

        opcion = input("Ingrese la opción deseada: ").lower()

        if opcion == 'a':
            agregar_receta(conexion, cursor)
        elif opcion == 'c':
            actualizar_receta(conexion, cursor)
        elif opcion == 'd':
            eliminar_receta(conexion, cursor)
        elif opcion == 'e':
            ver_listado_recetas(cursor)
        elif opcion == 'f':
            buscar_ingredientes_pasos(cursor)
        elif opcion == 'g':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")

    conexion.close()

if __name__ == "__main__":
    main()
