"""
Aba de gerenciamento de cortes (sem campo cliente)
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.cadastros import CadastroCorteWindow
from utils.validations import Formatador


class CortesTab:
    def __init__(self, notebook, data_manager):
        self.notebook = notebook
        self.data_manager = data_manager
        self.callback = None
        
        # Criar frame da aba
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="✂️ Cortes")
        
        self.criar_interface()
        self.atualizar_lista()
    
    def set_callback(self, callback):
        """Define callback para quando dados são alterados"""
        self.callback = callback
    
    def criar_interface(self):
        """Cria a interface da aba de cortes"""
        # Frame para botões
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        tk.Button(btn_frame, text="➕ Registrar Corte", command=self.registrar_corte,
                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✏️ Editar Corte", command=self.editar_corte,
                 bg="#3498db", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🗑️ Excluir Corte", command=self.excluir_corte,
                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista,
                 bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="right", padx=5)
        
        # Frame para busca
        search_frame = tk.Frame(self.frame, bg="#ecf0f1")
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 11), bg="#ecf0f1").pack(side="left")
        self.entry_busca = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.entry_busca.pack(side="left", padx=10)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_cortes)
        
        # Treeview
        columns = ("Tipo", "Preço", "Barbeiro", "Data/Hora")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=18)
        
        # Configurar colunas
        self.tree.heading("Tipo", text="✂️ Tipo")
        self.tree.heading("Preço", text="💰 Preço")
        self.tree.heading("Barbeiro", text="👨‍💼 Barbeiro")
        self.tree.heading("Data/Hora", text="📅 Data/Hora")
        
        self.tree.column("Tipo", width=250)
        self.tree.column("Preço", width=120)
        self.tree.column("Barbeiro", width=150)
        self.tree.column("Data/Hora", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
    
    def atualizar_lista(self):
        """Atualiza a lista de cortes"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for corte in self.data_manager.get_cortes():
            # Formatação do preço
            preco = corte.get("preco", "0")
            try:
                if isinstance(preco, str):
                    preco_float = float(preco.replace(',', '.'))
                else:
                    preco_float = float(preco)
                preco_formatado = f"R$ {preco_float:.2f}".replace('.', ',')
            except (ValueError, TypeError):
                preco_formatado = "R$ 0,00"
            
            self.tree.insert("", "end", values=(
                corte.get("corte", ""),
                preco_formatado,
                corte.get("barbeiro", ""),
                corte.get("data_hora", "")
            ))
    
    def filtrar_cortes(self, event=None):
        """Filtra cortes conforme busca"""
        termo = self.entry_busca.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for corte in self.data_manager.get_cortes():
            if (termo in corte.get("corte", "").lower() or
                termo in corte.get("barbeiro", "").lower()):
                
                preco = corte.get("preco", 0)
                preco_formatado = Formatador.formatar_preco(preco) if preco else "R$ 0,00"
                
                self.tree.insert("", "end", values=(
                    corte.get("corte", ""),
                    preco_formatado,
                    corte.get("barbeiro", ""),
                    corte.get("data_hora", "")
                ))
    
    def registrar_corte(self):
        """Abre janela de registro de corte"""
        CadastroCorteWindow(self.frame, self.callback_corte_salvo)
    
    def editar_corte(self):
        """Edita o corte selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um corte para editar!")
            return
        
        # Obter dados do corte selecionado
        item = selected[0]
        values = self.tree.item(item, 'values')
        tipo_corte = values[0] 
        data_hora = values[3] if len(values) > 3 else ""
        
        # Encontrar o corte completo na lista
        cortes = self.data_manager.get_cortes()
        for i, corte in enumerate(cortes):
            if (corte['corte'] == tipo_corte and 
                corte.get('data_hora', '') == data_hora):
                
                def callback_with_index(dados, index=i):
                    return self.callback_corte_editado(dados, index)
                
                CadastroCorteWindow(self.frame, callback_with_index, corte)
                break
    
    def excluir_corte(self):
        """Exclui o corte selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um corte para excluir!")
            return
        
        # Obter dados do corte selecionado
        item = selected[0]
        values = self.tree.item(item, 'values')
        tipo_corte = values[0]
        data_hora = values[3] if len(values) > 3 else ""
        
        # Confirmar exclusão
        resposta = messagebox.askyesno("Confirmar Exclusão", 
                                      f"Tem certeza que deseja excluir este corte?\n\n"
                                      f"Tipo: {tipo_corte}\n"
                                      f"Data/Hora: {data_hora}\n\n"
                                      "Esta ação não pode ser desfeita!")
        if not resposta:
            return
        
        # Encontrar e remover corte
        cortes = self.data_manager.get_cortes()
        for i, corte in enumerate(cortes):
            if (corte['corte'] == tipo_corte and 
                corte.get('data_hora', '') == data_hora):
                self.data_manager.delete_corte(i)
                break
        
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Corte excluído com sucesso!")
    
    def callback_corte_salvo(self, corte_data):
        """Callback executado quando corte é salvo"""
        self.data_manager.add_corte(corte_data)
        self.atualizar_lista()
        
        if self.callback:
            self.callback()
    
    def callback_corte_editado(self, corte_data, index):
        """Callback executado quando corte é editado"""
        self.data_manager.update_corte(index, corte_data)
        self.atualizar_lista()
        
        if self.callback:
            self.callback()
