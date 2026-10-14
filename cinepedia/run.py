# Archivo principal para arrancar el servidor de Flask
from flask_app import app
from flask_app.controllers import rutas_usuarios, rutas_peliculas

if __name__ == "__main__":
    app.run(debug=True)