"""
Módulo Principal da Aplicação - Sistema de Barbearia v2.0
=========================================================

Este módulo contém a classe BarbeariaApp que orquestra todo o sistema.
É responsável por:
- Configurar a janela principal
- Gerenciar o fluxo login -> janela principal
- Coordenar os diferentes módulos
- Controlar o ciclo de vida da aplicação

Classes:
- BarbeariaApp: Classe principal que controla toda a aplicação

Dependências:
- app.login: Para gerenciamento de login/registro de usuários
- app.main_window: Para a janela principal com abas
"""
import tkinter as tk
from tkinter import messagebox
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.login import LoginManager
from app.main_window import MainWindow


class BarbeariaApp:
    """
    Classe principal do Sistema de Barbearia.
    
    Coordena todos os componentes da aplicação:
    - Configuração da janela principal
    - Gerenciamento de login
    - Transição para interface principal
    - Controle do fluxo da aplicação
    
    Attributes:
        root (tk.Tk): Janela principal do Tkinter
        login_manager (LoginManager): Gerenciador de login/registro
        main_window (MainWindow): Janela principal com funcionalidades
    """
    
    def __init__(self, root):
        """
        Inicializa a aplicação principal.
        
        Args:
            root (tk.Tk): Janela root do Tkinter
        """
        self.root = root
        
        # Configurações da janela principal
        self.root.title("Sistema de Barbearia - Versão 2.0")
        self.root.geometry("900x700")  # Tamanho inicial adequado
        self.root.configure(bg="#2c3e50")  # Fundo escuro elegante
        
        # Tentar carregar ícone (opcional)
        try:
            self.root.iconbitmap('icon.ico')
        except (FileNotFoundError, tk.TclError):
            # Ignora se ícone não existe
            pass
        
        # Inicializar componentes principais
        self.login_manager = LoginManager(self.root)  # Gerenciador de login
        self.main_window = None  # Será inicializado após login
        
        # Iniciar com tela de login
        self.login_manager.show_login(self.on_login_success)
    
    def on_login_success(self, usuario):
        """
        Callback executado após login bem-sucedido.
        
        Responsabilidades:
        - Ocultar tela de login
        - Criar janela principal com funcionalidades
        - Passar dados do usuário logado
        
        Args:
            usuario (str): Nome do usuário que fez login
        """
        # Ocultar tela de login
        self.login_manager.hide_login()
        
        # Criar e exibir janela principal
        self.main_window = MainWindow(self.root, usuario)
        self.main_window.show()
