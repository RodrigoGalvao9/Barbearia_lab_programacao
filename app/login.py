"""
Módulo de Gerenciamento de Login e Registro - Sistema de Barbearia
================================================================

Este módulo é responsável por:
- Autenticação de usuários existentes
- Registro de novos usuários
- Validação de credenciais
- Persistência de dados de usuários em JSON
- Interface gráfica de login/registro

Funcionalidades:
- Login com usuário e senha
- Registro de novos usuários com validações
- Salvamento automático de usuários
- Interface responsiva e moderna
- Tratamento de erros de validação

Classes:
- LoginManager: Gerencia todo o processo de autenticação

Arquivos utilizados:
- data/usuarios.json: Armazena dados dos usuários
"""
import tkinter as tk
from tkinter import messagebox
import json
import os


class LoginManager:
    """
    Gerenciador de login e registro de usuários.
    
    Responsável por toda a autenticação do sistema:
    - Exibir tela de login
    - Validar credenciais
    - Permitir registro de novos usuários
    - Gerenciar arquivo de usuários
    
    Attributes:
        root (tk.Tk): Janela principal
        usuarios_file (str): Caminho do arquivo de usuários
        usuarios (dict): Dicionário com usuários carregados
        callback_success (function): Callback para login bem-sucedido
        login_frame (tk.Frame): Frame da interface de login
    """
    
    def __init__(self, root):
        """
        Inicializa o gerenciador de login.
        
        Args:
            root (tk.Tk): Janela principal do sistema
        """
        self.root = root
        self.usuarios_file = "data/usuarios.json"  # Arquivo de persistência
        self.usuarios = self.carregar_usuarios()   # Carrega usuários existentes
        self.callback_success = None               # Callback para sucesso
        self.login_frame = None                    # Frame da interface
        
    def carregar_usuarios(self):
        """
        Carrega usuários do arquivo JSON.
        
        Tenta carregar o arquivo data/usuarios.json. Se não existir ou
        houver erro, retorna um usuário padrão (admin/1234).
        
        Returns:
            dict: Dicionário com usuários {usuario: senha}
        """
        try:
            if os.path.exists(self.usuarios_file):
                with open(self.usuarios_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            # Se arquivo não existe, cria usuário padrão
            return {"admin": "1234"}
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar usuários: {str(e)}")
            return {"admin": "1234"}
    
    def show_login(self, callback_success):
        """Exibe a tela de login"""
        self.callback_success = callback_success
        
        # Frame principal de login
        self.login_frame = tk.Frame(self.root, bg="#34495e")
        self.login_frame.pack(fill="both", expand=True)
        
        # Container centralizado
        container = tk.Frame(self.login_frame, bg="#34495e")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = tk.Label(container, text="🪒 SISTEMA DE BARBEARIA", 
                         font=("Arial", 24, "bold"), bg="#34495e", fg="#ecf0f1")
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = tk.Label(container, text="Faça login para continuar", 
                           font=("Arial", 14), bg="#34495e", fg="#bdc3c7")
        subtitulo.pack(pady=(0, 30))
        
        # Campos de login
        self.criar_campo_login(container, "👤 Usuário:", "entry_usuario")
        self.criar_campo_login(container, "🔒 Senha:", "entry_senha", show="*")
        
        # Botão de login
        btn_login = tk.Button(container, text="ENTRAR", command=self.fazer_login,
                             bg="#27ae60", fg="white", font=("Arial", 14, "bold"),
                             width=20, cursor="hand2", relief="flat", bd=0)
        btn_login.pack(pady=30)
        
        # Botão de registro
        btn_registro = tk.Button(container, text="REGISTRAR USUÁRIO", command=self.mostrar_registro,
                                bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                                width=20, cursor="hand2", relief="flat", bd=0)
        btn_registro.pack(pady=(0, 10))
        
        # Focar no campo usuário
        self.entry_usuario.focus()
        
        # Bind Enter para login
        self.root.bind('<Return>', lambda e: self.fazer_login())
    
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
    
    def fazer_login(self):
        """Processa o login do usuário"""
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha usuário e senha!")
            return
        
        if usuario in self.usuarios and self.usuarios[usuario] == senha:
            if self.callback_success:
                self.callback_success(usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.focus()
    
    def hide_login(self):
        """Oculta a tela de login"""
        if self.login_frame:
            self.login_frame.destroy()
            self.login_frame = None
    
    def mostrar_registro(self):
        """Exibe a janela de registro de usuário"""
        registro_window = tk.Toplevel(self.root)
        registro_window.title("Registrar Usuário")
        registro_window.geometry("450x400")
        registro_window.configure(bg="#34495e")
        registro_window.resizable(False, False)
        
        # Centralizar janela
        registro_window.transient(self.root)
        registro_window.grab_set()
        
        # Container centralizado
        container = tk.Frame(registro_window, bg="#34495e")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = tk.Label(container, text="📝 REGISTRAR USUÁRIO", 
                         font=("Arial", 18, "bold"), bg="#34495e", fg="#ecf0f1")
        titulo.pack(pady=20)
        
        # Campos
        self.criar_campo_registro(container, "👤 Usuário:", "reg_entry_usuario")
        self.criar_campo_registro(container, "🔒 Senha:", "reg_entry_senha", show="*")
        self.criar_campo_registro(container, "🔒 Confirmar Senha:", "reg_entry_confirma", show="*")
        
        # Botões
        btn_frame = tk.Frame(container, bg="#34495e")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="REGISTRAR", command=lambda: self.fazer_registro(registro_window),
                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                 width=15, cursor="hand2", relief="flat", bd=0).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="CANCELAR", command=registro_window.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                 width=15, cursor="hand2", relief="flat", bd=0).pack(side="left", padx=5)
        
        # Focar no campo usuário
        self.reg_entry_usuario.focus()
    
    def criar_campo_registro(self, parent, label_text, attr_name, show=None):
        """Cria um campo estilizado para registro"""
        frame = tk.Frame(parent, bg="#34495e")
        frame.pack(pady=8)
        
        tk.Label(frame, text=label_text, font=("Arial", 12), 
                bg="#34495e", fg="#ecf0f1").pack(anchor="w")
        
        entry = tk.Entry(frame, font=("Arial", 12), width=30, relief="flat", 
                        bd=5, bg="#ecf0f1", show=show)
        entry.pack(pady=2)
        
        setattr(self, attr_name, entry)
    
    def fazer_registro(self, window):
        """Processa o registro do usuário"""
        usuario = self.reg_entry_usuario.get().strip()
        senha = self.reg_entry_senha.get()
        confirma = self.reg_entry_confirma.get()
        
        # Validações
        if not usuario or not senha or not confirma:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        if len(usuario) < 3:
            messagebox.showerror("Erro", "Usuário deve ter pelo menos 3 caracteres!")
            return
        
        if len(senha) < 4:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 4 caracteres!")
            return
        
        if senha != confirma:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        if usuario in self.usuarios:
            messagebox.showerror("Erro", "Usuário já existe!")
            return
        
        # Salvar usuário
        self.usuarios[usuario] = senha
        self.salvar_usuarios()
        
        messagebox.showinfo("Sucesso", f"Usuário '{usuario}' registrado com sucesso!")
        window.destroy()
    
    def salvar_usuarios(self):
        """Salva usuários no arquivo JSON"""
        try:
            # Criar diretório data se não existir
            os.makedirs(os.path.dirname(self.usuarios_file), exist_ok=True)
            
            with open(self.usuarios_file, 'w', encoding='utf-8') as f:
                json.dump(self.usuarios, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar usuários: {str(e)}")
