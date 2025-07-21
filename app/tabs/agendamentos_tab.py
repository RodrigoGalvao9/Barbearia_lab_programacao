"""
Aba de gerenciamento de agendamentos
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.cadastros import CadastroAgendamentoWindow


class AgendamentosTab:
    def __init__(self, notebook, data_manager):
        self.notebook = notebook
        self.data_manager = data_manager
        self.callback = None
        
        # Criar frame da aba
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📅 Agendamentos")
        
        self.criar_interface()
        self.atualizar_lista()
    
    def set_callback(self, callback):
        """Define callback para quando dados são alterados"""
        self.callback = callback
    
    def criar_interface(self):
        """Cria a interface da aba de agendamentos"""
        # Frame para botões
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        tk.Button(btn_frame, text="➕ Novo Agendamento", command=self.novo_agendamento,
                 bg="#f39c12", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✏️ Editar", command=self.editar_agendamento,
                 bg="#3498db", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✅ Confirmar", command=self.confirmar_agendamento,
                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="⏳ Em Andamento", command=self.marcar_em_andamento,
                 bg="#9b59b6", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✔️ Realizado", command=self.marcar_realizado,
                 bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="❌ Cancelar", command=self.cancelar_agendamento,
                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🗑️ Remover", command=self.remover_agendamento,
                 bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista,
                 bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(side="right", padx=5)
        
        # Treeview
        columns = ("Cliente", "Data", "Hora", "Serviço", "Barbeiro", "Status")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=18)
        
        # Configurar colunas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)
    
    def atualizar_lista(self):
        """Atualiza a lista de agendamentos"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for agendamento in self.data_manager.get_agendamentos():
            self.tree.insert("", "end", values=(
                agendamento.get("cliente", ""),
                agendamento.get("data", ""),
                agendamento.get("hora", ""),
                agendamento.get("servico", ""),
                agendamento.get("barbeiro", ""),
                agendamento.get("status", "")
            ))
    
    def novo_agendamento(self):
        """Abre janela de novo agendamento"""
        clientes = self.data_manager.get_clientes()
        if not clientes:
            messagebox.showwarning("Aviso", "Cadastre clientes primeiro!")
            return
        
        CadastroAgendamentoWindow(self.frame, clientes, self.callback_agendamento_salvo)
    
    def editar_agendamento(self):
        """Edita o agendamento selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento para editar!")
            return
        
        item = selected[0]
        values = self.tree.item(item, 'values')
        cliente_nome = values[0]
        data_agendamento = values[1]
        hora_agendamento = values[2]
        
        # Encontrar agendamento
        agendamentos = self.data_manager.get_agendamentos()
        for i, agendamento in enumerate(agendamentos):
            if (agendamento['cliente'] == cliente_nome and 
                agendamento['data'] == data_agendamento and 
                agendamento['hora'] == hora_agendamento):
                
                clientes = self.data_manager.get_clientes()
                CadastroAgendamentoWindow(self.frame, clientes, 
                                        lambda dados: self.callback_agendamento_editado(dados, i),
                                        agendamento)
                break
    
    def confirmar_agendamento(self):
        """Confirma o agendamento selecionado"""
        self.alterar_status_agendamento("Confirmado")
    
    def marcar_em_andamento(self):
        """Marca agendamento como em andamento"""
        self.alterar_status_agendamento("Em Andamento")
    
    def marcar_realizado(self):
        """Marca o agendamento como realizado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento!")
            return
        
        resposta = messagebox.askyesno("Marcar como Realizado", 
                                      "Marcar agendamento como realizado?\n\n"
                                      "Isso criará automaticamente um registro de corte.")
        if not resposta:
            return
        
        # Alterar status e criar corte
        item = selected[0]
        values = self.tree.item(item, 'values')
        
        # Criar corte automaticamente
        from datetime import datetime
        corte_data = {
            "corte": values[3],  # serviço
            "preco": 0.0,  # será preenchido depois
            "barbeiro": values[4],  # barbeiro
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "observacoes": f"Gerado automaticamente do agendamento de {values[1]} {values[2]}"
        }
        
        self.data_manager.add_corte(corte_data)
        self.alterar_status_agendamento("Realizado")
        messagebox.showinfo("Sucesso", "Agendamento marcado como realizado e corte registrado!")
    
    def cancelar_agendamento(self):
        """Cancela o agendamento selecionado"""
        self.alterar_status_agendamento("Cancelado")
    
    def remover_agendamento(self):
        """Remove agendamentos selecionados"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento para remover!")
            return
        
        resposta = messagebox.askyesno("Confirmar Remoção", 
                                      "Tem certeza que deseja remover este agendamento?\n\n"
                                      "Esta ação não pode ser desfeita!")
        if not resposta:
            return
        
        item = selected[0]
        values = self.tree.item(item, 'values')
        
        # Encontrar e remover agendamento
        agendamentos = self.data_manager.get_agendamentos()
        for i, agendamento in enumerate(agendamentos):
            if (agendamento['cliente'] == values[0] and 
                agendamento['data'] == values[1] and 
                agendamento['hora'] == values[2]):
                self.data_manager.delete_agendamento(i)
                break
        
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Agendamento removido!")
    
    def alterar_status_agendamento(self, novo_status):
        """Altera status do agendamento selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento!")
            return
        
        item = selected[0]
        values = self.tree.item(item, 'values')
        
        # Encontrar e alterar status
        agendamentos = self.data_manager.get_agendamentos()
        for i, agendamento in enumerate(agendamentos):
            if (agendamento['cliente'] == values[0] and 
                agendamento['data'] == values[1] and 
                agendamento['hora'] == values[2]):
                
                agendamento['status'] = novo_status
                self.data_manager.update_agendamento(i, agendamento)
                break
        
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Status alterado para: {novo_status}")
    
    def callback_agendamento_editado(self, agendamento_data, index):
        """Callback para agendamento editado"""
        self.data_manager.update_agendamento(index, agendamento_data)
        self.atualizar_lista()
        
        if self.callback:
            self.callback()
    
    def callback_agendamento_salvo(self, agendamento_data):
        """Callback executado quando agendamento é salvo"""
        self.data_manager.add_agendamento(agendamento_data)
        self.atualizar_lista()
        
        if self.callback:
            self.callback()
