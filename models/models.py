"""
Modelos de dados para o sistema da barbearia
"""

class Cliente:
    def __init__(self, nome, telefone, email="", endereco="", data_nascimento=""):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.data_nascimento = data_nascimento
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "endereco": self.endereco,
            "data_nascimento": self.data_nascimento
        }
    
    @staticmethod
    def from_dict(data):
        return Cliente(
            data.get("nome", ""),
            data.get("telefone", ""),
            data.get("email", ""),
            data.get("endereco", ""),
            data.get("data_nascimento", "")
        )

class Corte:
    def __init__(self, cliente, tipo_corte, preco=0.0, barbeiro="", data_hora="", observacoes=""):
        self.cliente = cliente
        self.tipo_corte = tipo_corte
        self.preco = preco
        self.barbeiro = barbeiro
        self.data_hora = data_hora
        self.observacoes = observacoes
    
    def to_dict(self):
        return {
            "cliente": self.cliente,
            "corte": self.tipo_corte,
            "preco": self.preco,
            "barbeiro": self.barbeiro,
            "data_hora": self.data_hora,
            "observacoes": self.observacoes
        }
    
    @staticmethod
    def from_dict(data):
        return Corte(
            data.get("cliente", ""),
            data.get("corte", ""),
            data.get("preco", 0.0),
            data.get("barbeiro", ""),
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
