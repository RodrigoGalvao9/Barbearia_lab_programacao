"""
Aba de gerenciamento de clientes
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.cadastros import CadastroClienteWindow


class ClientesTab:
    def __init__(self, notebook, data_manager):
        self.notebook = notebook
        self.data_manager = data_manager
        self.callback = None
        
        # Criar frame da aba
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="👥 Clientes")
        
        self.criar_interface()
        self.atualizar_lista()
    
    def set_callback(self, callback):
        """Define callback para quando dados são alterados"""
        self.callback = callback
    
    def criar_interface(self):
        """Cria a interface da aba de clientes"""
        # Frame para botões
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        tk.Button(btn_frame, text="➕ Cadastrar Cliente", command=self.cadastrar_cliente,
                 bg="#3498db", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✏️ Editar Cliente", command=self.editar_cliente,
                 bg="#f39c12", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🗑️ Excluir Cliente", command=self.excluir_cliente,
                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista,
                 bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="right", padx=5)
        
        # Frame para busca
        search_frame = tk.Frame(self.frame, bg="#ecf0f1")
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 11), bg="#ecf0f1").pack(side="left")
        self.entry_busca = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.entry_busca.pack(side="left", padx=10)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_clientes)
        
        # Treeview
        columns = ("Nome", "Telefone", "Email", "Data Nascimento")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=18)
        
        # Configurar colunas
        self.tree.heading("Nome", text="👤 Nome")
        self.tree.heading("Telefone", text="📱 Telefone")
        self.tree.heading("Email", text="📧 Email")
        self.tree.heading("Data Nascimento", text="🎂 Nascimento")
        
        self.tree.column("Nome", width=250)
        self.tree.column("Telefone", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Data Nascimento", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
        
        # Evento de duplo clique
        self.tree.bind("<Double-1>", lambda e: self.editar_cliente())
    
    def atualizar_lista(self):
        """Atualiza a lista de clientes"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for cliente in self.data_manager.get_clientes():
            self.tree.insert("", "end", values=(
                cliente.get("nome", ""),
                cliente.get("telefone", ""),
                cliente.get("email", ""),
                cliente.get("data_nascimento", "")
            ))
    
    def filtrar_clientes(self, event=None):
        """Filtra clientes conforme busca"""
        termo = self.entry_busca.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for cliente in self.data_manager.get_clientes():
            if (termo in cliente.get("nome", "").lower() or 
                termo in cliente.get("telefone", "").lower() or
                termo in cliente.get("email", "").lower()):
                
                self.tree.insert("", "end", values=(
                    cliente.get("nome", ""),
                    cliente.get("telefone", ""),
                    cliente.get("email", ""),
                    cliente.get("data_nascimento", "")
                ))
    
    def cadastrar_cliente(self):
        """Abre janela de cadastro de cliente"""
        CadastroClienteWindow(self.frame, self.callback_cliente_salvo)
    
    def editar_cliente(self):
        """Edita o cliente selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        # Obter dados do cliente selecionado
        item = selected[0]
        values = self.tree.item(item, 'values')
        nome_cliente = values[0]
        
        # Encontrar cliente na lista
        clientes = self.data_manager.get_clientes()
        for i, cliente in enumerate(clientes):
            if cliente['nome'] == nome_cliente:
                CadastroClienteWindow(self.frame, 
                                    lambda dados: self.callback_cliente_editado(dados, i),
                                    cliente)
                break
    
    def excluir_cliente(self):
        """Exclui o cliente selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
            return
        
        # Obter dados do cliente selecionado
        item = selected[0]
        values = self.tree.item(item, 'values')
        nome_cliente = values[0]
        
        # Confirmar exclusão
        resposta = messagebox.askyesno("Confirmar Exclusão", 
                                      f"Tem certeza que deseja excluir o cliente '{nome_cliente}'?\n\n"
                                      "Esta ação não pode ser desfeita!")
        if not resposta:
            return
        
        # Encontrar e remover cliente
        clientes = self.data_manager.get_clientes()
        for i, cliente in enumerate(clientes):
            if cliente['nome'] == nome_cliente:
                self.data_manager.delete_cliente(i)
                break
        
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Cliente '{nome_cliente}' excluído com sucesso!")
        
        if self.callback:
            self.callback()
    
    def callback_cliente_salvo(self, cliente_data):
        """Callback executado quando cliente é salvo"""
        self.data_manager.add_cliente(cliente_data)
        self.atualizar_lista()
        
        if self.callback:
            self.callback()
    
    def callback_cliente_editado(self, cliente_data, index):
        """Callback executado quando cliente é editado"""
        self.data_manager.update_cliente(index, cliente_data)
        self.atualizar_lista()
        
        if self.callback:
            self.callback()
