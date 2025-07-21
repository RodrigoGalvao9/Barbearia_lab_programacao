"""
Modelos de Dados - Sistema de Barbearia
=======================================

Este módulo define as classes modelo que representam as entidades
principais do sistema de barbearia:

Classes:
- Cliente: Representa um cliente da barbearia
- Corte: Representa um serviço de corte realizado (SEM campo barbeiro)
- Agendamento: Representa um agendamento de serviço

Funcionalidades dos modelos:
- Conversão para/de dicionário (JSON)
- Validação básica de dados
- Estrutura consistente para persistência
- Métodos de serialização/deserialização

Observações importantes:
- Campo "barbeiro" foi REMOVIDO da classe Corte
- Todos os modelos suportam conversão JSON
- Dados opcionais têm valores padrão vazios
"""

class Cliente:
    """
    Modelo que representa um cliente da barbearia.
    
    Attributes:
        nome (str): Nome completo do cliente (obrigatório)
        telefone (str): Telefone para contato (obrigatório)
        email (str): E-mail do cliente (opcional)
        endereco (str): Endereço completo (opcional)
        data_nascimento (str): Data de nascimento DD/MM/AAAA (opcional)
    """
    
    def __init__(self, nome, telefone, email="", endereco="", data_nascimento=""):
        """
        Inicializa um cliente.
        
        Args:
            nome (str): Nome completo (obrigatório)
            telefone (str): Telefone para contato (obrigatório)
            email (str, optional): E-mail do cliente
            endereco (str, optional): Endereço completo
            data_nascimento (str, optional): Data de nascimento
        """
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.data_nascimento = data_nascimento
    
    def to_dict(self):
        """
        Converte o cliente para dicionário (para JSON).
        
        Returns:
            dict: Dicionário com todos os dados do cliente
        """
        return {
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "endereco": self.endereco,
            "data_nascimento": self.data_nascimento
        }
    
    @staticmethod
    def from_dict(data):
        """
        Cria um cliente a partir de um dicionário (do JSON).
        
        Args:
            data (dict): Dicionário com dados do cliente
            
        Returns:
            Cliente: Nova instância de Cliente
        """
        return Cliente(
            data.get("nome", ""),
            data.get("telefone", ""),
            data.get("email", ""),
            data.get("endereco", ""),
            data.get("data_nascimento", "")
        )

class Corte:
    """
    Modelo que representa um serviço de corte realizado.
    
    IMPORTANTE: Campo "barbeiro" foi REMOVIDO do modelo por não ser necessário.
    
    Attributes:
        tipo_corte (str): Tipo/nome do corte realizado
        preco (float): Valor cobrado pelo serviço
        data_hora (str): Data e hora da realização
        observacoes (str): Observações adicionais sobre o serviço
    """
    
    def __init__(self, tipo_corte, preco=0.0, data_hora="", observacoes=""):
        """
        Inicializa um corte.
        
        Args:
            tipo_corte (str): Nome/tipo do corte (obrigatório)
            preco (float, optional): Valor do serviço (padrão 0.0)
            data_hora (str, optional): Data e hora da realização
            observacoes (str, optional): Observações sobre o serviço
        """
        self.tipo_corte = tipo_corte
        self.preco = preco
        self.data_hora = data_hora
        self.observacoes = observacoes
    
    def to_dict(self):
        """
        Converte o corte para dicionário (para JSON).
        
        Returns:
            dict: Dicionário com todos os dados do corte
        """
        return {
            "corte": self.tipo_corte,
            "preco": self.preco,
            "data_hora": self.data_hora,
            "observacoes": self.observacoes
        }
    
    @staticmethod
    def from_dict(data):
        """
        Cria um corte a partir de um dicionário (do JSON).
        
        Args:
            data (dict): Dicionário com dados do corte
            
        Returns:
            Corte: Nova instância de Corte
        """
        return Corte(
            data.get("corte", ""),
            data.get("preco", 0.0),
            data.get("data_hora", ""),
            data.get("observacoes", "")
        )

class Agendamento:
    def __init__(self, cliente, data, hora, servico="", barbeiro="", status="Agendado", observacoes=""):
        self.cliente = cliente
        self.data = data
        self.hora = hora
        self.servico = servico
        self.barbeiro = barbeiro
        self.status = status
        self.observacoes = observacoes
    
    def to_dict(self):
        return {
            "cliente": self.cliente,
            "data": self.data,
            "hora": self.hora,
            "servico": self.servico,
            "barbeiro": self.barbeiro,
            "status": self.status,
            "observacoes": self.observacoes
        }
    
    @staticmethod
    def from_dict(data):
        return Agendamento(
            data.get("cliente", ""),
            data.get("data", ""),
            data.get("hora", ""),
            data.get("servico", ""),
            data.get("barbeiro", ""),
            data.get("status", "Agendado"),
            data.get("observacoes", "")
        )
