from flask import Blueprint, jsonify, request, session
import os
from .vouchers import criar_voucher_fidelidade
from .utils import (
    ler_arquivo_json, salvar_arquivo_json, validar_dados_obrigatorios,
    retornar_erro, retornar_sucesso, retornar_dados, requer_admin, requer_login,
    gerar_proximo_id, buscar_item_por_id, remover_item_por_id, log_acao
)

agendamentos_bp = Blueprint('agendamentos', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'agendamentos.json')

def ler_agendamentos():
    return ler_arquivo_json(CAMINHO_ARQUIVO)

def salvar_agendamentos(agendamentos):
    return salvar_arquivo_json(CAMINHO_ARQUIVO, agendamentos)

@agendamentos_bp.route('/', methods=['GET'])
def listar_agendamentos():
    agendamentos = ler_agendamentos()
    return retornar_dados(agendamentos)

@agendamentos_bp.route('/', methods=['POST'])
@requer_login
def criar_agendamento():
    dados, erro = validar_dados_obrigatorios(['nome_cliente', 'data', 'horario'])
    if erro:
        return erro
    
    usuario_logado = session.get('usuario')
    nome_cliente = dados.get('nome_cliente')
    data = dados.get('data')
    horario = dados.get('horario')
    voucher = dados.get('voucher')
    pagamento = dados.get('pagamento')
    tipo_corte = dados.get('tipo_corte', '')
    valor_corte = dados.get('valor_corte', 0)
    desconto_voucher = dados.get('desconto_voucher', 0)
    valor_final = dados.get('valor_final', 0)
    
    agendamentos = ler_agendamentos()
    
    # Previne agendamento duplicado para o mesmo usuário, data e horário
    agendamento_duplicado = any(
        ag['nome_cliente'] == nome_cliente and 
        ag['data'] == data and 
        ag['horario'] == horario and 
        ag.get('usuario') == usuario_logado
        for ag in agendamentos
    )
    
    if agendamento_duplicado:
        return retornar_erro('Já existe agendamento para este cliente neste horário', 409)
    
    novo_agendamento = {
        'id': gerar_proximo_id(agendamentos),
        'nome_cliente': nome_cliente,
        'data': data,
        'horario': horario,
        'usuario': usuario_logado,
        'voucher': voucher,
        'pagamento': pagamento,
        'tipo_corte': tipo_corte,
        'valor_corte': valor_corte,
        'desconto_voucher': desconto_voucher,
        'valor_final': valor_final
    }
    
    agendamentos.append(novo_agendamento)
    
    if not salvar_agendamentos(agendamentos):
        return retornar_erro('Erro ao salvar agendamento', 500)
    
    # Fidelidade: gera voucher a cada 5 agendamentos do usuário
    total_usuario = sum(1 for ag in agendamentos if ag.get('usuario') == usuario_logado)
    if total_usuario % 5 == 0:
        sucesso_voucher = criar_voucher_fidelidade(usuario_logado)
        if sucesso_voucher:
            log_acao('Voucher de fidelidade gerado', usuario_logado, {'total_agendamentos': total_usuario})
    
    log_acao('Agendamento criado', usuario_logado, {'cliente': nome_cliente, 'data': data, 'horario': horario})
    return retornar_sucesso('Agendamento criado com sucesso', novo_agendamento, 201)

@agendamentos_bp.route('/<int:id_agendamento>', methods=['PUT'])
@requer_admin
def editar_agendamento(id_agendamento):
    dados, erro = validar_dados_obrigatorios([])
    if erro:
        return erro
    
    agendamentos = ler_agendamentos()
    agendamento = buscar_item_por_id(agendamentos, id_agendamento)
    
    if not agendamento:
        return retornar_erro('Agendamento não encontrado', 404)
      # Atualiza apenas os campos fornecidos
    campos_permitidos = ['nome_cliente', 'data', 'horario', 'voucher', 'pagamento', 'tipo_corte', 'valor_corte', 'desconto_voucher', 'valor_final']
    for campo in campos_permitidos:
        if campo in dados:
            agendamento[campo] = dados[campo]
    
    if not salvar_agendamentos(agendamentos):
        return retornar_erro('Erro ao salvar alterações', 500)
    
    log_acao('Agendamento editado', session.get('usuario'), {'id': id_agendamento})
    return retornar_sucesso('Agendamento editado com sucesso', agendamento)

@agendamentos_bp.route('/<int:id_agendamento>', methods=['DELETE'])
@requer_admin
def remover_agendamento(id_agendamento):
    agendamentos = ler_agendamentos()
    
    if not remover_item_por_id(agendamentos, id_agendamento):
        return retornar_erro('Agendamento não encontrado', 404)
    
    if not salvar_agendamentos(agendamentos):
        return retornar_erro('Erro ao remover agendamento', 500)
    
    log_acao('Agendamento removido', session.get('usuario'), {'id': id_agendamento})
    return retornar_sucesso('Agendamento removido com sucesso')