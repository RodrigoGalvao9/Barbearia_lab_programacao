from flask import Blueprint, jsonify, request, session
import os
from .utils import (
    ler_arquivo_json, salvar_arquivo_json, validar_dados_obrigatorios,
    retornar_erro, retornar_sucesso, retornar_dados, requer_admin,
    gerar_proximo_id, buscar_item_por_id, remover_item_por_id, log_acao
)

cortes_bp = Blueprint('cortes', __name__)
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), 'arquivos', 'cortes.json')

def ler_cortes():
    return ler_arquivo_json(CAMINHO_ARQUIVO)

def salvar_cortes(cortes):
    return salvar_arquivo_json(CAMINHO_ARQUIVO, cortes)

@cortes_bp.route('/', methods=['GET'])
def listar_cortes():
    cortes = ler_cortes()
    return retornar_dados(cortes)

@cortes_bp.route('/', methods=['POST'])
@requer_admin
def adicionar_corte():
    dados, erro = validar_dados_obrigatorios(['nome', 'preco'])
    if erro:
        return erro
    
    nome = dados.get('nome')
    preco = dados.get('preco')
    descricao = dados.get('descricao')
    duracao = dados.get('duracao')
    
    # Validação de preço
    try:
        preco = float(preco)
        if preco <= 0:
            return retornar_erro('Preço deve ser maior que zero', 400)
    except (ValueError, TypeError):
        return retornar_erro('Preço deve ser um número válido', 400)
    
    cortes = ler_cortes()
    
    # Verifica se corte já existe
    if any(c['nome'].lower() == nome.lower() for c in cortes):
        return retornar_erro('Corte com este nome já existe', 409)
    
    novo_corte = {
        'id': gerar_proximo_id(cortes),
        'nome': nome,
        'preco': preco,
        'descricao': descricao,
        'duracao': duracao
    }
    
    cortes.append(novo_corte)
    
    if not salvar_cortes(cortes):
        return retornar_erro('Erro ao salvar corte', 500)
    
    log_acao('Corte adicionado', session.get('usuario'), {'nome': nome, 'preco': preco})
    return retornar_sucesso('Corte adicionado com sucesso', novo_corte, 201)

@cortes_bp.route('/<int:id_corte>', methods=['PUT'])
@requer_admin
def editar_corte(id_corte):
    dados, erro = validar_dados_obrigatorios([])
    if erro:
        return erro
    
    # Validação de preço se fornecido
    preco = dados.get('preco')
    if preco is not None:
        try:
            preco = float(preco)
            if preco <= 0:
                return retornar_erro('Preço deve ser maior que zero', 400)
            dados['preco'] = preco
        except (ValueError, TypeError):
            return retornar_erro('Preço deve ser um número válido', 400)
    
    cortes = ler_cortes()
    corte = buscar_item_por_id(cortes, id_corte)
    
    if not corte:
        return retornar_erro('Corte não encontrado', 404)
    
    # Atualiza apenas os campos fornecidos
    campos_permitidos = ['nome', 'preco', 'descricao', 'duracao']
    for campo in campos_permitidos:
        if campo in dados:
            corte[campo] = dados[campo]
    
    if not salvar_cortes(cortes):
        return retornar_erro('Erro ao salvar alterações', 500)
    
    log_acao('Corte editado', session.get('usuario'), {'id': id_corte})
    return retornar_sucesso('Corte editado com sucesso', corte)

@cortes_bp.route('/<int:id_corte>', methods=['DELETE'])
@requer_admin
def remover_corte(id_corte):
    cortes = ler_cortes()
    
    if not remover_item_por_id(cortes, id_corte):
        return retornar_erro('Corte não encontrado', 404)
    
    if not salvar_cortes(cortes):
        return retornar_erro('Erro ao remover corte', 500)
    
    log_acao('Corte removido', session.get('usuario'), {'id': id_corte})
    return retornar_sucesso('Corte removido com sucesso')