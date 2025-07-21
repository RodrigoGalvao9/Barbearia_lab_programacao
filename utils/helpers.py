"""
=================================================
FUNÇÕES AUXILIARES DO SISTEMA
=================================================

Este módulo contém funções utilitárias reutilizáveis
em todo o sistema, facilitando operações comuns e
padronizando comportamentos.

=================================================
"""

import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime, timedelta
from core.config import config


def show_info(title, message):
    """
    Exibe mensagem informativa padronizada.
    
    Args:
        title (str): Título da mensagem
        message (str): Conteúdo da mensagem
    """
    messagebox.showinfo(title, message)


def show_error(title, message):
    """
    Exibe mensagem de erro padronizada.
    
    Args:
        title (str): Título da mensagem
        message (str): Conteúdo da mensagem
    """
    messagebox.showerror(title, message)


def show_warning(title, message):
    """
    Exibe mensagem de aviso padronizada.
    
    Args:
        title (str): Título da mensagem
        message (str): Conteúdo da mensagem
    """
    messagebox.showwarning(title, message)


def ask_yes_no(title, message):
    """
    Exibe diálogo de confirmação.
    
    Args:
        title (str): Título da mensagem
        message (str): Conteúdo da mensagem
        
    Returns:
        bool: True se usuário confirmou
    """
    return messagebox.askyesno(title, message)


def center_window(window, width=None, height=None):
    """
    Centraliza uma janela na tela.
    
    Args:
        window: Janela Tkinter
        width (int, optional): Largura desejada
        height (int, optional): Altura desejada
    """
    window.update_idletasks()
    
    # Usar dimensões atuais se não especificado
    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()
    
    # Calcular posição central
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f'{width}x{height}+{x}+{y}')


def create_styled_button(parent, text, command, style='default', **kwargs):
    """
    Cria botão com estilo padronizado.
    
    Args:
        parent: Widget pai
        text (str): Texto do botão
        command: Função a executar
        style (str): Estilo do botão
        **kwargs: Argumentos adicionais
        
    Returns:
        tk.Button: Botão criado
    """
    # Estilos predefinidos
    styles = {
        'default': {
            'bg': config.get_color('info'),
            'fg': config.get_color('text_light'),
            'font': config.get_font('button')
        },
        'success': {
            'bg': config.get_color('success'),
            'fg': config.get_color('text_light'),
            'font': config.get_font('button')
        },
        'danger': {
            'bg': config.get_color('danger'),
            'fg': config.get_color('text_light'),
            'font': config.get_font('button')
        },
        'warning': {
            'bg': config.get_color('warning'),
            'fg': config.get_color('text_light'),
            'font': config.get_font('button')
        },
        'secondary': {
            'bg': config.get_color('bg_medium'),
            'fg': config.get_color('text_light'),
            'font': config.get_font('button')
        }
    }
    
    # Aplicar estilo
    button_style = styles.get(style, styles['default'])
    button_style.update(kwargs)
    
    # Configurações padrão
    default_config = {
        'relief': 'flat',
        'cursor': 'hand2',
        'width': config.BUTTON_WIDTH,
        'height': config.BUTTON_HEIGHT
    }
    
    # Mesclar configurações
    final_config = {**default_config, **button_style}
    
    return tk.Button(parent, text=text, command=command, **final_config)


def create_styled_entry(parent, placeholder='', **kwargs):
    """
    Cria campo de entrada com estilo padronizado.
    
    Args:
        parent: Widget pai
        placeholder (str): Texto de placeholder
        **kwargs: Argumentos adicionais
        
    Returns:
        tk.Entry: Campo de entrada criado
    """
    default_config = {
        'font': config.get_font('default'),
        'width': config.ENTRY_WIDTH,
        'relief': 'solid',
        'bd': 1
    }
    
    final_config = {**default_config, **kwargs}
    entry = tk.Entry(parent, **final_config)
    
    # Adicionar placeholder se especificado
    if placeholder:
        add_placeholder(entry, placeholder)
    
    return entry


def add_placeholder(entry, placeholder_text):
    """
    Adiciona placeholder a um campo de entrada.
    
    Args:
        entry: Campo de entrada
        placeholder_text (str): Texto do placeholder
    """
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(fg=config.get_color('text_dark'))
    
    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg=config.get_color('text_muted'))
    
    # Configurar estado inicial
    entry.insert(0, placeholder_text)
    entry.config(fg=config.get_color('text_muted'))
    
    # Vincular eventos
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)


def format_currency(value):
    """
    Formata valor como moeda brasileira.
    
    Args:
        value (float): Valor numérico
        
    Returns:
        str: Valor formatado como moeda
    """
    try:
        return f"R$ {float(value):.2f}".replace('.', ',')
    except (ValueError, TypeError):
        return "R$ 0,00"


def parse_currency(currency_str):
    """
    Converte string de moeda para float.
    
    Args:
        currency_str (str): String de moeda
        
    Returns:
        float: Valor numérico
    """
    try:
        # Remover símbolos e converter
        clean_str = re.sub(r'[R$\s]', '', currency_str)
        clean_str = clean_str.replace(',', '.')
        return float(clean_str)
    except (ValueError, TypeError):
        return 0.0


def format_phone(phone):
    """
    Formata número de telefone brasileiro.
    
    Args:
        phone (str): Número de telefone
        
    Returns:
        str: Telefone formatado
    """
    # Remover caracteres não numéricos
    digits = re.sub(r'[^\d]', '', phone)
    
    if len(digits) == 11:
        # Celular: (xx) 9xxxx-xxxx
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    elif len(digits) == 10:
        # Fixo: (xx) xxxx-xxxx
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    else:
        return phone  # Retornar original se não conseguir formatar


def format_date(date_obj):
    """
    Formata objeto datetime como string brasileira.
    
    Args:
        date_obj (datetime): Objeto datetime
        
    Returns:
        str: Data formatada (DD/MM/AAAA)
    """
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%d/%m/%Y")
    return str(date_obj)


def format_datetime(datetime_obj):
    """
    Formata objeto datetime como string brasileira com hora.
    
    Args:
        datetime_obj (datetime): Objeto datetime
        
    Returns:
        str: Data e hora formatadas (DD/MM/AAAA HH:MM)
    """
    if isinstance(datetime_obj, datetime):
        return datetime_obj.strftime("%d/%m/%Y %H:%M")
    return str(datetime_obj)


def parse_date(date_str):
    """
    Converte string de data para objeto datetime.
    
    Args:
        date_str (str): String de data (DD/MM/AAAA)
        
    Returns:
        datetime or None: Objeto datetime ou None se inválido
    """
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None


def parse_time(time_str):
    """
    Converte string de hora para objeto time.
    
    Args:
        time_str (str): String de hora (HH:MM)
        
    Returns:
        time or None: Objeto time ou None se inválido
    """
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None


def get_next_business_day(date_obj=None, days_ahead=1):
    """
    Obtém próximo dia útil.
    
    Args:
        date_obj (datetime, optional): Data base
        days_ahead (int): Dias à frente
        
    Returns:
        datetime: Próximo dia útil
    """
    if date_obj is None:
        date_obj = datetime.now()
    
    next_day = date_obj + timedelta(days=days_ahead)
    
    # Pular fins de semana (6=sábado, 0=domingo)
    while next_day.weekday() > 4:  # Segunda a sexta = 0-4
        next_day += timedelta(days=1)
    
    return next_day


def is_valid_email(email):
    """
    Valida formato de email.
    
    Args:
        email (str): Endereço de email
        
    Returns:
        bool: True se email válido
    """
    if not email:
        return True  # Email é opcional
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone):
    """
    Valida número de telefone brasileiro.
    
    Args:
        phone (str): Número de telefone
        
    Returns:
        bool: True se telefone válido
    """
    # Remover caracteres não numéricos
    digits = re.sub(r'[^\d]', '', phone)
    
    # Verificar tamanho
    if len(digits) not in [10, 11]:
        return False
    
    # Verificar se não são todos números iguais
    if len(set(digits)) == 1:
        return False
    
    return True


def is_valid_cpf(cpf):
    """
    Valida número de CPF.
    
    Args:
        cpf (str): Número do CPF
        
    Returns:
        bool: True se CPF válido
    """
    # Remover caracteres não numéricos
    cpf = re.sub(r'[^\d]', '', cpf)
    
    # Verificar tamanho
    if len(cpf) != 11:
        return False
    
    # Verificar se não são todos números iguais
    if len(set(cpf)) == 1:
        return False
    
    # Validar dígitos verificadores
    def calculate_digit(cpf_digits, position):
        sum_digits = sum(int(digit) * weight for digit, weight in zip(cpf_digits, range(position, 1, -1)))
        remainder = sum_digits % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Verificar primeiro dígito
    first_digit = calculate_digit(cpf[:9], 10)
    if int(cpf[9]) != first_digit:
        return False
    
    # Verificar segundo dígito
    second_digit = calculate_digit(cpf[:10], 11)
    if int(cpf[10]) != second_digit:
        return False
    
    return True


def sanitize_filename(filename):
    """
    Remove caracteres inválidos de nome de arquivo.
    
    Args:
        filename (str): Nome do arquivo
        
    Returns:
        str: Nome sanitizado
    """
    # Caracteres inválidos para nomes de arquivo
    invalid_chars = r'<>:"/\|?*'
    
    # Substituir caracteres inválidos
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remover espaços extras e caracteres de controle
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    return filename


def truncate_text(text, max_length=50, suffix="..."):
    """
    Trunca texto longo adicionando sufixo.
    
    Args:
        text (str): Texto original
        max_length (int): Comprimento máximo
        suffix (str): Sufixo para texto truncado
        
    Returns:
        str: Texto truncado
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def get_system_info():
    """
    Obtém informações do sistema.
    
    Returns:
        dict: Informações do sistema
    """
    import platform
    import sys
    
    return {
        'app_name': config.APP_NAME,
        'app_version': config.APP_VERSION,
        'python_version': sys.version,
        'platform': platform.platform(),
        'system': platform.system(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'timestamp': datetime.now().isoformat()
    }


class ProgressTracker:
    """
    Rastreador de progresso para operações longas.
    """
    
    def __init__(self, total_steps, callback=None):
        """
        Inicializa rastreador de progresso.
        
        Args:
            total_steps (int): Total de passos
            callback: Função chamada a cada passo
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.callback = callback
        self.start_time = datetime.now()
    
    def step(self, description=""):
        """
        Avança um passo no progresso.
        
        Args:
            description (str): Descrição do passo atual
        """
        self.current_step += 1
        progress = (self.current_step / self.total_steps) * 100
        
        if self.callback:
            self.callback({
                'step': self.current_step,
                'total': self.total_steps,
                'progress': progress,
                'description': description,
                'elapsed_time': datetime.now() - self.start_time
            })
    
    def is_complete(self):
        """
        Verifica se o progresso está completo.
        
        Returns:
            bool: True se completo
        """
        return self.current_step >= self.total_steps
