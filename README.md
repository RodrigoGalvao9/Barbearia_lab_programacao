# 🏛️ Barbearia Lab Programação

Sistema web **completo e moderno** para gerenciamento de barbearia, com autenticação, controle de agendamentos, clientes, cortes, vouchers de fidelidade, **filtros avançados** e permissões de administrador. Interface **totalmente repaginada** com design moderno, responsiva e integrada ao backend.

## 🚀 Tecnologias Utilizadas

- **Backend:** Python 3 + Flask com rotas modulares e validação de sessão
- **Frontend:** HTML5, CSS3 (moderno com custom properties), JavaScript ES6+ modular
- **Design System:** CSS com variáveis, transições suaves e responsividade total
- **Armazenamento:** JSON (arquivos locais) com estrutura otimizada
- **Integração:** Fetch API com credentials, controle de sessão e cache inteligente
- **Arquitetura:** SPA (Single Page Application) com carregamento dinâmico
- **UX/UI:** Interface moderna, cards responsivos e feedback visual completo

## ✨ Funcionalidades

### 🔐 1. Autenticação e Controle de Sessão
- Login, registro e logout de usuários com validação completa
- **Permissões diferenciadas:** usuário comum (cliente) e administrador
- Controle de sessão via cookies e localStorage
- **Títulos centralizados** nas telas de login e registro

### 📊 2. CRUD Completo com Design Moderno
- **🎨 Interface repaginada:** Todas as tabelas com design moderno e consistente
- **Tabelas para admin:** Layout profissional com headers estilizados, hover effects e ações
- **Cards para clientes:** Design em grid responsivo com informações organizadas
- **Cortes:** Gestão completa com popularidade simulada e preços destacados
- **Clientes:** Cadastro com links diretos para telefone e email
- **Agendamentos:** Sistema completo com **filtros por período**
- **Vouchers:** Gestão avançada com status visuais e badges

### 🎫 3. Sistema de Fidelidade Avançado
- **Geração automática** de voucher a cada 5 agendamentos
- **Vouchers públicos e privados:** Controle de visibilidade por usuário
- **Porcentagem de desconto:** Sistema flexível de descontos
- **Aplicação inteligente:** Vouchers aplicados automaticamente no agendamento
- **Status visuais:** Ativo, Usado, Vencido com cores diferenciadas
- **Restrições:** Não permite voucher com pagamento em dinheiro

### 📅 4. **NOVO! Filtros de Agendamentos**
- **🌟 Hoje (padrão):** Agendamentos do dia atual
- **⏰ Amanhã:** Agendamentos do próximo dia  
- **📅 Esta Semana:** Agendamentos da semana corrente
- **📆 Este Mês:** Agendamentos do mês atual
- **🗂️ Todos:** Visualização completa
- **Interface intuitiva:** Select estilizado com aplicação automática
- **Performance otimizada:** Filtros em tempo real sem recarregar

### 🎯 5. Experiência Diferenciada por Usuário
- **👑 Admin:** Tabelas completas + filtros + ações (editar/remover/adicionar)
- **👤 Cliente:** Cards modernos + filtros + informações organizadas
- **Botões de ação** visíveis apenas para admin
- **Rotas protegidas** no backend com validação de permissões
- **Sessão obrigatória** para agendar e acessar dados pessoais

### 🎨 6. **NOVO! Design System Moderno**
- **CSS com Custom Properties:** Variáveis para cores, espaçamentos e tipografia
- **Transições suaves:** Hover effects e animações em todos os elementos
- **Badges e status:** Indicadores visuais coloridos para diferentes estados
- **Responsividade total:** Design adaptativo para desktop, tablet e mobile
- **Hierarquia visual clara:** Tipografia e cores organizadas por importância

### 💳 7. Agendamento e Pagamento Inteligente
- **Modal de agendamento** com seleção completa (data, horário, corte, voucher, pagamento)
- **Cálculo automático:** Aplicação de desconto e valor final em tempo real
- **Restrições inteligentes:** Voucher desabilitado para pagamento em dinheiro
- **Comprovante visual:** Modal estilizado com resumo completo
- **Validação completa:** Verificação de vouchers em tempo real

### 🏷️8. **NOVO! Cards Modernos para Clientes**
- **Grid responsivo:** Layout adaptável para diferentes telas
- **Status visuais por cores:**
  - 🟢 **Hoje:** Verde (prioritário)
  - 🔵 **Amanhã:** Azul (próximo)  
  - 🟡 **Futuro:** Amarelo (agendado)
  - ⚫ **Passado:** Cinza (finalizado)
- **Informações organizadas:** Layout com ícones e estrutura clara
- **Seção de preços:** Valor original, desconto e economia destacados
- **Vouchers aplicados:** Exibição especial com benefícios

### 🎭 9. Experiência do Usuário Aprimorada
- **Navegação SPA** sem recarregar página
- **Modais reutilizáveis** e totalmente estilizados
- **Feedback visual completo:** Popups, confirmações, mensagens de erro/sucesso
- **Campos de senha** com botão "exibir/ocultar"
- **Validação em tempo real** para formulários
- **Atualização dinâmica** de permissões ao logar/deslogar

## 🚀 Como Usar

1. **Instale as dependências automaticamente:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o backend (que já serve a interface):**
   ```bash
   python app.py
   ```

3. **Acesse o sistema:**
   - Abra o navegador e acesse: [http://localhost:5000](http://localhost:5000)

4. **Crie um usuário admin:**
   - Registre normalmente e altere o tipo para "admin" no arquivo `backend/arquivos/usuarios.json` (campo `tipo`)

5. **Explore as funcionalidades:**
   - **Como cliente:** Visualize cards modernos, faça agendamentos, use filtros
   - **Como admin:** Gerencie todas as tabelas, use filtros avançados, controle total

## 📁 Estrutura de Pastas

```
├── backend/                 # Código Python (Flask) e arquivos JSON
│   ├── __init__.py         # Configuração principal do Flask
│   ├── agendamentos.py     # CRUD de agendamentos com filtros
│   ├── clientes.py         # CRUD de clientes
│   ├── cortes.py          # CRUD de cortes
│   ├── usuarios.py        # Autenticação e usuários
│   ├── vouchers.py        # Sistema de vouchers com porcentagem
│   └── arquivos/          # Armazenamento JSON
├── interface/              # Frontend moderno e responsivo
│   ├── index.html         # Interface principal com filtros
│   ├── style.css          # CSS moderno com custom properties
│   └── js/                # JavaScript modular ES6+
│       ├── main.js        # Arquivo principal e coordenação
│       ├── navigation.js  # Navegação SPA
│       ├── ui.js          # Modais e feedback visual
│       ├── auth.js        # Autenticação
│       ├── agendamentos.js # Agendamentos com filtros
│       ├── clientes.js    # Gestão de clientes
│       ├── cortes.js      # Gestão de cortes
│       └── vouchers.js    # Sistema de vouchers
└── app.py                 # Servidor principal
```

## 🎯 Destaques da Versão Atual

### ✅ **Totalmente Repaginado**
- **Design moderno** em todas as tabelas e interfaces
- **Filtros avançados** para agendamentos por período
- **Cards responsivos** para experiência mobile otimizada
- **Sistema de cores** consistente com variáveis CSS

### ✅ **Performance Otimizada**
- **Modularização completa** do JavaScript ES6+
- **Filtros em tempo real** sem recarregar página
- **Cache inteligente** para dados de agendamentos
- **Transições suaves** sem impacto na performance

### ✅ **UX/UI Profissional**
- **Hierarquia visual clara** com tipografia moderna
- **Feedback visual completo** para todas as ações
- **Responsividade total** testada em diferentes dispositivos
- **Acessibilidade** melhorada com cores contrastantes

## 📝 Observações

- **Desenvolvimento:** Sistema completo para fins didáticos e laboratoriais
- **Armazenamento:** Utiliza JSON para facilitar testes e deploy local
- **Produção:** Para uso comercial, recomenda-se adaptar para banco de dados real e HTTPS
- **Compatibilidade:** Testado nos principais navegadores modernos
- **Mobile:** Interface totalmente responsiva e touch-friendly


## 🏆 Funcionalidades Únicas

- ✨ **Filtros inteligentes** de agendamentos com padrão "hoje"
- 🎨 **Design system** moderno com custom properties CSS
- 📱 **Cards responsivos** para experiência mobile otimizada  
- 🎫 **Sistema de vouchers** com porcentagem e validação em tempo real
- 👑 **Experiência diferenciada** para admin e clientes
- 🚀 **Performance** otimizada com JavaScript modular
- 🎯 **Títulos centralizados** em todas as seções principais
- 💳 **Cálculo automático** de descontos e valores finais
- 🔒 **Validação avançada** com restrições inteligentes
- 🌟 **Status visuais** diferenciados por cores e badges

---
**🎯 Desenvolvido com foco em modernidade, usabilidade e performance!**
*Sistema de barbearia completo, pronto para uso educacional e profissional.*
