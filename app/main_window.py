"""
Módulo da janela principal com todas as abas
"""
import tkinter as tk
from tkinter import ttk
from app.data_manager import DataManager
from app.tabs.clientes_tab import ClientesTab
from app.tabs.cortes_tab import CortesTab
from app.tabs.agendamentos_tab import AgendamentosTab
from app.tabs.relatorios_tab import RelatoriosTab


class MainWindow:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.data_manager = DataManager()
        self.main_frame = None
        
    def show(self):
        """Exibe a janela principal"""
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(fill="both", expand=True)
        
        # Notebook (abas) - criar primeiro para referenciar no header
        self.criar_abas()
        
        # Header - criar depois para usar referências das abas
        self.criar_header()
    
    def criar_header(self):
        """Cria o cabeçalho da aplicação"""
        header_frame = tk.Frame(self.main_frame, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Container do conteúdo do header
        content_frame = tk.Frame(header_frame, bg="#2c3e50")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        titulo = tk.Label(content_frame, text="🪒 Sistema de Barbearia", 
                         font=("Arial", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
        titulo.pack(side="left")
        
        # Botões de ação rápida no header
        action_frame = tk.Frame(content_frame, bg="#2c3e50")
        action_frame.pack(side="left", padx=20)
        
        tk.Button(action_frame, text="➕ Cliente", command=self.clientes_tab.cadastrar_cliente,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(side="left", padx=2)
        
        tk.Button(action_frame, text="✂️ Corte", command=self.cortes_tab.registrar_corte,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(side="left", padx=2)
        
        tk.Button(action_frame, text="📅 Agendar", command=self.agendamentos_tab.novo_agendamento,
                 bg="#f39c12", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(side="left", padx=2)
        
        # Info do usuário
        user_info = tk.Label(content_frame, text=f"Usuário: {self.usuario}", 
                           font=("Arial", 12), bg="#2c3e50", fg="#bdc3c7")
        user_info.pack(side="right")
        
        # Botão de logout
        btn_logout = tk.Button(content_frame, text="🚪 Sair", command=self.logout,
                             bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                             cursor="hand2")
        btn_logout.pack(side="right", padx=(0, 10))
        
        # Botão de atualizar tudo
        btn_refresh = tk.Button(content_frame, text="🔄 Atualizar Tudo", 
                              command=self.atualizar_todas_abas,
                              bg="#95a5a6", fg="white", font=("Arial", 10, "bold"),
                              cursor="hand2")
        btn_refresh.pack(side="right", padx=(0, 10))
    
    def criar_abas(self):
        """Cria o sistema de abas"""
        # Notebook
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar abas
        self.clientes_tab = ClientesTab(notebook, self.data_manager)
        self.cortes_tab = CortesTab(notebook, self.data_manager)
        self.agendamentos_tab = AgendamentosTab(notebook, self.data_manager)
        self.relatorios_tab = RelatoriosTab(notebook, self.data_manager)
        
        # Configurar callbacks entre abas
        self.configurar_callbacks()
    
    def configurar_callbacks(self):
        """Configura callbacks entre abas para sincronização"""
        # Quando cliente é salvo, atualizar aba de agendamentos
        self.clientes_tab.set_callback(self.agendamentos_tab.atualizar_lista)
        
        # Quando agendamento é realizado, criar corte automaticamente
        self.agendamentos_tab.set_callback(self.cortes_tab.atualizar_lista)
    
    def atualizar_todas_abas(self):
        """Atualiza todas as abas"""
        self.clientes_tab.atualizar_lista()
        self.cortes_tab.atualizar_lista()
        self.agendamentos_tab.atualizar_lista()
        self.relatorios_tab.atualizar_relatorios()
    
    def logout(self):
        """Faz logout e volta para tela de login"""
        if self.main_frame:
            self.main_frame.destroy()
        
        from app.login import LoginManager
        login_manager = LoginManager(self.root)
        login_manager.show_login(self.on_login_success)
    
    def on_login_success(self, usuario):
        """Callback para novo login"""
        from app.main_window import MainWindow
        main_window = MainWindow(self.root, usuario)
        main_window.show()
