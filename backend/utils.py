from flask import jsonify, session, request
import os
import json
from functools import wraps
from datetime import datetime

# ==================== DECORADORES DE AUTENTICAÇÃO ====================

def requer_login(f):
    """Decorator que requer que o usuário esteja logado"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('usuario'):
            return retornar_erro('Usuário não autenticado. Faça login para continuar.', 401)
        return f(*args, **kwargs)
    return wrapper

def requer_admin(f):
    """Decorator que requer permissão de administrador"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('usuario'):
            return retornar_erro('Usuário não autenticado. Faça login para continuar.', 401)
        if session.get('tipo') != 'admin':
            return retornar_erro('Permissão negada. Apenas administradores podem realizar esta ação.', 403)
        return f(*args, **kwargs)
    return wrapper

def requer_permissao(tipos_permitidos):
    """Decorator que requer permissões específicas"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session.get('usuario'):
                return retornar_erro('Usuário não autenticado. Faça login para continuar.', 401)
            if session.get('tipo') not in tipos_permitidos:
                return retornar_erro('Permissão negada. Você não tem autorização para realizar esta ação.', 403)
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ==================== FUNÇÕES DE VERIFICAÇÃO ====================

def checar_usuario_logado():
    """Verifica se o usuário está logado e retorna o nome do usuário"""
    usuario = session.get('usuario')
    if not usuario:
        return None, retornar_erro('Usuário não autenticado. Faça login para continuar.', 401)
    return usuario, None

def checar_permissao_admin():
    """Verifica se o usuário tem permissão de administrador"""
    usuario, erro = checar_usuario_logado()
    if erro:
        return erro
    if session.get('tipo') != 'admin':
        return retornar_erro('Permissão negada. Apenas administradores podem realizar esta ação.', 403)
    return None

def obter_usuario_atual():
    """Retorna informações do usuário atual"""
    return {
        'usuario': session.get('usuario'),
        'tipo': session.get('tipo'),
        'logado': bool(session.get('usuario'))
    }

# ==================== FUNÇÕES DE RESPOSTA HTTP ====================

def retornar_erro(mensagem, codigo=400):
    """Retorna uma resposta de erro padronizada"""
    return jsonify({
        'erro': mensagem,
        'codigo': codigo,
        'timestamp': datetime.now().isoformat()
    }), codigo

def retornar_sucesso(mensagem, dados=None, codigo=200):
    """Retorna uma resposta de sucesso padronizada"""
    resposta = {
        'mensagem': mensagem,
        'sucesso': True,
        'timestamp': datetime.now().isoformat()
    }
    if dados:
        resposta['dados'] = dados
    return jsonify(resposta), codigo

def retornar_dados(dados, codigo=200):
    """Retorna dados sem mensagem"""
    return jsonify(dados), codigo

# ==================== FUNÇÕES DE ARQUIVO JSON ====================

def ler_arquivo_json(caminho):
    """Lê dados de um arquivo JSON"""
    try:
        if not os.path.exists(caminho):
            return []
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"Erro ao ler arquivo {caminho}: {e}")
        return []

def salvar_arquivo_json(caminho, dados):
    """Salva dados em um arquivo JSON"""
    try:
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo {caminho}: {e}")
        return False

# ==================== FUNÇÕES DE VALIDAÇÃO ====================

def validar_dados_obrigatorios(campos_obrigatorios):
    """Valida se os campos obrigatórios estão presentes no request"""
    if not request.json:
        return None, retornar_erro('Dados JSON não fornecidos', 400)
    
    dados = request.json
    campos_ausentes = [campo for campo in campos_obrigatorios if not dados.get(campo)]
    
    if campos_ausentes:
        return None, retornar_erro(f'Campos obrigatórios ausentes: {", ".join(campos_ausentes)}', 400)
    
    return dados, None

def validar_email(email):
    """Valida formato de email básico"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_senha(senha, min_length=6):
    """Valida força da senha"""
    if len(senha) < min_length:
        return False, f'Senha deve ter pelo menos {min_length} caracteres'
    return True, 'Senha válida'

# ==================== FUNÇÕES DE CRUD GENÉRICO ====================

def buscar_item_por_id(lista, item_id):
    """Busca um item por ID em uma lista"""
    return next((item for item in lista if item.get('id') == item_id), None)

def gerar_proximo_id(lista):
    """Gera o próximo ID para uma lista"""
    if not lista:
        return 1
    return max(item.get('id', 0) for item in lista) + 1

def remover_item_por_id(lista, item_id):
    """Remove um item da lista por ID"""
    item_original = len(lista)
    lista[:] = [item for item in lista if item.get('id') != item_id]
    return len(lista) < item_original

# ==================== FUNÇÕES DE LOG ====================

def log_acao(acao, usuario=None, detalhes=None):
    """Registra uma ação no sistema"""
    if not usuario:
        usuario = session.get('usuario', 'Anônimo')
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'usuario': usuario,
        'acao': acao,
        'detalhes': detalhes
    }
    
    print(f"[LOG] {log_entry}")  # Por enquanto só print, pode ser expandido para arquivo
    return log_entry
