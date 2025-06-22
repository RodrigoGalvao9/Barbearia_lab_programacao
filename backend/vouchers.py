from flask import Blueprint, jsonify, request, session
import os
import json

vouchers_bp = Blueprint('vouchers', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'vouchers.json')

def ler_vouchers():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def salvar_vouchers(vouchers):
    with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as arquivo:
        json.dump(vouchers, arquivo, ensure_ascii=False, indent=4)

@vouchers_bp.route('/', methods=['GET'])
def listar_vouchers():
    vouchers = ler_vouchers()
    return jsonify(vouchers)

@vouchers_bp.route('/', methods=['POST'])
def adicionar_voucher():
    if session.get('tipo') != 'adm':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem adicionar vouchers.'}), 403
    vouchers = ler_vouchers()
    novo_voucher = request.json
    novo_voucher['id'] = len(vouchers) + 1
    vouchers.append(novo_voucher)
    salvar_vouchers(vouchers)
    return jsonify(novo_voucher), 201

@vouchers_bp.route('/<int:id_voucher>', methods=['PUT'])
def editar_voucher(id_voucher):
    if session.get('tipo') != 'adm':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem editar vouchers.'}), 403
    vouchers = ler_vouchers()
    dados = request.json
    for voucher in vouchers:
        if voucher['id'] == id_voucher:
            voucher.update(dados)
            salvar_vouchers(vouchers)
            return jsonify(voucher)
    return jsonify({'erro': 'Voucher não encontrado'}), 404

@vouchers_bp.route('/<int:id_voucher>', methods=['DELETE'])
def remover_voucher(id_voucher):
    if session.get('tipo') != 'adm':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem remover vouchers.'}), 403
    vouchers = ler_vouchers()
    vouchers_novos = [v for v in vouchers if v['id'] != id_voucher]
    if len(vouchers_novos) == len(vouchers):
        return jsonify({'erro': 'Voucher não encontrado'}), 404
    salvar_vouchers(vouchers_novos)
    return jsonify({'mensagem': 'Voucher removido com sucesso'})