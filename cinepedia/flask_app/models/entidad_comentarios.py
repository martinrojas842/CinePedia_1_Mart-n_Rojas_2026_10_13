from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db_name = "cinepedia_db"

class Comentario:
    def __init__(data):
        self = data.get('self') if 'self' in data else None
    def __init__(self, data):
        self.id = data['id']
        self.contenido = data['contenido']
        self.usuario_id = data['usuario_id']
        self.pelicula_id = data['pelicula_id']
        self.autor_nombre = data.get('autor_nombre', '')
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Inserta un nuevo comentario
    @classmethod
    def guardar(cls, formulario):
        query = """
            INSERT INTO comentarios (contenido, usuario_id, pelicula_id) 
            VALUES (%(contenido)s, %(usuario_id)s, %(pelicula_id)s);
        """
        return connectToMySQL(db_name).query_db(query, formulario)

    # Obtiene todos los comentarios de una película
    @classmethod
    def obtener_por_pelicula(cls, pelicula_id):
        query = """
            SELECT comentarios.*, usuarios.nombre AS autor_nombre 
            FROM comentarios 
            JOIN usuarios ON comentarios.usuario_id = usuarios.id 
            WHERE pelicula_id = %(pelicula_id)s 
            ORDER BY comentarios.created_at DESC;
        """
        resultados = connectToMySQL(db_name).query_db(query, {'pelicula_id': pelicula_id})
        comentarios = []
        if resultados:
            for fila in resultados:
                comentarios.append(cls(fila))
        return comentarios

    # Busca un comentario específico por su ID
    @classmethod
    def obtener_por_id(cls, comentario_id):
        query = "SELECT * FROM comentarios WHERE id = %(id)s;"
        resultado = connectToMySQL(db_name).query_db(query, {'id': comentario_id})
        if not resultado:
            return False
        return cls(resultado[0])

    # Elimina un comentario
    @classmethod
    def eliminar(cls, comentario_id):
        query = "DELETE FROM comentarios WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query, {'id': comentario_id})

    # Valida que el comentario no esté vacío
    @staticmethod
    def validar_comentario(formulario):
        es_valido = True
        if len(formulario['contenido'].strip()) < 1:
            flash("El comentario no puede estar vacío.", "comentario")
            es_valido = False
        return es_valido