from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db_name = "cinepedia_db"

class Usuario:
    # Constructor para inicializar los datos del usuario
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Inserta un nuevo usuario
    @classmethod
    def guardar(cls, formulario):
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        return connectToMySQL(db_name).query_db(query, formulario)

    # Busca un usuario en la base de datos usando su correo electrónico
    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(db_name).query_db(query, {'email': email})
        
        if not resultado or not isinstance(resultado, list) or len(resultado) < 1:
            return False
        return cls(resultado[0])

    # Busca un usuario por su ID
    @classmethod
    def obtener_por_id(cls, id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL(db_name).query_db(query, {'id': id})
        
        if not resultado or not isinstance(resultado, list) or len(resultado) < 1:
            return False
        return cls(resultado[0])

    # Valida los campos del formulario de registro de usuario
    @staticmethod
    def validar_registro(formulario):
        es_valido = True
        
        if len(formulario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        if len(formulario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        if not EMAIL_REGEX.match(formulario['email']):
            flash("Formato de correo electrónico inválido.", "registro")
            es_valido = False
        else:
            usuario_existente = Usuario.obtener_por_email(formulario['email'])
            if usuario_existente:
                flash("El correo electrónico ya está registrado.", "registro")
                es_valido = False
        if len(formulario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            es_valido = False
            
        if 'confirm_password' in formulario and formulario['password'] != formulario['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False
            
        return es_valido