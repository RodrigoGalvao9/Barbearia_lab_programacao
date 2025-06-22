from flask import Blueprint, jsonify, request, session
import os
import json

usuarios_bp = Blueprint('usuarios', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'usuarios.json')

def ler_usuarios():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def salvar_usuarios(usuarios):
    with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as arquivo:
        json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)

@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = ler_usuarios()
    return jsonify(usuarios)

@usuarios_bp.route('/registrar', methods=['POST'])
def registrar_usuario():
    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    nome = dados.get('nome')
    if not usuario or not senha or not nome:
        return jsonify({'erro': 'Preencha todos os campos.'}), 400
    usuarios = ler_usuarios()
    if any(u['usuario'] == usuario for u in usuarios):
        return jsonify({'erro': 'Usuário já existe.'}), 409
    novo_usuario = {
        'id': len(usuarios) + 1,
        'usuario': usuario,
        'senha': senha,
        'nome': nome,
        'tipo': 'cliente'
    }
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    return jsonify({'mensagem': 'Usuário registrado com sucesso!'}), 201

@usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    usuarios = ler_usuarios()
    user = next((u for u in usuarios if u['usuario'] == usuario and u['senha'] == senha), None)
    if user:
        session['usuario'] = usuario
        session['tipo'] = user.get('tipo', 'cliente')
        return jsonify({'mensagem': 'Login realizado com sucesso!', 'tipo': user.get('tipo', 'cliente')}), 200
    return jsonify({'erro': 'Usuário ou senha inválidos.'}), 401

@usuarios_bp.route('/logout', methods=['POST'])
def logout_usuario():
    session.clear()
    return jsonify({'mensagem': 'Logout realizado com sucesso!'}), 200

@usuarios_bp.route('/editar', methods=['PUT'])
def editar_perfil():
    dados = request.json
    usuario = dados.get('usuario')
    nome = dados.get('nome')
    senha = dados.get('senha')
    usuarios = ler_usuarios()
    for u in usuarios:
        if u['usuario'] == usuario:
            if nome:
                u['nome'] = nome
            if senha:
                u['senha'] = senha
            salvar_usuarios(usuarios)
            return jsonify({'mensagem': 'Perfil atualizado com sucesso!'}), 200
    return jsonify({'erro': 'Usuário não encontrado.'}), 404