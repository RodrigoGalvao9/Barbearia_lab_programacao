from flask import Blueprint, jsonify, request, session
import os
import json
import random
import string

agendamentos_bp = Blueprint('agendamentos', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'agendamentos.json')

def ler_agendamentos():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def salvar_agendamentos(agendamentos):
    with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as arquivo:
        json.dump(agendamentos, arquivo, ensure_ascii=False, indent=4)

@agendamentos_bp.route('/', methods=['GET'])
def listar_agendamentos():
    agendamentos = ler_agendamentos()
    return jsonify(agendamentos)

@agendamentos_bp.route('/', methods=['POST'])
def criar_agendamento():
    # Verifica se o usuário está logado
    usuario_logado = session.get('usuario')
    if not usuario_logado:
        return jsonify({'erro': 'É necessário estar logado para agendar.'}), 401

    dados = request.json
    nome_cliente = dados.get('nome_cliente')
    data = dados.get('data')
    horario = dados.get('horario')
    voucher = dados.get('voucher')
    pagamento = dados.get('pagamento')
    if not nome_cliente or not data or not horario:
        return jsonify({'erro': 'Dados obrigatórios faltando.'}), 400

    agendamentos = ler_agendamentos()
    # Previne agendamento duplicado para o mesmo usuário, data e horário
    for ag in agendamentos:
        if (ag['nome_cliente'] == nome_cliente and ag['data'] == data and ag['horario'] == horario and ag.get('usuario') == usuario_logado):
            return jsonify({'erro': 'Já existe agendamento para este cliente neste horário.'}), 409

    novo_agendamento = {
        'id': len(agendamentos) + 1,
        'nome_cliente': nome_cliente,
        'data': data,
        'horario': horario,
        'usuario': usuario_logado,
        'voucher': voucher,
        'pagamento': pagamento
    }
    agendamentos.append(novo_agendamento)
    salvar_agendamentos(agendamentos)

    # Fidelidade: gera voucher a cada 5 agendamentos do usuário
    total_usuario = sum(1 for ag in agendamentos if ag.get('usuario') == usuario_logado)
    if total_usuario % 5 == 0:
        _criar_voucher_fidelidade(usuario_logado)

    return jsonify(novo_agendamento), 201

# Função auxiliar para criar voucher de fidelidade
def _criar_voucher_fidelidade(usuario):
    caminho_vouchers = os.path.join(os.path.dirname(__file__), 'arquivos', 'vouchers.json')
    if not os.path.exists(caminho_vouchers):
        vouchers = []
    else:
        with open(caminho_vouchers, 'r', encoding='utf-8') as arq:
            vouchers = json.load(arq)
    codigo = 'FIDELIDADE-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    voucher = {
        'id': len(vouchers) + 1,
        'codigo': codigo,
        'descricao': f'Voucher fidelidade para {usuario}',
        'validade': '2025-12-31',
        'usuario': usuario
    }
    vouchers.append(voucher)
    with open(caminho_vouchers, 'w', encoding='utf-8') as arq:
        json.dump(vouchers, arq, ensure_ascii=False, indent=4)

@agendamentos_bp.route('/<int:id_agendamento>', methods=['PUT'])
def editar_agendamento(id_agendamento):
    from flask import session
    if session.get('tipo') != 'admin':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem editar agendamentos.'}), 403
    agendamentos = ler_agendamentos()
    dados = request.json
    for ag in agendamentos:
        if ag['id'] == id_agendamento:
            ag.update(dados)
            salvar_agendamentos(agendamentos)
            return jsonify(ag)
    return jsonify({'erro': 'Agendamento não encontrado'}), 404

@agendamentos_bp.route('/<int:id_agendamento>', methods=['DELETE'])
def remover_agendamento(id_agendamento):
    from flask import session
    if session.get('tipo') != 'admin':
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem remover agendamentos.'}), 403
    agendamentos = ler_agendamentos()
    agendamentos_novos = [a for a in agendamentos if a['id'] != id_agendamento]
    if len(agendamentos_novos) == len(agendamentos):
        return jsonify({'erro': 'Agendamento não encontrado'}), 404
    salvar_agendamentos(agendamentos_novos)
    return jsonify({'mensagem': 'Agendamento removido com sucesso'})