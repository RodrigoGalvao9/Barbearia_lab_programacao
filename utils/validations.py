"""
=================================================
SISTEMA DE VALIDAÇÕES E CONSTANTES
=================================================

Este módulo centraliza todas as validações de dados
e constantes utilizadas no sistema de barbearia.

Inclui validações para:
- Telefone brasileiro
- Email
- Nome
- Data e hora
- Preço

E constantes para:
- Tipos de corte
- Lista de barbeiros
- Status de agendamentos

Autor: Sistema Barbearia v2.0
Data: Julho 2025

=================================================
"""

import re
from datetime import datetime


class Validador:
    """
    =================================================
    CLASSE DE VALIDAÇÃO DE DADOS
    =================================================
    
    Centraliza todas as validações utilizadas no sistema,
    garantindo consistência e reutilização de código.
    
    Todas as validações retornam True para dados válidos
    e False para dados inválidos.
    """
    
    @staticmethod
    def validar_telefone(telefone):
        """
        Valida formato de telefone brasileiro.
        
        Aceita telefones com 10 ou 11 dígitos:
        - 10 dígitos: telefone fixo (xx) xxxx-xxxx
        - 11 dígitos: celular (xx) 9xxxx-xxxx
        
        Args:
            telefone (str): Número de telefone para validar
            
        Returns:
            bool: True se telefone válido, False caso contrário
            
        Examples:
            >>> Validador.validar_telefone("(11) 99999-9999")
            True
            >>> Validador.validar_telefone("11999999999")
            True
            >>> Validador.validar_telefone("123")
            False
        """
        # Remove caracteres não numéricos
        telefone_limpo = re.sub(r'[^\d]', '', telefone)
        
        # Verifica se tem 10 ou 11 dígitos
        if len(telefone_limpo) not in [10, 11]:
            return False
        
        # Verifica se não são todos números iguais (ex: 11111111111)
        if len(set(telefone_limpo)) == 1:
            return False
        
        return True
    
    @staticmethod
    def validar_email(email):
        """
        Valida formato de email.
        
        Aceita emails vazios (campo opcional) ou emails
        com formato válido (usuario@dominio.com).
        
        Args:
            email (str): Endereço de email para validar
            
        Returns:
            bool: True se email válido ou vazio, False caso contrário
            
        Examples:
            >>> Validador.validar_email("usuario@gmail.com")
            True
            >>> Validador.validar_email("")
            True
            >>> Validador.validar_email("email_invalido")
            False
        """
        if not email:  # Email é opcional
            return True
        
        # Padrão de regex para validação de email
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))
    
    @staticmethod
    def validar_nome(nome):
        """
        Valida se o nome tem pelo menos 2 caracteres.
        
        Remove espaços extras e verifica comprimento mínimo
        para garantir que não sejam aceitos nomes muito curtos.
        
        Args:
            nome (str): Nome para validar
            
        Returns:
            bool: True se nome válido, False caso contrário
            
        Examples:
            >>> Validador.validar_nome("João Silva")
            True
            >>> Validador.validar_nome("A")
            False
            >>> Validador.validar_nome("  João  ")
            True
        """
        return len(nome.strip()) >= 2
    
    @staticmethod
    def validar_data(data_str):
        """
        Valida formato de data DD/MM/AAAA.
        
        Verifica se a string está no formato correto
        e se representa uma data válida.
        
        Args:
            data_str (str): String de data para validar
            
        Returns:
            bool: True se data válida, False caso contrário
            
        Examples:
            >>> Validador.validar_data("25/12/2023")
            True
            >>> Validador.validar_data("31/02/2023")
            False
            >>> Validador.validar_data("25-12-2023")
            False
        """
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_hora(hora_str):
        """
        Valida formato de hora HH:MM.
        
        Verifica se a string está no formato de hora válido
        (00:00 a 23:59).
        
        Args:
            hora_str (str): String de hora para validar
            
        Returns:
            bool: True se hora válida, False caso contrário
            
        Examples:
            >>> Validador.validar_hora("14:30")
            True
            >>> Validador.validar_hora("25:00")
            False
            >>> Validador.validar_hora("14h30")
            False
        """
        try:
            datetime.strptime(hora_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_preco(preco_str):
        """
        Valida se o preço é um número válido.
        
        Aceita números com vírgula ou ponto decimal
        e verifica se não são negativos.
        
        Args:
            preco_str (str): String do preço para validar
            
        Returns:
            bool: True se preço válido, False caso contrário
            
        Examples:
            >>> Validador.validar_preco("25,50")
            True
            >>> Validador.validar_preco("25.50")
            True
            >>> Validador.validar_preco("-10")
            False
            >>> Validador.validar_preco("abc")
            False
        """
        try:
            preco = float(preco_str.replace(',', '.'))
            return preco >= 0
        except ValueError:
            return False


class Formatador:
    """
    =================================================
    CLASSE DE FORMATAÇÃO DE DADOS
    =================================================
    
    Centraliza todas as formatações de dados utilizadas
    no sistema, garantindo apresentação consistente.
    
    Inclui formatações para:
    - Telefone brasileiro
    - Preço em reais
    - Limpeza de dados
    """
    
    @staticmethod
    def formatar_telefone(telefone):
        """
        Formata telefone para exibição.
        
        Converte números limpos em formato brasileiro:
        - 11 dígitos: (xx) 9xxxx-xxxx
        - 10 dígitos: (xx) xxxx-xxxx
        
        Args:
            telefone (str): Número de telefone limpo ou sujo
            
        Returns:
            str: Telefone formatado
            
        Examples:
            >>> Formatador.formatar_telefone("11999999999")
            "(11) 99999-9999"
            >>> Formatador.formatar_telefone("1133334444")
            "(11) 3333-4444"
        """
        telefone_limpo = re.sub(r'[^\d]', '', telefone)
        
        if len(telefone_limpo) == 11:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
        elif len(telefone_limpo) == 10:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
        
        return telefone
    
    @staticmethod
    def formatar_preco(preco):
        """
        Formata preço para exibição em reais.
        
        Converte números em formato monetário brasileiro
        com símbolo R$ e vírgula decimal.
        
        Args:
            preco (float or str): Valor do preço
            
        Returns:
            str: Preço formatado (R$ 00,00)
            
        Examples:
            >>> Formatador.formatar_preco(25.50)
            "R$ 25,50"
            >>> Formatador.formatar_preco("30.75")
            "R$ 30,75"
        """
        if isinstance(preco, str):
            preco = float(preco.replace(',', '.'))
        return f"R$ {preco:.2f}".replace('.', ',')
    
    @staticmethod
    def limpar_telefone(telefone):
        """
        Remove formatação do telefone.
        
        Extrai apenas os dígitos do telefone,
        removendo parênteses, hífens e espaços.
        
        Args:
            telefone (str): Telefone formatado
            
        Returns:
            str: Apenas dígitos do telefone
            
        Examples:
            >>> Formatador.limpar_telefone("(11) 99999-9999")
            "11999999999"
            >>> Formatador.limpar_telefone("11 99999 9999")
            "11999999999"
        """
        return re.sub(r'[^\d]', '', telefone)


# =================================================
# CONSTANTES DO SISTEMA
# =================================================

# Lista completa de tipos de corte oferecidos pela barbearia
# Organizada por categoria para facilitar manutenção
TIPOS_CORTE = [
    # === CORTES MASCULINOS POPULARES ===
    "Corte Degradê",        # Corte com transição suave
    "Corte Social",         # Corte clássico profissional
    "Corte Militar",        # Corte bem baixo, estilo militar
    "Corte Undercut",       # Lateral raspada, topo comprido
    "Corte Samurai",        # Estilo japonês moderno
    "Corte Americano",      # Estilo americano clássico
    
    # === SERVIÇOS DE BARBA ===
    "Barba Completa",       # Barba inteira aparada e desenhada
    "Barba + Bigode",       # Barba e bigode estilizados
    "Aparar Barba",         # Apenas manutenção da barba
    
    # === OUTROS SERVIÇOS ===
    "Sobrancelha",          # Design de sobrancelha masculina
    
    # === COMBOS PROMOCIONAIS ===
    "Combo Corte + Barba"   # Pacote completo com desconto
]

# Lista dos barbeiros disponíveis no estabelecimento
# Nomes fictícios para demonstração do sistema
BARBEIROS = [
    "João Silva",          # Barbeiro especialista em degradê
    "Pedro Santos",        # Especialista em cortes sociais
    "Carlos Oliveira",     # Expert em barbas
    "Rafael Costa",        # Barbeiro experiente
    "Lucas Ferreira"       # Barbeiro júnior
]

# Status possíveis para agendamentos
# Controla o fluxo de trabalho da barbearia
STATUS_AGENDAMENTO = [
    "Agendado",           # Status inicial - agendamento criado
    "Confirmado",         # Cliente confirmou presença
    "Em Andamento",       # Serviço sendo executado
    "Realizado",          # Serviço finalizado com sucesso
    "Cancelado"           # Agendamento cancelado pelo cliente ou barbearia
]


# =================================================
# DADOS DE EXEMPLO PARA DEMONSTRAÇÃO
# =================================================
# Utilizados apenas para popular o sistema durante desenvolvimento
# e demonstrações. Em produção, estes dados não serão necessários.

# Clientes de exemplo com dados fictícios
CLIENTES_EXEMPLO = [
    {
        "nome": "João da Silva",
        "telefone": "11987654321",
        "email": "joao@email.com",
        "data_nascimento": "15/05/1985",
        "endereco": "Rua das Flores, 123",
        "data_cadastro": "01/01/2024"
    },
    {
        "nome": "Maria Santos",
        "telefone": "11876543210", 
        "email": "maria@email.com",
        "data_nascimento": "22/08/1990",
        "endereco": "Av. Central, 456",
        "data_cadastro": "05/01/2024"
    },
    {
        "nome": "Pedro Oliveira",
        "telefone": "11765432109",
        "email": "pedro@email.com", 
        "data_nascimento": "10/12/1988",
        "endereco": "Rua do Comércio, 789",
        "data_cadastro": "10/01/2024"
    }
]

# Cortes de exemplo para demonstração
CORTES_EXEMPLO = [
    {
        "corte": "Corte Degradê",
        "preco": 35.0,
        "barbeiro": "João Silva",
        "data_hora": "15/01/2024 14:30",
        "observacoes": "Corte degradê baixo"
    },
    {
        "corte": "Combo Corte + Barba",
        "preco": 50.0,
        "barbeiro": "Carlos Oliveira",
        "data_hora": "18/01/2024 16:00",
        "observacoes": "Combo completo"
    }
]

# Agendamentos de exemplo para demonstração
AGENDAMENTOS_EXEMPLO = [
    {
        "cliente": "Maria Santos",
        "data": "25/01/2024",
        "hora": "15:00",
        "servico": "Sobrancelha",
        "barbeiro": "Rafael Costa",
        "status": "Agendado",
        "observacoes": "Cliente prefere design natural"
    },
    {
        "cliente": "João da Silva",
        "data": "26/01/2024", 
        "hora": "10:30",
        "servico": "Corte Social",
        "barbeiro": "Pedro Santos",
        "status": "Confirmado",
        "observacoes": "Reunião importante, corte conservador"
    }
]
