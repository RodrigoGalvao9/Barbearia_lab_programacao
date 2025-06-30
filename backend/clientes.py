from flask import Blueprint, jsonify, request, session
import os
from .utils import (
    ler_arquivo_json, salvar_arquivo_json, validar_dados_obrigatorios,
    retornar_erro, retornar_sucesso, retornar_dados, requer_admin,
    gerar_proximo_id, buscar_item_por_id, remover_item_por_id, 
    validar_email, log_acao
)

clientes_bp = Blueprint('clientes', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'clientes.json')

def ler_clientes():
    return ler_arquivo_json(CAMINHO_ARQUIVO)

def salvar_clientes(clientes):
    return salvar_arquivo_json(CAMINHO_ARQUIVO, clientes)

@clientes_bp.route('/', methods=['GET'])
def listar_clientes():
    clientes = ler_clientes()
    return retornar_dados(clientes)

@clientes_bp.route('/', methods=['POST'])
@requer_admin
def adicionar_cliente():
    dados, erro = validar_dados_obrigatorios(['nome'])
    if erro:
        return erro
    
    nome = dados.get('nome')
    telefone = dados.get('telefone')
    email = dados.get('email')
    
    # Validação de email se fornecido
    if email and not validar_email(email):
        return retornar_erro('Formato de email inválido', 400)
    
    clientes = ler_clientes()
    
    # Verifica se cliente já existe (por nome e telefone)
    if telefone and any(c.get('telefone') == telefone for c in clientes):
        return retornar_erro('Cliente com este telefone já existe', 409)
    
    novo_cliente = {
        'id': gerar_proximo_id(clientes),
        'nome': nome,
        'telefone': telefone,
        'email': email
    }
    
    clientes.append(novo_cliente)
    
    if not salvar_clientes(clientes):
        return retornar_erro('Erro ao salvar cliente', 500)
    
    log_acao('Cliente adicionado', session.get('usuario'), {'nome': nome})
    return retornar_sucesso('Cliente adicionado com sucesso', novo_cliente, 201)

@clientes_bp.route('/<int:id_cliente>', methods=['PUT'])
@requer_admin
def editar_cliente(id_cliente):
    dados, erro = validar_dados_obrigatorios([])
    if erro:
        return erro
    
    # Validação de email se fornecido
    email = dados.get('email')
    if email and not validar_email(email):
        return retornar_erro('Formato de email inválido', 400)
    
    clientes = ler_clientes()
    cliente = buscar_item_por_id(clientes, id_cliente)
    
    if not cliente:
        return retornar_erro('Cliente não encontrado', 404)
    
    # Atualiza apenas os campos fornecidos
    campos_permitidos = ['nome', 'telefone', 'email']
    for campo in campos_permitidos:
        if campo in dados:
            cliente[campo] = dados[campo]
    
    if not salvar_clientes(clientes):
        return retornar_erro('Erro ao salvar alterações', 500)
    
    log_acao('Cliente editado', session.get('usuario'), {'id': id_cliente})
    return retornar_sucesso('Cliente editado com sucesso', cliente)

@clientes_bp.route('/<int:id_cliente>', methods=['DELETE'])
@requer_admin
def remover_cliente(id_cliente):
    clientes = ler_clientes()
    
    if not remover_item_por_id(clientes, id_cliente):
        return retornar_erro('Cliente não encontrado', 404)
    
    if not salvar_clientes(clientes):
        return retornar_erro('Erro ao remover cliente', 500)
    
    log_acao('Cliente removido', session.get('usuario'), {'id': id_cliente})
    return retornar_sucesso('Cliente removido com sucesso')
