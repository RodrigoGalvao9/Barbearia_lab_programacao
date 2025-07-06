"""
Interface gráfica para cadastro de clientes
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.models import Cliente
from utils.validations import Validador, Formatador


class CadastroClienteWindow:
    def __init__(self, parent, callback_sucesso=None, cliente_editando=None):
        self.parent = parent
        self.callback_sucesso = callback_sucesso
        self.cliente_editando = cliente_editando
        
        self.janela = tk.Toplevel(parent)
        self.janela.title("Cadastrar Cliente" if not cliente_editando else "Editar Cliente")
        self.janela.geometry("500x600")
        self.janela.configure(bg="#ecf0f1")
        self.janela.resizable(False, False)
        
        # Centralizar janela
        self.janela.transient(parent)
        self.janela.grab_set()
        
        self.criar_interface()
        
        # Se está editando, preencher campos
        if cliente_editando:
            self.preencher_campos()
    
    def criar_interface(self):
        """Cria a interface de cadastro"""
        # Título
        titulo_frame = tk.Frame(self.janela, bg="#34495e", height=60)
        titulo_frame.pack(fill="x")
        titulo_frame.pack_propagate(False)
        
        titulo_text = "CADASTRAR CLIENTE" if not self.cliente_editando else "EDITAR CLIENTE"
        tk.Label(titulo_frame, text=titulo_text, 
                font=("Arial", 16, "bold"), bg="#34495e", fg="white").pack(pady=15)
        
        # Frame principal para campos
        main_frame = tk.Frame(self.janela, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Nome (obrigatório)
        self.criar_campo(main_frame, "Nome*:", "entry_nome", obrigatorio=True)
        
        # Telefone (obrigatório)
        self.criar_campo(main_frame, "Telefone*:", "entry_telefone", obrigatorio=True)
        
        # Email (opcional)
        self.criar_campo(main_frame, "Email:", "entry_email")
        
        # Data de nascimento (opcional)
        self.criar_campo(main_frame, "Data de Nascimento (DD/MM/AAAA):", "entry_data_nascimento")
        
        # Endereço (opcional)
        self.criar_campo_texto(main_frame, "Endereço:", "text_endereco")
        
        # Frame para botões
        btn_frame = tk.Frame(main_frame, bg="#ecf0f1")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="Salvar", command=self.salvar_cliente,
                 bg="#27ae60", fg="white", font=("Arial", 12), width=12).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Cancelar", command=self.janela.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 12), width=12).pack(side="left", padx=10)
        
        # Focar no primeiro campo
        self.entry_nome.focus()
        
        # Labels de ajuda
        help_frame = tk.Frame(main_frame, bg="#ecf0f1")
        help_frame.pack(fill="x", pady=10)
        
        tk.Label(help_frame, text="* Campos obrigatórios", 
                font=("Arial", 9), bg="#ecf0f1", fg="#7f8c8d").pack(anchor="w")
        
        tk.Label(help_frame, text="Telefone: (11) 99999-9999 ou 11999999999", 
                font=("Arial", 9), bg="#ecf0f1", fg="#7f8c8d").pack(anchor="w")
    
    def criar_campo(self, parent, label_text, attr_name, obrigatorio=False):
        """Cria um campo de entrada simples"""
        frame = tk.Frame(parent, bg="#ecf0f1")
        frame.pack(fill="x", pady=8)
        
        cor_label = "#2c3e50" if obrigatorio else "#34495e"
        tk.Label(frame, text=label_text, font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg=cor_label).pack(anchor="w")
        
        entry = tk.Entry(frame, font=("Arial", 11), width=50, relief="solid", bd=1)
        entry.pack(pady=2)
        
        setattr(self, attr_name, entry)
    
    def criar_campo_texto(self, parent, label_text, attr_name):
        """Cria um campo de texto multilinha"""
        frame = tk.Frame(parent, bg="#ecf0f1")
        frame.pack(fill="x", pady=8)
        
        tk.Label(frame, text=label_text, font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#34495e").pack(anchor="w")
        
        text_widget = tk.Text(frame, font=("Arial", 11), width=50, height=3, 
                             relief="solid", bd=1, wrap="word")
        text_widget.pack(pady=2)
        
        setattr(self, attr_name, text_widget)
    
    def preencher_campos(self):
        """Preenche os campos com dados do cliente em edição"""
        if not self.cliente_editando:
            return
            
        self.entry_nome.insert(0, self.cliente_editando.get("nome", ""))
        self.entry_telefone.insert(0, self.cliente_editando.get("telefone", ""))
        self.entry_email.insert(0, self.cliente_editando.get("email", ""))
        self.entry_data_nascimento.insert(0, self.cliente_editando.get("data_nascimento", ""))
        self.text_endereco.insert("1.0", self.cliente_editando.get("endereco", ""))
    
    def salvar_cliente(self):
        """Valida e salva o cliente"""
        # Coletar dados
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        data_nascimento = self.entry_data_nascimento.get().strip()
        endereco = self.text_endereco.get("1.0", "end-1c").strip()
        
        # Validações
        erros = []
        
        if not Validador.validar_nome(nome):
            erros.append("Nome deve ter pelo menos 2 caracteres")
        
        if not telefone:
            erros.append("Telefone é obrigatório")
        elif not Validador.validar_telefone(telefone):
            erros.append("Telefone inválido. Use formato (11) 99999-9999")
        
        if email and not Validador.validar_email(email):
            erros.append("Email inválido")
        
        if data_nascimento and not Validador.validar_data(data_nascimento):
            erros.append("Data de nascimento inválida. Use formato DD/MM/AAAA")
        
        if erros:
            messagebox.showerror("Erro de Validação", "\n".join(erros))
            return
        
        # Criar objeto cliente
        cliente_data = {
            "nome": nome,
            "telefone": Formatador.formatar_telefone(telefone),
            "email": email,
            "endereco": endereco,
            "data_nascimento": data_nascimento
        }
        
        # Chamar callback de sucesso
        if self.callback_sucesso:
            self.callback_sucesso(cliente_data)
        
        messagebox.showinfo("Sucesso", 
                           "Cliente cadastrado com sucesso!" if not self.cliente_editando 
                           else "Cliente atualizado com sucesso!")
        self.janela.destroy()


class CadastroCorteWindow:
    def __init__(self, parent, clientes, callback_sucesso=None):
        self.parent = parent
        self.clientes = clientes
        self.callback_sucesso = callback_sucesso
        
        if not clientes:
            messagebox.showwarning("Aviso", "Cadastre clientes primeiro!")
            return
        
        self.janela = tk.Toplevel(parent)
        self.janela.title("Registrar Corte")
        self.janela.geometry("500x550")
        self.janela.configure(bg="#ecf0f1")
        self.janela.resizable(False, False)
        
        self.janela.transient(parent)
        self.janela.grab_set()
        
        self.criar_interface()
    
    def criar_interface(self):
        """Cria a interface de registro de corte"""
        from utils.validations import TIPOS_CORTE, BARBEIROS
        
        # Título
        titulo_frame = tk.Frame(self.janela, bg="#27ae60", height=60)
        titulo_frame.pack(fill="x")
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="REGISTRAR CORTE", 
                font=("Arial", 16, "bold"), bg="#27ae60", fg="white").pack(pady=15)
        
        # Frame principal
        main_frame = tk.Frame(self.janela, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cliente
        tk.Label(main_frame, text="Cliente*:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", pady=(0,5))
        
        self.combo_cliente = ttk.Combobox(main_frame, font=("Arial", 11), width=47, state="readonly")
        self.combo_cliente['values'] = [cliente['nome'] for cliente in self.clientes]
        self.combo_cliente.pack(pady=(0,15))
        
        # Tipo de corte
        tk.Label(main_frame, text="Tipo de Corte*:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", pady=(0,5))
        
        self.combo_tipo = ttk.Combobox(main_frame, font=("Arial", 11), width=47, state="readonly")
        self.combo_tipo['values'] = TIPOS_CORTE
        self.combo_tipo.pack(pady=(0,15))
        
        # Barbeiro
        tk.Label(main_frame, text="Barbeiro:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(0,5))
        
        self.combo_barbeiro = ttk.Combobox(main_frame, font=("Arial", 11), width=47, state="readonly")
        self.combo_barbeiro['values'] = BARBEIROS
        self.combo_barbeiro.pack(pady=(0,15))
        
        # Preço
        tk.Label(main_frame, text="Preço (R$):", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(0,5))
        
        self.entry_preco = tk.Entry(main_frame, font=("Arial", 11), width=50, relief="solid", bd=1)
        self.entry_preco.pack(pady=(0,15))
        
        # Observações
        tk.Label(main_frame, text="Observações:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(0,5))
        
        self.text_obs = tk.Text(main_frame, font=("Arial", 11), width=50, height=4, 
                               relief="solid", bd=1, wrap="word")
        self.text_obs.pack(pady=(0,20))
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg="#ecf0f1")
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Salvar", command=self.salvar_corte,
                 bg="#27ae60", fg="white", font=("Arial", 12), width=12).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Cancelar", command=self.janela.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 12), width=12).pack(side="left", padx=10)
        
        # Labels de ajuda
        tk.Label(main_frame, text="* Campos obrigatórios", 
                font=("Arial", 9), bg="#ecf0f1", fg="#7f8c8d").pack(anchor="w", pady=(10,0))
    
    def salvar_corte(self):
        """Valida e salva o corte"""
        from datetime import datetime
        
        cliente = self.combo_cliente.get()
        tipo_corte = self.combo_tipo.get()
        barbeiro = self.combo_barbeiro.get()
        preco = self.entry_preco.get().strip()
        observacoes = self.text_obs.get("1.0", "end-1c").strip()
        
        erros = []
        
        if not cliente:
            erros.append("Selecione um cliente")
        
        if not tipo_corte:
            erros.append("Selecione o tipo de corte")
        
        if preco and not Validador.validar_preco(preco):
            erros.append("Preço inválido")
        
        if erros:
            messagebox.showerror("Erro de Validação", "\n".join(erros))
            return
        
        # Converter preço
        preco_float = 0.0
        if preco:
            preco_float = float(preco.replace(',', '.'))
        
        agora = datetime.now()
        corte_data = {
            "cliente": cliente,
            "corte": tipo_corte,
            "preco": preco_float,
            "barbeiro": barbeiro,
            "data_hora": agora.strftime("%d/%m/%Y %H:%M"),
            "observacoes": observacoes
        }
        
        if self.callback_sucesso:
            self.callback_sucesso(corte_data)
        
        messagebox.showinfo("Sucesso", "Corte registrado com sucesso!")
        self.janela.destroy()


class CadastroAgendamentoWindow:
    def __init__(self, parent, clientes, callback_sucesso=None):
        self.parent = parent
        self.clientes = clientes
        self.callback_sucesso = callback_sucesso
        
        if not clientes:
            messagebox.showwarning("Aviso", "Cadastre clientes primeiro!")
            return
        
        self.janela = tk.Toplevel(parent)
        self.janela.title("Novo Agendamento")
        self.janela.geometry("500x600")
        self.janela.configure(bg="#ecf0f1")
        self.janela.resizable(False, False)
        
        self.janela.transient(parent)
        self.janela.grab_set()
        
        self.criar_interface()
    
    def criar_interface(self):
        """Cria a interface de agendamento"""
        from utils.validations import TIPOS_CORTE, BARBEIROS, STATUS_AGENDAMENTO
        
        # Título
        titulo_frame = tk.Frame(self.janela, bg="#f39c12", height=60)
        titulo_frame.pack(fill="x")
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="NOVO AGENDAMENTO", 
                font=("Arial", 16, "bold"), bg="#f39c12", fg="white").pack(pady=15)
        
        # Frame principal
        main_frame = tk.Frame(self.janela, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cliente
        tk.Label(main_frame, text="Cliente*:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", pady=(0,5))
        
        self.combo_cliente = ttk.Combobox(main_frame, font=("Arial", 11), width=47, state="readonly")
        self.combo_cliente['values'] = [cliente['nome'] for cliente in self.clientes]
        self.combo_cliente.pack(pady=(0,15))
        
        # Data
        tk.Label(main_frame, text="Data (DD/MM/AAAA)*:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", pady=(0,5))
        
        self.entry_data = tk.Entry(main_frame, font=("Arial", 11), width=50, relief="solid", bd=1)
        self.entry_data.pack(pady=(0,15))
        
        # Hora
        tk.Label(main_frame, text="Hora (HH:MM)*:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", pady=(0,5))
        
        self.entry_hora = tk.Entry(main_frame, font=("Arial", 11), width=50, relief="solid", bd=1)
        self.entry_hora.pack(pady=(0,15))
        
        # Serviço
        tk.Label(main_frame, text="Serviço:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(0,5))
        
        self.combo_servico = ttk.Combobox(main_frame, font=("Arial", 11), width=47, state="readonly")
        self.combo_servico['values'] = TIPOS_CORTE
        self.combo_servico.pack(pady=(0,15))
        
        # Barbeiro
        tk.Label(main_frame, text="Barbeiro:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(0,5))
        
        self.combo_barbeiro = ttk.Combobox(main_frame, font=("Arial", 11), width=47, state="readonly")
        self.combo_barbeiro['values'] = BARBEIROS
        self.combo_barbeiro.pack(pady=(0,15))
        
        # Status
        tk.Label(main_frame, text="Status:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(0,5))
        
        self.combo_status = ttk.Combobox(main_frame, font=("Arial", 11), width=47, state="readonly")
        self.combo_status['values'] = STATUS_AGENDAMENTO
        self.combo_status.set("Agendado")  # Valor padrão
        self.combo_status.pack(pady=(0,15))
        
        # Observações
        tk.Label(main_frame, text="Observações:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(0,5))
        
        self.text_obs = tk.Text(main_frame, font=("Arial", 11), width=50, height=3, 
                               relief="solid", bd=1, wrap="word")
        self.text_obs.pack(pady=(0,20))
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg="#ecf0f1")
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Salvar", command=self.salvar_agendamento,
                 bg="#f39c12", fg="white", font=("Arial", 12), width=12).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Cancelar", command=self.janela.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 12), width=12).pack(side="left", padx=10)
        
        # Labels de ajuda
        tk.Label(main_frame, text="* Campos obrigatórios", 
                font=("Arial", 9), bg="#ecf0f1", fg="#7f8c8d").pack(anchor="w", pady=(10,0))
    
    def salvar_agendamento(self):
        """Valida e salva o agendamento"""
        cliente = self.combo_cliente.get()
        data = self.entry_data.get().strip()
        hora = self.entry_hora.get().strip()
        servico = self.combo_servico.get()
        barbeiro = self.combo_barbeiro.get()
        status = self.combo_status.get()
        observacoes = self.text_obs.get("1.0", "end-1c").strip()
        
        erros = []
        
        if not cliente:
            erros.append("Selecione um cliente")
        
        if not data:
            erros.append("Data é obrigatória")
        elif not Validador.validar_data(data):
            erros.append("Data inválida. Use formato DD/MM/AAAA")
        
        if not hora:
            erros.append("Hora é obrigatória")
        elif not Validador.validar_hora(hora):
            erros.append("Hora inválida. Use formato HH:MM")
        
        if erros:
            messagebox.showerror("Erro de Validação", "\n".join(erros))
            return
        
        agendamento_data = {
            "cliente": cliente,
            "data": data,
            "hora": hora,
            "servico": servico,
            "barbeiro": barbeiro,
            "status": status,
            "observacoes": observacoes
        }
        
        if self.callback_sucesso:
            self.callback_sucesso(agendamento_data)
        
        messagebox.showinfo("Sucesso", "Agendamento criado com sucesso!")
        self.janela.destroy()
