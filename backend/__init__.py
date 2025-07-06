from flask import Flask
from backend.usuarios import usuarios_bp
from backend.clientes import clientes_bp
from backend.cortes import cortes_bp
from backend.vouchers import vouchers_bp
from backend.agendamentos import agendamentos_bp

def criar_app():
    app = Flask(__name__)
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
    app.register_blueprint(cortes_bp, url_prefix='/api/cortes')
    app.register_blueprint(vouchers_bp, url_prefix='/api/vouchers')
    app.register_blueprint(agendamentos_bp, url_prefix='/api/agendamentos')
    return app
