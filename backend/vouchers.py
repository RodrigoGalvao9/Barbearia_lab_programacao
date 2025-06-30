from flask import Blueprint, jsonify, request, session
import os
import random
import string
from datetime import datetime, timedelta
from .utils import (
    ler_arquivo_json, salvar_arquivo_json, validar_dados_obrigatorios,
    retornar_erro, retornar_sucesso, retornar_dados, requer_admin, requer_login,
    checar_usuario_logado, gerar_proximo_id, buscar_item_por_id,
    remover_item_por_id, log_acao
)

vouchers_bp = Blueprint('vouchers', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'vouchers.json')

def ler_vouchers():
    return ler_arquivo_json(CAMINHO_ARQUIVO)

def salvar_vouchers(vouchers):
    return salvar_arquivo_json(CAMINHO_ARQUIVO, vouchers)

@vouchers_bp.route('/', methods=['GET'])
def listar_vouchers():
    vouchers = ler_vouchers()
    # Para usuários não logados, mostra apenas vouchers públicos (sem campo usuario) que não foram usados
    vouchers_publicos = [
        v for v in vouchers 
        if (not v.get('usuario') or v.get('usuario') == '') and not v.get('usado', False)
    ]
    return retornar_dados(vouchers_publicos)

@vouchers_bp.route('/', methods=['POST'])
@requer_admin
def adicionar_voucher():
    dados, erro = validar_dados_obrigatorios(['codigo', 'descricao'])
    if erro:
        return erro
    
    vouchers = ler_vouchers()
      # Verifica se o código já existe
    if any(v['codigo'] == dados.get('codigo') for v in vouchers):
        return retornar_erro('Código de voucher já existe', 409)
    
    novo_voucher = {
        'id': gerar_proximo_id(vouchers),
        'codigo': dados.get('codigo'),
        'descricao': dados.get('descricao'),
        'validade': dados.get('validade'),
        'usuario': dados.get('usuario'),
        'porcentagem': dados.get('porcentagem', 10),  # Default 10% se não especificado
        'usado': False
    }
    
    vouchers.append(novo_voucher)
    
    if not salvar_vouchers(vouchers):
        return retornar_erro('Erro ao salvar voucher', 500)
    
    log_acao('Voucher adicionado', session.get('usuario'), {'codigo': novo_voucher['codigo']})
    return retornar_sucesso('Voucher adicionado com sucesso', novo_voucher, 201)

@vouchers_bp.route('/<int:id_voucher>', methods=['PUT'])
@requer_admin
def editar_voucher(id_voucher):
    dados, erro = validar_dados_obrigatorios([])
    if erro:
        return erro
    
    vouchers = ler_vouchers()
    voucher = buscar_item_por_id(vouchers, id_voucher)
    
    if not voucher:
        return retornar_erro('Voucher não encontrado', 404)
      # Atualiza apenas os campos fornecidos
    campos_permitidos = ['codigo', 'descricao', 'validade', 'usuario', 'porcentagem']
    for campo in campos_permitidos:
        if campo in dados:
            voucher[campo] = dados[campo]
    
    if not salvar_vouchers(vouchers):
        return retornar_erro('Erro ao salvar alterações', 500)
    
    log_acao('Voucher editado', session.get('usuario'), {'id': id_voucher})
    return retornar_sucesso('Voucher editado com sucesso', voucher)

@vouchers_bp.route('/<int:id_voucher>', methods=['DELETE'])
@requer_admin
def remover_voucher(id_voucher):
    vouchers = ler_vouchers()
    
    if not remover_item_por_id(vouchers, id_voucher):
        return retornar_erro('Voucher não encontrado', 404)
    
    if not salvar_vouchers(vouchers):
        return retornar_erro('Erro ao remover voucher', 500)
    
    log_acao('Voucher removido', session.get('usuario'), {'id': id_voucher})
    return retornar_sucesso('Voucher removido com sucesso')

# Função auxiliar para criar voucher de fidelidade

def criar_voucher_fidelidade(usuario):
    vouchers = ler_vouchers()
    codigo = 'FIDELIDADE-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    validade = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
    
    voucher = {
        'id': gerar_proximo_id(vouchers),
        'codigo': codigo,
        'descricao': f'Voucher fidelidade para {usuario}',
        'validade': validade,
        'usuario': usuario,
        'porcentagem': 15,  # Vouchers fidelidade têm 15% de desconto
        'usado': False
    }
    vouchers.append(voucher)
    
    if not salvar_vouchers(vouchers):
        print(f"Erro ao salvar voucher de fidelidade para {usuario}")
        return False
    
    log_acao('Voucher de fidelidade criado', usuario, {'codigo': codigo})
    return True

@vouchers_bp.route('/meus-vouchers', methods=['GET'])
@requer_login
def listar_vouchers_usuario():
    usuario_logado = session.get('usuario')
    vouchers = ler_vouchers()
    
    # Inclui vouchers próprios + vouchers públicos (sem campo usuario ou usuario vazio)
    vouchers_usuario = [
        v for v in vouchers 
        if (v.get('usuario') == usuario_logado or v.get('usuario') is None or v.get('usuario') == '') 
        and not v.get('usado')
    ]
    
    if not vouchers_usuario:
        return retornar_sucesso('Nenhum voucher disponível para este usuário', [])
    
    return retornar_dados(vouchers_usuario)

@vouchers_bp.route('/usar/<int:id_voucher>', methods=['POST'])
@requer_login
def usar_voucher(id_voucher):
    usuario_logado = session.get('usuario')
    vouchers = ler_vouchers()
    
    voucher = buscar_item_por_id(vouchers, id_voucher)
    
    if not voucher:
        return retornar_erro('Voucher não encontrado', 404)
    
    # Verifica se o usuário pode usar este voucher (voucher público ou próprio)
    if voucher.get('usuario') and voucher['usuario'] != usuario_logado:
        return retornar_erro('Este voucher não pertence a você', 403)
    
    if voucher.get('usado'):
        return retornar_erro('Este voucher já foi usado', 400)
    
    # Verifica se o voucher ainda é válido
    if voucher.get('validade'):
        try:
            data_validade = datetime.strptime(voucher['validade'], '%Y-%m-%d')
            if data_validade.date() < datetime.now().date():
                return retornar_erro('Este voucher expirou', 400)
        except ValueError:
            pass  # Se não conseguir parsear a data, continua
    
    voucher['usado'] = True
    voucher['data_uso'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not salvar_vouchers(vouchers):
        return retornar_erro('Erro ao usar voucher', 500)
    
    log_acao('Voucher usado', usuario_logado, {'codigo': voucher['codigo']})
    return retornar_sucesso('Voucher usado com sucesso')

@vouchers_bp.before_request
def verificar_sessao():
    # Permite acesso público à listagem de vouchers (GET /)
    if request.method == 'GET' and request.endpoint == 'vouchers.listar_vouchers':
        return None
    
    if not session.get('usuario'):
        return jsonify({'erro': 'Usuário não autenticado. Faça login para continuar.'}), 401