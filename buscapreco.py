from app import app
import os
from app.database import inicializar_db

#app.config['SECRET_KEY'] = 'Vilma@2024'

# Inicializar o banco de dados se necessário
inicializar_db()

if __name__=='main':
    port = int(os.getenv('PORT'), 5000)
    app.run(host='0.0.0.0', port = port)