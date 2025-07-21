"""
Aba de Relatórios e Estatísticas - Sistema de Barbearia
=======================================================

Este módulo implementa a aba de relatórios do sistema, fornecendo:
- Estatísticas resumidas em cards visuais
- Relatórios detalhados com informações específicas
- Interface responsiva e colorida
- Atualização automática dos dados

Funcionalidades principais:
- Cards de estatísticas principais (clientes, cortes, receita, agendamentos)
- Seção detalhada com análises aprofundadas
- Interface scrollável para grandes volumes de dados
- Cores organizadas por categoria de informação
- Centralização adequada dos elementos

Componentes:
- Cards superiores: Estatísticas gerais
- Seção detalhada: Análises específicas por categoria
- Botão de atualização: Refresh manual dos dados

Tecnologias utilizadas:
- Tkinter para interface gráfica
- Canvas com scrollbar para conteúdo extenso
- Sistema de cores categorizadas
- Layout responsivo com centralização
"""
import tkinter as tk
from tkinter import ttk


class RelatoriosTab:
    """
    Classe responsável pela aba de relatórios e estatísticas.
    
    Gerencia toda a apresentação de dados estatísticos do sistema:
    - Cards de resumo com números principais
    - Relatórios detalhados por categoria
    - Interface visual moderna e colorida
    - Atualização dinâmica dos dados
    
    Attributes:
        notebook (ttk.Notebook): Notebook pai das abas
        data_manager (DataManager): Gerenciador de dados do sistema
        frame (ttk.Frame): Frame principal da aba
        stats_frame (tk.Frame): Frame dos cards de estatísticas
        detalhes_frame (tk.Frame): Frame dos relatórios detalhados
    """
    
    def __init__(self, notebook, data_manager):
        """
        Inicializa a aba de relatórios.
        
        Args:
            notebook (ttk.Notebook): Notebook pai
            data_manager (DataManager): Gerenciador de dados
        """
        self.notebook = notebook
        self.data_manager = data_manager
        
        # Criar frame da aba e adicionar ao notebook
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📊 Relatórios")
        
        # Configurar interface e carregar dados iniciais
        self.criar_interface()
        self.atualizar_relatorios()
    
    def criar_interface(self):
        """
        Cria a interface gráfica da aba de relatórios.
        
        Componentes criados:
        - Título principal da seção
        - Frame para cards de estatísticas resumidas
        - Botão de atualização manual
        - Seção de relatórios detalhados com scroll
        - Canvas configurado para navegação vertical
        """
        # Título principal da aba
        titulo = tk.Label(self.frame, text="📊 Relatórios e Estatísticas", 
                         font=("Arial", 16, "bold"), bg="#ecf0f1")
        titulo.pack(pady=20)
        
        # Frame para os cards de estatísticas principais
        self.stats_frame = tk.Frame(self.frame, bg="#ecf0f1")
        self.stats_frame.pack(pady=20)
        
        # Botão de atualizar
        tk.Button(self.frame, text="🔄 Atualizar Relatórios", command=self.atualizar_relatorios,
                 bg="#3498db", fg="white", font=("Arial", 12, "bold"), cursor="hand2").pack(pady=10)
        
        # Seção de detalhes
        detalhes_label = tk.Label(self.frame, text="📋 Detalhes dos Relatórios", 
                                font=("Arial", 14, "bold"), bg="#ecf0f1")
        detalhes_label.pack(pady=(30, 10))
        
        # Frame scrollable para detalhes
        canvas_frame = tk.Frame(self.frame)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.detalhes_frame = tk.Frame(canvas, bg="#ecf0f1")
        
        self.detalhes_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.detalhes_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def criar_card_estatistica(self, parent, icone, titulo, valor, cor):
        """Cria um card de estatística"""
        card = tk.Frame(parent, bg=cor, relief="raised", bd=2)
        card.pack(side="left", padx=10, pady=10, ipadx=20, ipady=15)
        
        # Ícone
        tk.Label(card, text=icone, font=("Arial", 24), bg=cor, fg="white").pack()
        
        # Valor
        tk.Label(card, text=str(valor), font=("Arial", 20, "bold"), bg=cor, fg="white").pack()
        
        # Título
        tk.Label(card, text=titulo, font=("Arial", 10), bg=cor, fg="white").pack()
    
    def atualizar_relatorios(self):
        """Atualiza os relatórios"""
        # Limpar cards existentes
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Limpar detalhes existentes
        for widget in self.detalhes_frame.winfo_children():
            widget.destroy()
        
        # Dados
        clientes = self.data_manager.get_clientes()
        cortes = self.data_manager.get_cortes()
        agendamentos = self.data_manager.get_agendamentos()
        
        # Calcular receita total
        receita_total = 0
        precos = []
        for corte in cortes:
            try:
                preco_str = str(corte.get('preco', '0')).replace(',', '.')
                preco = float(preco_str)
                receita_total += preco
                if preco > 0:
                    precos.append(preco)
            except (ValueError, AttributeError):
                continue
        
        # Criar cards de estatísticas
        self.criar_card_estatistica(self.stats_frame, "👥", "Total de Clientes", len(clientes), "#3498db")
        self.criar_card_estatistica(self.stats_frame, "✂️", "Cortes Realizados", len(cortes), "#27ae60")
        self.criar_card_estatistica(self.stats_frame, "📅", "Agendamentos", len(agendamentos), "#f39c12")
        self.criar_card_estatistica(self.stats_frame, "💰", f"Receita Total", f"R$ {receita_total:.2f}", "#e74c3c")
        
        # Criar seção de detalhes
        self.criar_detalhes_clientes(clientes)
        self.criar_detalhes_cortes(cortes, precos, receita_total)
        self.criar_detalhes_agendamentos(agendamentos)
    
    def criar_detalhes_clientes(self, clientes):
        """Cria detalhes dos clientes"""
        frame = tk.LabelFrame(self.detalhes_frame, text="👥 Detalhes dos Clientes", 
                             font=("Arial", 12, "bold"), bg="#ecf0f1", relief="solid", bd=1)
        frame.pack(fill="x", padx=20, pady=10)
        
        # Container centralizado
        container = tk.Frame(frame, bg="#ecf0f1")
        container.pack(expand=True, fill="x", padx=20, pady=15)
        
        if clientes:
            # Card principal com largura centralizada
            main_card = tk.Frame(container, bg="#3498db", relief="flat", bd=2)
            main_card.pack(anchor="center", pady=(0, 15))
            
            tk.Label(main_card, text=f"📊 {len(clientes)} CLIENTES CADASTRADOS", 
                    font=("Arial", 12, "bold"), bg="#3498db", fg="white").pack(padx=30, pady=10)
            
            # Seção de clientes recentes
            recent_card = tk.Frame(container, bg="white", relief="solid", bd=1)
            recent_card.pack(anchor="center", fill="x", pady=5)
            
            tk.Label(recent_card, text="🆕 Clientes Mais Recentes", 
                    font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(pady=(10, 5))
            
            # Lista de clientes
            for i, cliente in enumerate(clientes[-5:], 1):
                cliente_info = f"{i}. {cliente.get('nome', 'N/A')} - {cliente.get('telefone', 'N/A')}"
                tk.Label(recent_card, text=cliente_info, font=("Arial", 10), 
                        bg="white", fg="#34495e").pack(pady=2)
            
            tk.Frame(recent_card, bg="white", height=10).pack()  # Espaçamento
        else:
            # Card de vazio
            empty_card = tk.Frame(container, bg="#e74c3c", relief="flat", bd=2)
            empty_card.pack(anchor="center")
            
            tk.Label(empty_card, text="⚠️ NENHUM CLIENTE CADASTRADO", 
                    font=("Arial", 12, "bold"), bg="#e74c3c", fg="white").pack(padx=30, pady=15)
    
    def criar_detalhes_cortes(self, cortes, precos, receita_total):
        """Cria detalhes dos cortes"""
        frame = tk.LabelFrame(self.detalhes_frame, text="✂️ Detalhes dos Cortes", 
                             font=("Arial", 12, "bold"), bg="#ecf0f1", relief="solid", bd=1)
        frame.pack(fill="x", padx=20, pady=10)
        
        # Container centralizado
        container = tk.Frame(frame, bg="#ecf0f1")
        container.pack(expand=True, fill="x", padx=20, pady=15)
        
        if cortes:
            # Card principal de receita
            main_card = tk.Frame(container, bg="#27ae60", relief="flat", bd=2)
            main_card.pack(anchor="center", pady=(0, 15))
            
            tk.Label(main_card, text=f"💰 R$ {receita_total:.2f} EM {len(cortes)} CORTES", 
                    font=("Arial", 12, "bold"), bg="#27ae60", fg="white").pack(padx=30, pady=10)
            
            # Estatísticas financeiras
            if precos:
                media_corte = sum(precos) / len(precos)
                maior_valor = max(precos)
                menor_valor = min(precos)
                
                # Frame para as 3 estatísticas
                stats_container = tk.Frame(container, bg="#ecf0f1")
                stats_container.pack(anchor="center", pady=(0, 15))
                
                # Cards lado a lado
                col1 = tk.Frame(stats_container, bg="#3498db", relief="solid", bd=1)
                col1.pack(side="left", padx=5)
                tk.Label(col1, text="📊 MÉDIA\nR$ {:.2f}".format(media_corte), 
                        font=("Arial", 10, "bold"), bg="#3498db", fg="white", 
                        justify="center").pack(padx=15, pady=10)
                
                col2 = tk.Frame(stats_container, bg="#e67e22", relief="solid", bd=1)
                col2.pack(side="left", padx=5)
                tk.Label(col2, text="📈 MAIOR\nR$ {:.2f}".format(maior_valor), 
                        font=("Arial", 10, "bold"), bg="#e67e22", fg="white",
                        justify="center").pack(padx=15, pady=10)
                
                col3 = tk.Frame(stats_container, bg="#9b59b6", relief="solid", bd=1)
                col3.pack(side="left", padx=5)
                tk.Label(col3, text="📉 MENOR\nR$ {:.2f}".format(menor_valor), 
                        font=("Arial", 10, "bold"), bg="#9b59b6", fg="white",
                        justify="center").pack(padx=15, pady=10)
            
            # Tipos de corte mais populares
            tipos_card = tk.Frame(container, bg="white", relief="solid", bd=1)
            tipos_card.pack(anchor="center", fill="x", pady=10)
            
            tk.Label(tipos_card, text="🏆 Tipos de Corte Mais Populares", 
                    font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(pady=(10, 5))
            
            # Contar e mostrar tipos
            tipos_corte = {}
            for corte in cortes:
                tipo = corte.get('corte', 'Não especificado')
                tipos_corte[tipo] = tipos_corte.get(tipo, 0) + 1
            
            for i, (tipo, count) in enumerate(sorted(tipos_corte.items(), key=lambda x: x[1], reverse=True)[:3], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                tk.Label(tipos_card, text=f"{medal} {tipo}: {count} vezes", 
                        font=("Arial", 10), bg="white", fg="#34495e").pack(pady=2)
            
            tk.Frame(tipos_card, bg="white", height=10).pack()  # Espaçamento
        else:
            # Card de vazio
            empty_card = tk.Frame(container, bg="#e74c3c", relief="flat", bd=2)
            empty_card.pack(anchor="center")
            
            tk.Label(empty_card, text="⚠️ NENHUM CORTE REGISTRADO", 
                    font=("Arial", 12, "bold"), bg="#e74c3c", fg="white").pack(padx=30, pady=15)
    
    def criar_detalhes_agendamentos(self, agendamentos):
        """Cria detalhes dos agendamentos"""
        frame = tk.LabelFrame(self.detalhes_frame, text="📅 Detalhes dos Agendamentos", 
                             font=("Arial", 12, "bold"), bg="#ecf0f1", relief="solid", bd=1)
        frame.pack(fill="x", padx=20, pady=10)
        
        # Container centralizado
        container = tk.Frame(frame, bg="#ecf0f1")
        container.pack(expand=True, fill="x", padx=20, pady=15)
        
        if agendamentos:
            # Card principal
            main_card = tk.Frame(container, bg="#f39c12", relief="flat", bd=2)
            main_card.pack(anchor="center", pady=(0, 15))
            
            tk.Label(main_card, text=f"📋 {len(agendamentos)} AGENDAMENTOS REGISTRADOS", 
                    font=("Arial", 12, "bold"), bg="#f39c12", fg="white").pack(padx=30, pady=10)
            
            # Status dos agendamentos
            status_count = {}
            for agendamento in agendamentos:
                status = agendamento.get('status', 'Não especificado')
                status_count[status] = status_count.get(status, 0) + 1
            
            # Cards de status
            if status_count:
                tk.Label(container, text="📊 Status dos Agendamentos", 
                        font=("Arial", 11, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=(0, 10))
                
                colors = {"Agendado": "#3498db", "Confirmado": "#27ae60", 
                         "Em Andamento": "#f39c12", "Realizado": "#2ecc71", "Cancelado": "#e74c3c"}
                
                # Container para os cards de status
                status_container = tk.Frame(container, bg="#ecf0f1")
                status_container.pack(anchor="center", pady=(0, 15))
                
                for status, count in status_count.items():
                    color = colors.get(status, "#95a5a6")
                    status_card = tk.Frame(status_container, bg=color, relief="solid", bd=1)
                    status_card.pack(side="left", padx=5)
                    
                    tk.Label(status_card, text=f"{status}\n{count}", 
                            font=("Arial", 9, "bold"), bg=color, fg="white",
                            justify="center").pack(padx=12, pady=8)
            
            # Próximos agendamentos
            proximos_card = tk.Frame(container, bg="white", relief="solid", bd=1)
            proximos_card.pack(anchor="center", fill="x")
            
            tk.Label(proximos_card, text="⏰ Próximos Agendamentos", 
                    font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(pady=(10, 5))
            
            # Lista de agendamentos
            for i, agendamento in enumerate(agendamentos[:5], 1):
                cliente = agendamento.get('cliente', 'N/A')
                data = agendamento.get('data', 'N/A')
                hora = agendamento.get('hora', 'N/A')
                status = agendamento.get('status', 'N/A')
                
                status_emoji = {"Agendado": "📅", "Confirmado": "✅", "Em Andamento": "⚡", 
                               "Realizado": "✨", "Cancelado": "❌"}.get(status, "❓")
                
                agend_info = f"{i}. {status_emoji} {cliente} - {data} às {hora} ({status})"
                tk.Label(proximos_card, text=agend_info, font=("Arial", 10), 
                        bg="white", fg="#34495e").pack(pady=2)
            
            tk.Frame(proximos_card, bg="white", height=10).pack()  # Espaçamento
        else:
            # Card de vazio
            empty_card = tk.Frame(container, bg="#e74c3c", relief="flat", bd=2)
            empty_card.pack(anchor="center")
            
            tk.Label(empty_card, text="⚠️ NENHUM AGENDAMENTO REGISTRADO", 
                    font=("Arial", 12, "bold"), bg="#e74c3c", fg="white").pack(padx=30, pady=15)
