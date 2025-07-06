"""
Utilitários para validação e formatação
"""
import re
from datetime import datetime


class Validador:
    @staticmethod
    def validar_telefone(telefone):
        """Valida formato de telefone brasileiro"""
        # Remove caracteres não numéricos
        telefone_limpo = re.sub(r'[^\d]', '', telefone)
        
        # Verifica se tem 10 ou 11 dígitos
        if len(telefone_limpo) not in [10, 11]:
            return False
        
        # Verifica se não são todos números iguais
        if len(set(telefone_limpo)) == 1:
            return False
        
        return True
    
    @staticmethod
    def validar_email(email):
        """Valida formato de email"""
        if not email:  # Email é opcional
            return True
        
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))
    
    @staticmethod
    def validar_nome(nome):
        """Valida se o nome tem pelo menos 2 caracteres"""
        return len(nome.strip()) >= 2
    
    @staticmethod
    def validar_data(data_str):
        """Valida formato de data DD/MM/AAAA"""
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_hora(hora_str):
        """Valida formato de hora HH:MM"""
        try:
            datetime.strptime(hora_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_preco(preco_str):
        """Valida se o preço é um número válido"""
        try:
            preco = float(preco_str.replace(',', '.'))
            return preco >= 0
        except ValueError:
            return False


class Formatador:
    @staticmethod
    def formatar_telefone(telefone):
        """Formata telefone para exibição"""
        telefone_limpo = re.sub(r'[^\d]', '', telefone)
        
        if len(telefone_limpo) == 11:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
        elif len(telefone_limpo) == 10:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
        
        return telefone
    
    @staticmethod
    def formatar_preco(preco):
        """Formata preço para exibição"""
        if isinstance(preco, str):
            preco = float(preco.replace(',', '.'))
        return f"R$ {preco:.2f}".replace('.', ',')
    
    @staticmethod
    def limpar_telefone(telefone):
        """Remove formatação do telefone"""
        return re.sub(r'[^\d]', '', telefone)


# Dados de exemplo para o sistema
DADOS_EXEMPLO = {
    "clientes": [
        {
            "nome": "João Silva",
            "telefone": "(11) 99999-1234",
            "email": "joao.silva@email.com",
            "endereco": "Rua das Flores, 123",
            "data_nascimento": "15/05/1985"
        },
        {
            "nome": "Maria Santos",
            "telefone": "(11) 88888-5678",
            "email": "maria.santos@email.com",
            "endereco": "Av. Principal, 456",
            "data_nascimento": "22/08/1990"
        },
        {
            "nome": "Pedro Oliveira",
            "telefone": "(11) 77777-9012",
            "email": "pedro.oliveira@email.com",
            "endereco": "Rua do Centro, 789",
            "data_nascimento": "10/12/1988"
        },
        {
            "nome": "Ana Costa",
            "telefone": "(11) 66666-3456",
            "email": "ana.costa@email.com",
            "endereco": "Rua Nova, 321",
            "data_nascimento": "03/03/1992"
        },
        {
            "nome": "Carlos Pereira",
            "telefone": "(11) 55555-7890",
            "email": "carlos.pereira@email.com",
            "endereco": "Av. Liberdade, 654",
            "data_nascimento": "18/09/1987"
        }
    ],
    "cortes": [
        {
            "cliente": "João Silva",
            "corte": "Corte Social",
            "preco": 25.0,
            "barbeiro": "Roberto",
            "data_hora": "02/07/2025 14:30",
            "observacoes": "Cliente preferiu degradê nas laterais"
        },
        {
            "cliente": "Pedro Oliveira",
            "corte": "Corte + Barba",
            "preco": 35.0,
            "barbeiro": "Carlos",
            "data_hora": "03/07/2025 10:15",
            "observacoes": "Primeira vez no estabelecimento"
        },
        {
            "cliente": "Carlos Pereira",
            "corte": "Corte Militar",
            "preco": 20.0,
            "barbeiro": "Roberto",
            "data_hora": "04/07/2025 16:45",
            "observacoes": "Corte bem baixo nas laterais"
        },
        {
            "cliente": "Ana Costa",
            "corte": "Corte Feminino",
            "preco": 45.0,
            "barbeiro": "Marina",
            "data_hora": "05/07/2025 11:00",
            "observacoes": "Corte em camadas, sem franja"
        }
    ],
    "agendamentos": [
        {
            "cliente": "Maria Santos",
            "data": "08/07/2025",
            "hora": "14:00",
            "servico": "Corte + Escova",
            "barbeiro": "Marina",
            "status": "Agendado",
            "observacoes": "Cliente solicitou hidratação"
        },
        {
            "cliente": "João Silva",
            "data": "09/07/2025",
            "hora": "15:30",
            "servico": "Corte Social",
            "barbeiro": "Roberto",
            "status": "Agendado",
            "observacoes": "Manutenção do corte anterior"
        },
        {
            "cliente": "Pedro Oliveira",
            "data": "10/07/2025",
            "hora": "09:45",
            "servico": "Barba",
            "barbeiro": "Carlos",
            "status": "Agendado",
            "observacoes": "Apenas aparar a barba"
        },
        {
            "cliente": "Carlos Pereira",
            "data": "11/07/2025",
            "hora": "16:15",
            "servico": "Corte Militar",
            "barbeiro": "Roberto",
            "status": "Confirmado",
            "observacoes": "Cliente é militar ativo"
        },
        {
            "cliente": "Ana Costa",
            "data": "12/07/2025",
            "hora": "13:00",
            "servico": "Corte + Tratamento",
            "barbeiro": "Marina",
            "status": "Agendado",
            "observacoes": "Tratamento para cabelo danificado"
        }
    ]
}

# Lista de tipos de corte disponíveis
TIPOS_CORTE = [
    "Corte Social",
    "Corte Militar",
    "Corte Degradê",
    "Corte Samurai",
    "Corte Navalhado",
    "Corte + Barba",
    "Corte Feminino",
    "Corte Infantil",
    "Apenas Barba",
    "Corte + Escova",
    "Corte + Tratamento"
]

# Lista de barbeiros
BARBEIROS = [
    "Roberto",
    "Carlos", 
    "Marina",
    "Anderson",
    "Fabiana"
]

# Status de agendamento
STATUS_AGENDAMENTO = [
    "Agendado",
    "Confirmado", 
    "Realizado",
    "Cancelado",
    "Não Compareceu"
]
