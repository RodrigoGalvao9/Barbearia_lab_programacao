from flask import Blueprint, jsonify, request, session
import os
import json

cortes_bp = Blueprint('cortes', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'cortes.json')

def ler_cortes():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def salvar_cortes(cortes):
    with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as arquivo:
        json.dump(cortes, arquivo, ensure_ascii=False, indent=4)

@cortes_bp.route('/', methods=['GET'])
def listar_cortes():
    cortes = ler_cortes()
    return jsonify(cortes)

@cortes_bp.route('/', methods=['POST'])
def adicionar_corte():
    if session.get('tipo') != 'admin':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem adicionar cortes.'}), 403
    cortes = ler_cortes()
    novo_corte = request.json
    novo_corte['id'] = len(cortes) + 1
    cortes.append(novo_corte)
    salvar_cortes(cortes)
    return jsonify(novo_corte), 201

@cortes_bp.route('/<int:id_corte>', methods=['PUT'])
def editar_corte(id_corte):
    if session.get('tipo') != 'admin':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem editar cortes.'}), 403
    cortes = ler_cortes()
    dados = request.json
    for corte in cortes:
        if corte['id'] == id_corte:
            corte.update(dados)
            salvar_cortes(cortes)
            return jsonify(corte)
    return jsonify({'erro': 'Corte não encontrado'}), 404

@cortes_bp.route('/<int:id_corte>', methods=['DELETE'])
def remover_corte(id_corte):
    if session.get('tipo') != 'admin':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem remover cortes.'}), 403
    cortes = ler_cortes()
    cortes_novos = [c for c in cortes if c['id'] != id_corte]
    if len(cortes_novos) == len(cortes):
        return jsonify({'erro': 'Corte não encontrado'}), 404
    salvar_cortes(cortes_novos)
    return jsonify({'mensagem': 'Corte removido com sucesso'})