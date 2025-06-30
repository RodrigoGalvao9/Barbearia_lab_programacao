from flask import Blueprint, jsonify, request, session
import os
from .utils import (
    ler_arquivo_json, salvar_arquivo_json, validar_dados_obrigatorios,
    retornar_erro, retornar_sucesso, validar_email, validar_senha,
    gerar_proximo_id, log_acao
)

usuarios_bp = Blueprint('usuarios', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'usuarios.json')

def ler_usuarios():
    return ler_arquivo_json(CAMINHO_ARQUIVO)

def salvar_usuarios(usuarios):
    return salvar_arquivo_json(CAMINHO_ARQUIVO, usuarios)

@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = ler_usuarios()
    return jsonify(usuarios)

@usuarios_bp.route('/registrar', methods=['POST'])
def registrar_usuario():
    dados, erro = validar_dados_obrigatorios(['usuario', 'senha', 'nome'])
    if erro:
        return erro
    
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    nome = dados.get('nome')
    email = dados.get('email')
    
    # Validação de email se fornecido
    if email and not validar_email(email):
        return retornar_erro('Formato de email inválido', 400)
    
    # Validação de senha
    senha_valida, msg_senha = validar_senha(senha)
    if not senha_valida:
        return retornar_erro(msg_senha, 400)
    
    usuarios = ler_usuarios()
    
    # Verifica se usuário já existe
    if any(u['usuario'] == usuario for u in usuarios):
        return retornar_erro('Usuário já existe', 409)
    
    novo_usuario = {
        'id': gerar_proximo_id(usuarios),
        'usuario': usuario,
        'senha': senha,
        'nome': nome,
        'tipo': 'cliente'
    }
    
    if email:
        novo_usuario['email'] = email
    
    usuarios.append(novo_usuario)
    
    if not salvar_usuarios(usuarios):
        return retornar_erro('Erro ao salvar usuário', 500)
    
    log_acao('Usuário registrado', usuario, {'nome': nome})
    return retornar_sucesso('Usuário registrado com sucesso!', novo_usuario, 201)

@usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    dados, erro = validar_dados_obrigatorios(['usuario', 'senha'])
    if erro:
        return erro
    
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    usuarios = ler_usuarios()
    
    user = next((u for u in usuarios if u['usuario'] == usuario and u['senha'] == senha), None)
    if user:
        session['usuario'] = usuario
        session['tipo'] = user.get('tipo', 'cliente')
        log_acao('Login realizado', usuario)
        return retornar_sucesso('Login realizado com sucesso!', {'tipo': user.get('tipo', 'cliente')}, 200)
    
    log_acao('Tentativa de login falhou', usuario)
    return retornar_erro('Usuário ou senha inválidos', 401)

@usuarios_bp.route('/logout', methods=['POST'])
def logout_usuario():
    usuario_atual = session.get('usuario')
    session.clear()
    log_acao('Logout realizado', usuario_atual)
    return retornar_sucesso('Logout realizado com sucesso!', None, 200)

@usuarios_bp.route('/editar', methods=['PUT'])
def editar_perfil():
    dados, erro = validar_dados_obrigatorios(['usuario'])
    if erro:
        return erro
    
    usuario = dados.get('usuario')
    nome = dados.get('nome')
    senha = dados.get('senha')
    email = dados.get('email')
    
    # Validação de email se fornecido
    if email and not validar_email(email):
        return retornar_erro('Formato de email inválido', 400)
    
    # Validação de senha se fornecida
    if senha:
        senha_valida, msg_senha = validar_senha(senha)
        if not senha_valida:
            return retornar_erro(msg_senha, 400)
    
    usuarios = ler_usuarios()
    
    for u in usuarios:
        if u['usuario'] == usuario:
            if nome:
                u['nome'] = nome
            if senha:
                u['senha'] = senha
            if email:
                u['email'] = email
            
            if not salvar_usuarios(usuarios):
                return retornar_erro('Erro ao salvar alterações', 500)
            
            log_acao('Perfil editado', usuario, {'campos_alterados': [k for k, v in {'nome': nome, 'senha': senha, 'email': email}.items() if v]})
            return retornar_sucesso('Perfil atualizado com sucesso!', None, 200)
    
    return retornar_erro('Usuário não encontrado', 404)