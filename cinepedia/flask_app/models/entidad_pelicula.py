from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db_name = "cinepedia_db"

class Pelicula:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.usuario_id = data['usuario_id']
        self.creador_nombre = data.get('creador_nombre', '')
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Inserta una nueva película
    @classmethod
    def guardar(cls, formulario):
        query = """
            INSERT INTO peliculas (nombre, director, fecha_estreno, sinopsis, usuario_id) 
            VALUES (%(nombre)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s);
        """
        return connectToMySQL(db_name).query_db(query, formulario)

    # Obtiene todas las películas haciendo un JOIN con usuarios para saber quién la subió
    @classmethod
    def obtener_todas(cls):
        query = """
            SELECT peliculas.*, usuarios.nombre AS creador_nombre 
            FROM peliculas 
            JOIN usuarios ON peliculas.usuario_id = usuarios.id;
        """
        resultados = connectToMySQL(db_name).query_db(query)
        peliculas = []
        if resultados:
            for fila in resultados:
                peliculas.append(cls(fila))
        return peliculas

    # Busca una película específica por su ID
    @classmethod
    def obtener_por_id(cls, pelicula_id):
        query = """
            SELECT peliculas.*, usuarios.nombre AS creador_nombre 
            FROM peliculas 
            JOIN usuarios ON peliculas.usuario_id = usuarios.id 
            WHERE peliculas.id = %(id)s;
        """
        resultado = connectToMySQL(db_name).query_db(query, {'id': pelicula_id})
        if not resultado:
            return False
        return cls(resultado[0])

    # Busca una película por su nombre exacto
    @classmethod
    def obtener_por_nombre(cls, nombre):
        query = "SELECT * FROM peliculas WHERE nombre = %(nombre)s;"
        resultado = connectToMySQL(db_name).query_db(query, {'nombre': nombre})
        if not resultado:
            return False
        return cls(resultado[0])

    # Actualiza los datos de una película existente
    @classmethod
    def actualizar(cls, formulario):
        query = """
            UPDATE peliculas 
            SET nombre = %(nombre)s, director = %(director)s, 
                fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s 
            WHERE id = %(id)s;
        """
        return connectToMySQL(db_name).query_db(query, formulario)

    # Elimina una película de la base de datos por su ID
    @classmethod
    def eliminar(cls, pelicula_id):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query, {'id': pelicula_id})

    @staticmethod
    def validar_pelicula(formulario, pelicula_id=None):
        es_valido = True
        return es_valido