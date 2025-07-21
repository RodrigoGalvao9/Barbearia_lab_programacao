"""
=================================================
SISTEMA DE BARBEARIA v2.0 - MODULARIZADO
=================================================

Sistema completo de gerenciamento para barbearias com:
- Cadastro de clientes com validações
- Registro de cortes (sem campo barbeiro desnecessário)
- Agendamentos com controle de status avançado
- Relatórios estatísticos visuais e detalhados
- Sistema de login com registro de novos usuários

Arquitetura Modular:
- app/main_app.py: Aplicação principal
- app/login.py: Gerenciamento de login/registro
- app/main_window.py: Janela principal com abas
- app/data_manager.py: Gerenciamento de dados
- app/tabs/: Módulos individuais para cada funcionalidade
- models/: Modelos de dados (Cliente, Corte, Agendamento)
- gui/: Interfaces de cadastro
- utils/: Utilitários e validações

Tecnologias:
- Python 3.x
- Tkinter para interface gráfica
- JSON para persistência de dados
- Arquitetura MVC modular

=================================================
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Garantir que estamos no diretório correto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """
    Função principal que inicializa o sistema de barbearia modularizado.
    
    Responsabilidades:
    - Configura o ambiente de execução
    - Importa módulos necessários
    - Cria a janela principal do Tkinter
    - Inicializa a aplicação BarbeariaApp
    - Inicia o loop principal da interface gráfica
    - Trata erros de importação e execução
    
    Tratamento de Erros:
    - ImportError: Quando módulos não são encontrados
    - Exception: Erros gerais de inicialização
    """
    try:
        print("Iniciando Sistema de Barbearia v2.0 - Modularizado...")
        
        # Importar e executar o sistema principal modular
        from app.main_app import BarbeariaApp
        
        # Criar janela principal do Tkinter
        root = tk.Tk()
        
        # Inicializar aplicação principal
        app = BarbeariaApp(root)
        
        # Iniciar loop principal da interface gráfica
        root.mainloop()
        
    except ImportError as e:
        # Erro quando módulos não são encontrados
        messagebox.showerror(
            "Erro de Importação", 
            f"Erro ao carregar módulos:\n{e}\n\nVerifique se todos os arquivos estão presentes."
        )
    except Exception as e:
        # Erro geral de inicialização
        messagebox.showerror(
            "Erro", 
            f"Erro ao inicializar sistema:\n{e}"
        )

if __name__ == "__main__":
    # Ponto de entrada do programa
    # Executa apenas quando o arquivo é rodado diretamente
    main()
