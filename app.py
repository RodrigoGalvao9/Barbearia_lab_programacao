from backend import criar_app
from flask import send_from_directory
import os

app = criar_app()
app.secret_key = 'chave-super-secreta-123'  # Troque por uma chave forte em produção

@app.route('/')
def pagina_inicial():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'interface'), 'index.html')

@app.route('/<path:arquivo>')
def arquivos_estaticos(arquivo):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'interface'), arquivo)

if __name__ == '__main__':
    app.run(debug=True)