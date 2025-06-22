from flask import Blueprint, jsonify, request, session
import os
import json

clientes_bp = Blueprint('clientes', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'clientes.json')

def ler_clientes():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def salvar_clientes(clientes):
    with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as arquivo:
        json.dump(clientes, arquivo, ensure_ascii=False, indent=4)

@clientes_bp.route('/', methods=['GET'])
def listar_clientes():
    clientes = ler_clientes()
    return jsonify(clientes)

@clientes_bp.route('/', methods=['POST'])
def adicionar_cliente():
    if session.get('tipo') != 'adm':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem adicionar clientes.'}), 403
    clientes = ler_clientes()
    novo_cliente = request.json
    novo_cliente['id'] = len(clientes) + 1 
    clientes.append(novo_cliente)
    salvar_clientes(clientes)
    return jsonify(novo_cliente), 201

@clientes_bp.route('/<int:id_cliente>', methods=['PUT'])
def editar_cliente(id_cliente):
    if session.get('tipo') != 'adm':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem editar clientes.'}), 403
    clientes = ler_clientes()
    dados = request.json
    for cliente in clientes:
        if cliente['id'] == id_cliente:
            cliente.update(dados)
            salvar_clientes(clientes)
            return jsonify(cliente)
    return jsonify({'erro': 'Cliente não encontrado'}), 404

@clientes_bp.route('/<int:id_cliente>', methods=['DELETE'])
def remover_cliente(id_cliente):
    if session.get('tipo') != 'adm':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem remover clientes.'}), 403
    clientes = ler_clientes()
    clientes_novos = [c for c in clientes if c['id'] != id_cliente]
    if len(clientes_novos) == len(clientes):
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    salvar_clientes(clientes_novos)
    return jsonify({'mensagem': 'Cliente removido com sucesso'})
