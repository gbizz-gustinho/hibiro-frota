from flask_bcrypt import Bcrypt
from flask_mail import Mail

bcrypt = Bcrypt()
mail = Mail() # Agora o app.py vai encontrar o 'mail' aqui!