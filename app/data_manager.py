"""
Módulo de gerenciamento de dados
"""
import json
import os
from tkinter import messagebox


class DataManager:
    def __init__(self):
        self.clientes_file = "data/clientes.json"
        self.cortes_file = "data/cortes.json"
        self.agendamentos_file = "data/agendamentos.json"
        
        self.clientes = self.carregar_dados(self.clientes_file, [])
        self.cortes = self.carregar_dados(self.cortes_file, [])
        self.agendamentos = self.carregar_dados(self.agendamentos_file, [])
    
    def carregar_dados(self, arquivo, padrao):
        """Carrega dados de um arquivo JSON"""
        try:
            if os.path.exists(arquivo):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return padrao
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar {arquivo}: {str(e)}")
            return padrao
    
    def salvar_dados(self, dados, arquivo):
        """Salva dados em arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar {arquivo}: {str(e)}")
    
    # CLIENTES
    def get_clientes(self):
        return self.clientes
    
    def add_cliente(self, cliente_data):
        self.clientes.append(cliente_data)
        self.salvar_dados(self.clientes, self.clientes_file)
    
    def update_cliente(self, index, cliente_data):
        if 0 <= index < len(self.clientes):
            self.clientes[index] = cliente_data
            self.salvar_dados(self.clientes, self.clientes_file)
    
    def delete_cliente(self, index):
        if 0 <= index < len(self.clientes):
            del self.clientes[index]
            self.salvar_dados(self.clientes, self.clientes_file)
    
    # CORTES
    def get_cortes(self):
        return self.cortes
    
    def add_corte(self, corte_data):
        self.cortes.append(corte_data)
        self.salvar_dados(self.cortes, self.cortes_file)
    
    def update_corte(self, index, corte_data):
        if 0 <= index < len(self.cortes):
            self.cortes[index] = corte_data
            self.salvar_dados(self.cortes, self.cortes_file)
    
    def delete_corte(self, index):
        if 0 <= index < len(self.cortes):
            del self.cortes[index]
            self.salvar_dados(self.cortes, self.cortes_file)
    
    # AGENDAMENTOS
    def get_agendamentos(self):
        return self.agendamentos
    
    def add_agendamento(self, agendamento_data):
        self.agendamentos.append(agendamento_data)
        self.salvar_dados(self.agendamentos, self.agendamentos_file)
    
    def update_agendamento(self, index, agendamento_data):
        if 0 <= index < len(self.agendamentos):
            self.agendamentos[index] = agendamento_data
            self.salvar_dados(self.agendamentos, self.agendamentos_file)
    
    def delete_agendamento(self, index):
        if 0 <= index < len(self.agendamentos):
            del self.agendamentos[index]
            self.salvar_dados(self.agendamentos, self.agendamentos_file)
