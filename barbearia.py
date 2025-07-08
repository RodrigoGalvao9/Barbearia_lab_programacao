import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.models import Cliente, Corte, Agendamento
from utils.validations import Validador, Formatador
from gui.cadastros import CadastroClienteWindow, CadastroCorteWindow, CadastroAgendamentoWindow


class BarbeariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Barbearia - Versão 2.0")
        self.root.geometry("900x700")
        self.root.configure(bg="#2c3e50")
        
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # === ARQUIVOS DE DADOS ===
        self.usuarios_file = "usuarios.json"
        self.clientes_file = "clientes.json"
        self.cortes_file = "cortes.json"
        self.agendamentos_file = "agendamentos.json"
        
        self.usuarios = self.carregar_dados(self.usuarios_file, {"admin": "1234"})
        self.clientes = self.carregar_dados(self.clientes_file, [])
        self.cortes = self.carregar_dados(self.cortes_file, [])
        self.agendamentos = self.carregar_dados(self.agendamentos_file, [])
        
        self.usuario_logado = None
        self.criar_tela_login()
    
    def carregar_dados(self, arquivo, padrao):
        try:
            if os.path.exists(arquivo):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return padrao
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar {arquivo}: {str(e)}")
            return padrao
    
    def salvar_dados(self, dados, arquivo):
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar {arquivo}: {str(e)}")
            return False
    
    # === INTERFACE LOGIN ===
    def criar_tela_login(self):
        """Cria a tela de login"""
        # Limpar a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both")
        
        # Frame de login
        login_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=3)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=350)
        
        # Título com estilo
        title_label = tk.Label(login_frame, text="🪒 SISTEMA BARBEARIA", 
                              font=("Arial", 22, "bold"), 
                              bg="#34495e", fg="#ecf0f1")
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(login_frame, text="Versão 2.0 - Profissional", 
                                 font=("Arial", 10), 
                                 bg="#34495e", fg="#bdc3c7")
        subtitle_label.pack(pady=(0, 30))
        
        # Campos de entrada com estilo
        self.criar_campo_login(login_frame, "👤 Usuário:", "entry_usuario")
        self.criar_campo_login(login_frame, "🔒 Senha:", "entry_senha", show="*")
        
        # Frame para botões
        btn_frame = tk.Frame(login_frame, bg="#34495e")
        btn_frame.pack(pady=25)
        
        # Botões estilizados
        btn_login = tk.Button(btn_frame, text="🚀 Entrar", command=self.fazer_login,
                             bg="#3498db", fg="white", font=("Arial", 12, "bold"), 
                             width=12, height=2, relief="flat", cursor="hand2")
        btn_login.pack(side="left", padx=8)
        
        btn_cadastrar = tk.Button(btn_frame, text="👤 Cadastrar", command=self.cadastrar_usuario,
                                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"), 
                                 width=12, height=2, relief="flat", cursor="hand2")
        btn_cadastrar.pack(side="left", padx=8)
        

        
        # Eventos
        self.entry_senha.bind("<Return>", lambda e: self.fazer_login())
        self.entry_usuario.focus()
        

    
    def criar_campo_login(self, parent, label_text, attr_name, show=None):
        """Cria um campo estilizado para login"""
        frame = tk.Frame(parent, bg="#34495e")
        frame.pack(pady=8)
        
        tk.Label(frame, text=label_text, font=("Arial", 12), 
                bg="#34495e", fg="#ecf0f1").pack(anchor="w")
        
        entry = tk.Entry(frame, font=("Arial", 12), width=30, relief="flat", 
                        bd=5, bg="#ecf0f1", show=show)
        entry.pack(pady=2)
        
        setattr(self, attr_name, entry)
    
    def adicionar_efeito_hover(self, widget, cor_hover, cor_normal):
        """Adiciona efeito hover aos botões"""
        widget.bind("<Enter>", lambda e: widget.config(bg=cor_hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=cor_normal))
    
    def fazer_login(self):
        """Valida o login do usuário"""
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        if usuario in self.usuarios and self.usuarios[usuario] == senha:
            self.usuario_logado = usuario
            messagebox.showinfo("Sucesso", f"🎉 Bem-vindo, {usuario}!")
            self.criar_menu_principal()
        else:
            messagebox.showerror("Erro", "❌ Usuário ou senha inválidos!")
            self.entry_senha.delete(0, 'end')
            self.entry_senha.focus()
    
    def cadastrar_usuario(self):
        """Cadastra um novo usuário com validações"""
        usuario = simpledialog.askstring("Cadastro", "Digite o nome de usuário:")
        if not usuario:
            return
        
        usuario = usuario.strip()
        if len(usuario) < 3:
            messagebox.showerror("Erro", "Nome de usuário deve ter pelo menos 3 caracteres!")
            return
        
        if usuario in self.usuarios:
            messagebox.showerror("Erro", "Usuário já existe!")
            return
        
        senha = simpledialog.askstring("Cadastro", "Digite a senha:", show="*")
        if not senha:
            return
        
        if len(senha) < 4:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 4 caracteres!")
            return
        
        confirmar_senha = simpledialog.askstring("Cadastro", "Confirme a senha:", show="*")
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "Senhas não coincidem!")
            return
        
        self.usuarios[usuario] = senha
        if self.salvar_dados(self.usuarios, self.usuarios_file):
            messagebox.showinfo("Sucesso", "✅ Usuário cadastrado com sucesso!")
    
    def criar_menu_principal(self):
        """Cria o menu principal da aplicação"""
        # Limpar a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True)
        
        # Barra superior melhorada
        self.criar_barra_superior(main_frame)
        
        # Frame do notebook (abas)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configurar estilo do notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Criar abas
        self.criar_aba_clientes(notebook)
        self.criar_aba_cortes(notebook)
        self.criar_aba_agendamentos(notebook)
        self.criar_aba_relatorios(notebook)
    
    def criar_barra_superior(self, parent):
        """Cria barra superior com informações e botões"""
        top_frame = tk.Frame(parent, bg="#34495e", height=70)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)
        
        # Frame esquerdo - Informações
        left_frame = tk.Frame(top_frame, bg="#34495e")
        left_frame.pack(side="left", fill="y", padx=20)
        
        tk.Label(left_frame, text="🪒 SISTEMA BARBEARIA", 
                font=("Arial", 18, "bold"), bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=5)
        
        tk.Label(left_frame, text=f"👤 Usuário: {self.usuario_logado} | 📊 Dados em tempo real", 
                font=("Arial", 10), bg="#34495e", fg="#bdc3c7").pack(anchor="w")
        
        # Frame direito - Botões
        right_frame = tk.Frame(top_frame, bg="#34495e")
        right_frame.pack(side="right", fill="y", padx=20, pady=15)
        
        tk.Button(right_frame, text="🔄 Atualizar", command=self.atualizar_todas_listas,
                 bg="#3498db", fg="white", font=("Arial", 10), cursor="hand2").pack(side="right", padx=5)
        
        tk.Button(right_frame, text="🚪 Logout", command=self.criar_tela_login,
                 bg="#e74c3c", fg="white", font=("Arial", 10), cursor="hand2").pack(side="right", padx=5)
    
    def criar_aba_clientes(self, notebook):
        """Cria a aba de gerenciamento de clientes"""
        frame_clientes = ttk.Frame(notebook)
        notebook.add(frame_clientes, text="👥 Clientes")
        
        # Frame para botões
        btn_frame = tk.Frame(frame_clientes, bg="#ecf0f1")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        tk.Button(btn_frame, text="➕ Cadastrar Cliente", command=self.abrir_cadastro_cliente,
                 bg="#3498db", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✏️ Editar Cliente", command=self.editar_cliente,
                 bg="#f39c12", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🗑️ Excluir Cliente", command=self.excluir_cliente,
                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista_clientes,
                 bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="right", padx=5)
        
        # Frame para busca
        search_frame = tk.Frame(frame_clientes, bg="#ecf0f1")
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 11), bg="#ecf0f1").pack(side="left")
        self.entry_busca_cliente = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.entry_busca_cliente.pack(side="left", padx=10)
        self.entry_busca_cliente.bind("<KeyRelease>", self.filtrar_clientes)
        
        # Treeview para lista de clientes
        columns = ("Nome", "Telefone", "Email", "Data Nascimento")
        self.tree_clientes = ttk.Treeview(frame_clientes, columns=columns, show="headings", height=18)
        
        # Configurar colunas
        self.tree_clientes.heading("Nome", text="👤 Nome")
        self.tree_clientes.heading("Telefone", text="📱 Telefone")
        self.tree_clientes.heading("Email", text="📧 Email")
        self.tree_clientes.heading("Data Nascimento", text="🎂 Nascimento")
        
        self.tree_clientes.column("Nome", width=250)
        self.tree_clientes.column("Telefone", width=150)
        self.tree_clientes.column("Email", width=200)
        self.tree_clientes.column("Data Nascimento", width=120)
        
        # Scrollbar
        scrollbar_clientes = ttk.Scrollbar(frame_clientes, orient="vertical", command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar_clientes.set)
        
        self.tree_clientes.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar_clientes.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
        
        # Evento de duplo clique
        self.tree_clientes.bind("<Double-1>", lambda e: self.editar_cliente())
        
        self.atualizar_lista_clientes()
    
    def criar_aba_cortes(self, notebook):
        """Cria a aba de registro de cortes"""
        frame_cortes = ttk.Frame(notebook)
        notebook.add(frame_cortes, text="✂️ Cortes")
        
        # Frame para botões
        btn_frame = tk.Frame(frame_cortes, bg="#ecf0f1")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        tk.Button(btn_frame, text="➕ Registrar Corte", command=self.abrir_registro_corte,
                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🗑️ Excluir Corte", command=self.excluir_corte,
                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista_cortes,
                 bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="right", padx=5)
        
        # Frame para busca
        search_frame = tk.Frame(frame_cortes, bg="#ecf0f1")
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 11), bg="#ecf0f1").pack(side="left")
        self.entry_busca_corte = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.entry_busca_corte.pack(side="left", padx=10)
        self.entry_busca_corte.bind("<KeyRelease>", self.filtrar_cortes)
        
        # Treeview para lista de cortes
        columns = ("Cliente", "Tipo", "Preço", "Barbeiro", "Data/Hora")
        self.tree_cortes = ttk.Treeview(frame_cortes, columns=columns, show="headings", height=18)
        
        # Configurar colunas
        self.tree_cortes.heading("Cliente", text="👤 Cliente")
        self.tree_cortes.heading("Tipo", text="✂️ Tipo")
        self.tree_cortes.heading("Preço", text="💰 Preço")
        self.tree_cortes.heading("Barbeiro", text="👨‍💼 Barbeiro")
        self.tree_cortes.heading("Data/Hora", text="📅 Data/Hora")
        
        self.tree_cortes.column("Cliente", width=200)
        self.tree_cortes.column("Tipo", width=180)
        self.tree_cortes.column("Preço", width=100)
        self.tree_cortes.column("Barbeiro", width=120)
        self.tree_cortes.column("Data/Hora", width=150)
        
        # Scrollbar
        scrollbar_cortes = ttk.Scrollbar(frame_cortes, orient="vertical", command=self.tree_cortes.yview)
        self.tree_cortes.configure(yscrollcommand=scrollbar_cortes.set)
        
        self.tree_cortes.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar_cortes.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
        
        self.atualizar_lista_cortes()
    
    def criar_aba_agendamentos(self, notebook):
        """Cria a aba de agendamentos"""
        frame_agendamentos = ttk.Frame(notebook)
        notebook.add(frame_agendamentos, text="📅 Agendamentos")
        
        # Frame para botões
        btn_frame = tk.Frame(frame_agendamentos, bg="#ecf0f1")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        tk.Button(btn_frame, text="➕ Novo Agendamento", command=self.abrir_novo_agendamento,
                 bg="#f39c12", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✅ Confirmar", command=self.confirmar_agendamento,
                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="❌ Cancelar", command=self.cancelar_agendamento,
                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista_agendamentos,
                 bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="right", padx=5)
        
        # Frame para busca
        search_frame = tk.Frame(frame_agendamentos, bg="#ecf0f1")
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 11), bg="#ecf0f1").pack(side="left")
        self.entry_busca_agendamento = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.entry_busca_agendamento.pack(side="left", padx=10)
        self.entry_busca_agendamento.bind("<KeyRelease>", self.filtrar_agendamentos)
        
        # Treeview para lista de agendamentos
        columns = ("Cliente", "Data", "Hora", "Serviço", "Barbeiro", "Status")
        self.tree_agendamentos = ttk.Treeview(frame_agendamentos, columns=columns, show="headings", height=18)
        
        # Configurar colunas
        self.tree_agendamentos.heading("Cliente", text="👤 Cliente")
        self.tree_agendamentos.heading("Data", text="📅 Data")
        self.tree_agendamentos.heading("Hora", text="🕐 Hora")
        self.tree_agendamentos.heading("Serviço", text="✂️ Serviço")
        self.tree_agendamentos.heading("Barbeiro", text="👨‍💼 Barbeiro")
        self.tree_agendamentos.heading("Status", text="📊 Status")
        
        self.tree_agendamentos.column("Cliente", width=180)
        self.tree_agendamentos.column("Data", width=100)
        self.tree_agendamentos.column("Hora", width=80)
        self.tree_agendamentos.column("Serviço", width=150)
        self.tree_agendamentos.column("Barbeiro", width=120)
        self.tree_agendamentos.column("Status", width=100)
        
        # Scrollbar
        scrollbar_agendamentos = ttk.Scrollbar(frame_agendamentos, orient="vertical", command=self.tree_agendamentos.yview)
        self.tree_agendamentos.configure(yscrollcommand=scrollbar_agendamentos.set)
        
        self.tree_agendamentos.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar_agendamentos.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
        
        self.atualizar_lista_agendamentos()
    
    def criar_aba_relatorios(self, notebook):
        """Cria a aba de relatórios"""
        frame_relatorios = ttk.Frame(notebook)
        notebook.add(frame_relatorios, text="📊 Relatórios")
        
        # Frame principal
        main_frame = tk.Frame(frame_relatorios, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(main_frame, text="📊 RELATÓRIOS E ESTATÍSTICAS", 
                font=("Arial", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)
        
        # Frame para estatísticas
        stats_frame = tk.Frame(main_frame, bg="#ecf0f1")
        stats_frame.pack(fill="x", pady=20)
        
        # Criar cards de estatísticas
        self.criar_card_estatistica(stats_frame, "👥", "Total de Clientes", len(self.clientes), "#3498db")
        self.criar_card_estatistica(stats_frame, "✂️", "Cortes Realizados", len(self.cortes), "#27ae60")
        self.criar_card_estatistica(stats_frame, "📅", "Agendamentos", len(self.agendamentos), "#f39c12")
        
        # Calcular receita total
        receita_total = sum(corte.get('preco', 0) for corte in self.cortes)
        self.criar_card_estatistica(stats_frame, "💰", "Receita Total", f"R$ {receita_total:.2f}".replace('.', ','), "#e74c3c")
    
    def criar_card_estatistica(self, parent, icone, titulo, valor, cor):
        """Cria um card de estatística"""
        card = tk.Frame(parent, bg=cor, relief="raised", bd=2)
        card.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(card, text=icone, font=("Arial", 24), bg=cor, fg="white").pack(pady=10)
        tk.Label(card, text=titulo, font=("Arial", 12, "bold"), bg=cor, fg="white").pack()
        tk.Label(card, text=str(valor), font=("Arial", 16, "bold"), bg=cor, fg="white").pack(pady=10)
    
    # Métodos para abrir janelas de cadastro
    def abrir_cadastro_cliente(self):
        """Abre janela de cadastro de cliente"""
        CadastroClienteWindow(self.root, self.callback_cliente_salvo)
    
    def abrir_registro_corte(self):
        """Abre janela de registro de corte"""
        CadastroCorteWindow(self.root, self.clientes, self.callback_corte_salvo)
    
    def abrir_novo_agendamento(self):
        """Abre janela de novo agendamento"""
        CadastroAgendamentoWindow(self.root, self.clientes, self.callback_agendamento_salvo)
    
    # Callbacks para salvar dados
    def callback_cliente_salvo(self, cliente_data):
        """Callback executado quando cliente é salvo"""
        self.clientes.append(cliente_data)
        self.salvar_dados(self.clientes, self.clientes_file)
        self.atualizar_lista_clientes()
    
    def callback_corte_salvo(self, corte_data):
        """Callback executado quando corte é salvo"""
        self.cortes.append(corte_data)
        self.salvar_dados(self.cortes, self.cortes_file)
        self.atualizar_lista_cortes()
    
    def callback_agendamento_salvo(self, agendamento_data):
        """Callback executado quando agendamento é salvo"""
        self.agendamentos.append(agendamento_data)
        self.salvar_dados(self.agendamentos, self.agendamentos_file)
        self.atualizar_lista_agendamentos()
    
    # Métodos para atualizar listas
    def atualizar_lista_clientes(self):
        """Atualiza a lista de clientes na interface"""
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        for cliente in self.clientes:
            self.tree_clientes.insert("", "end", values=(
                cliente.get("nome", ""),
                cliente.get("telefone", ""),
                cliente.get("email", ""),
                cliente.get("data_nascimento", "")
            ))
    
    def atualizar_lista_cortes(self):
        """Atualiza a lista de cortes na interface"""
        for item in self.tree_cortes.get_children():
            self.tree_cortes.delete(item)
        
        for corte in self.cortes:
            preco = corte.get("preco", 0)
            preco_formatado = Formatador.formatar_preco(preco) if preco else "R$ 0,00"
            
            self.tree_cortes.insert("", "end", values=(
                corte.get("cliente", ""),
                corte.get("corte", ""),
                preco_formatado,
                corte.get("barbeiro", ""),
                corte.get("data_hora", "")
            ))
    
    def atualizar_lista_agendamentos(self):
        """Atualiza a lista de agendamentos na interface"""
        for item in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(item)
        
        for agendamento in self.agendamentos:
            self.tree_agendamentos.insert("", "end", values=(
                agendamento.get("cliente", ""),
                agendamento.get("data", ""),
                agendamento.get("hora", ""),
                agendamento.get("servico", ""),
                agendamento.get("barbeiro", ""),
                agendamento.get("status", "")
            ))
    
    def atualizar_todas_listas(self):
        """Atualiza todas as listas"""
        self.atualizar_lista_clientes()
        self.atualizar_lista_cortes()
        self.atualizar_lista_agendamentos()
        messagebox.showinfo("Sucesso", "✅ Todas as listas foram atualizadas!")
    
    # Métodos para filtros de busca
    def filtrar_clientes(self, event=None):
        """Filtra clientes conforme busca"""
        termo = self.entry_busca_cliente.get().lower()
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        for cliente in self.clientes:
            if (termo in cliente.get("nome", "").lower() or 
                termo in cliente.get("telefone", "").lower() or
                termo in cliente.get("email", "").lower()):
                
                self.tree_clientes.insert("", "end", values=(
                    cliente.get("nome", ""),
                    cliente.get("telefone", ""),
                    cliente.get("email", ""),
                    cliente.get("data_nascimento", "")
                ))
    
    def filtrar_cortes(self, event=None):
        """Filtra cortes conforme busca"""
        termo = self.entry_busca_corte.get().lower()
        for item in self.tree_cortes.get_children():
            self.tree_cortes.delete(item)
        
        for corte in self.cortes:
            if (termo in corte.get("cliente", "").lower() or 
                termo in corte.get("corte", "").lower() or
                termo in corte.get("barbeiro", "").lower()):
                
                preco = corte.get("preco", 0)
                preco_formatado = Formatador.formatar_preco(preco) if preco else "R$ 0,00"
                
                self.tree_cortes.insert("", "end", values=(
                    corte.get("cliente", ""),
                    corte.get("corte", ""),
                    preco_formatado,
                    corte.get("barbeiro", ""),
                    corte.get("data_hora", "")
                ))
    
    def filtrar_agendamentos(self, event=None):
        """Filtra agendamentos conforme busca"""
        termo = self.entry_busca_agendamento.get().lower()
        for item in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(item)
        
        for agendamento in self.agendamentos:
            if (termo in agendamento.get("cliente", "").lower() or 
                termo in agendamento.get("servico", "").lower() or
                termo in agendamento.get("barbeiro", "").lower() or
                termo in agendamento.get("status", "").lower()):
                
                self.tree_agendamentos.insert("", "end", values=(
                    agendamento.get("cliente", ""),
                    agendamento.get("data", ""),
                    agendamento.get("hora", ""),
                    agendamento.get("servico", ""),
                    agendamento.get("barbeiro", ""),
                    agendamento.get("status", "")
                ))
    
    # Métodos para edição e exclusão
    def editar_cliente(self):
        """Edita o cliente selecionado"""
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        # Implementar edição de cliente
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de edição em desenvolvimento!")
    
    def excluir_cliente(self):
        """Exclui o cliente selecionado"""
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
            return
        
        # Implementar exclusão
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de exclusão em desenvolvimento!")
    
    def excluir_corte(self):
        """Exclui o corte selecionado"""
        selected = self.tree_cortes.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um corte para excluir!")
            return
        
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de exclusão em desenvolvimento!")
    
    def confirmar_agendamento(self):
        """Confirma o agendamento selecionado"""
        selected = self.tree_agendamentos.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento para confirmar!")
            return
        
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade em desenvolvimento!")
    
    def cancelar_agendamento(self):
        """Cancela o agendamento selecionado"""
        selected = self.tree_agendamentos.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento para cancelar!")
            return
        
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade em desenvolvimento!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BarbeariaApp(root)
    root.mainloop()
