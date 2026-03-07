# models.py (Exemplo simplificado)
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, nome, email, password_hash):
        self.id = id
        self.nome = nome
        self.email = email
        self.password_hash = password_hash

    # Método de validação de senha
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Simulando um banco de dados simples com uma lista de usuários
# Em um projeto real, você usaria um banco de dados como SQLite, PostgreSQL, etc.
_users_db = []
_next_user_id = 1

class UserDao:
    @staticmethod
    def get_by_id(user_id):
        return next((user for user in _users_db if user.id == user_id), None)

    @staticmethod
    def get_by_email(email):
        return next((user for user in _users_db if user.email == email), None)

    @staticmethod
    def create(nome, email, password):
        global _next_user_id
        # Hash da senha antes de armazenar
        hashed_password = generate_password_hash(password)
        new_user = User(_next_user_id, nome, email, hashed_password)
        _users_db.append(new_user)
        _next_user_id += 1
        return new_user