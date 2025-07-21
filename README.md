
# 🪒 Sistema de Barbearia v2.0 - Modularizado

Sistema completo de gerenciamento para barbearias desenvolvido em Python com interface gráfica Tkinter.

## 📋 Funcionalidades Principais

### 🔐 **Sistema de Autenticação**
- Login de usuários existentes
- Registro de novos usuários com validações
- Persistência segura de credenciais

### 👥 **Gestão de Clientes**
- Cadastro completo com dados pessoais e contato
- Validação de telefone, email e dados obrigatórios
- Edição e remoção de clientes
- Busca e filtros em tempo real

### ✂️ **Registro de Cortes** 
- Cadastro simplificado: tipo, preço, observações
- Histórico completo de serviços
- Edição de preços e detalhes
- Cálculo automático de receitas

### 📅 **Sistema de Agendamentos**
- Agendamento completo com cliente, data, hora, serviço
- **Controle de status**: Agendado → Confirmado → Em Andamento → Realizado
- Cancelamento e edição de agendamentos
- Visualização organizada por status

### 📊 **Relatórios Detalhados e Visuais**
- **Cards coloridos** com estatísticas principais
- **Seção detalhada** com análises específicas:
  - � Clientes: Total e lista dos mais recentes
  - ✂️ Cortes: Receita, médias, maiores/menores valores, tipos populares
  - � Agendamentos: Status com cores, próximos agendamentos
- Interface **centralizada e profissional**
- Atualização em tempo real

## 📁 Estrutura Modular do Projeto

```
Barbearia_lab_programacao/
├── main.py                     # Ponto de entrada principal
├── app/                        # Módulos da aplicação
│   ├── main_app.py            # Aplicação principal
│   ├── login.py               # Sistema de login/registro
│   ├── main_window.py         # Janela principal com abas
│   ├── data_manager.py        # Gerenciamento de dados
│   └── tabs/                  # Abas especializadas
│       ├── clientes_tab.py    # Aba de clientes
│       ├── cortes_tab.py      # Aba de cortes (sem barbeiro)
│       ├── agendamentos_tab.py # Aba de agendamentos
│       └── relatorios_tab.py  # Aba de relatórios visuais
├── models/                     # Modelos de dados
│   ├── __init__.py
│   └── models.py              # Classes Cliente, Corte, Agendamento
├── gui/                        # Interfaces de cadastro
│   ├── __init__.py
│   └── cadastros.py           # Janelas de formulários
├── utils/                      # Utilitários do sistema
│   ├── __init__.py
│   ├── validations.py         # Validações e constantes
│   ├── file_manager.py        # Gerenciamento de arquivos
│   └── helpers.py             # Funções auxiliares
└── data/                       # Dados persistidos (JSON)
    ├── usuarios.json          # Usuários do sistema
    ├── clientes.json          # Dados de clientes
    ├── cortes.json           # Histórico de cortes
    └── agendamentos.json     # Agendamentos
```

## � Requisitos do Sistema

- **Python 3.6+** instalado
- **Bibliotecas**: tkinter (já incluída no Python)

## 🎮 Como Executar

1. Clone ou baixe o projeto
2. Navegue até a pasta do projeto
3. Execute o comando:

```bash
python barbearia.py
```

## 🎨 Interface

- **Design moderno** com cores profissionais
- **Navegação por abas** organizada
- **Busca em tempo real** em todas as seções
- **Validações visuais** com mensagens claras
- **Formulários intuitivos** para cadastros

## 📝 Razão

Desenvolvido para laboratório de programação.

## 📄 Licença

Este projeto está licenciado sob a MIT License.
