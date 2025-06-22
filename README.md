# Barbearia Lab Programação

Sistema web completo para gerenciamento de barbearia, com autenticação, controle de agendamentos, clientes, cortes, vouchers de fidelidade e permissões de administrador. Interface moderna, responsiva e totalmente integrada ao backend.

## Tecnologias Utilizadas

- **Backend:** Python 3 + Flask
- **Frontend:** HTML5, CSS3 (moderno, responsivo, dark), JavaScript puro (ES6+)
- **Armazenamento:** JSON (arquivos locais)
- **Integração:** Fetch API (com credentials para sessão)

## Funcionalidades

### 1. Autenticação e Controle de Sessão
- Login, registro e logout de usuários.
- Permissões diferenciadas: usuário comum (cliente) e administrador.
- Controle de sessão via cookies e localStorage.

### 2. CRUD Completo
- **Cortes:** Adicionar, editar, remover e listar cortes disponíveis. Apenas admin pode gerenciar.
- **Clientes:** Cadastro, edição, remoção e listagem de clientes. Apenas admin pode gerenciar.
- **Agendamentos:** Qualquer usuário autenticado pode agendar. Admin pode editar/remover todos os agendamentos.
- **Vouchers:** Sistema de fidelidade automático. A cada 5 agendamentos, o cliente recebe um voucher exclusivo.

### 3. Sistema de Fidelidade
- Geração automática de voucher a cada 5 agendamentos do mesmo usuário.
- Vouchers listados na tela "Vouchers" e no perfil do usuário.
- Uso do código do voucher no momento do agendamento para desconto.

### 4. Permissões e Segurança
- Botões de ação (editar/remover/adicionar) visíveis apenas para admin.
- Rotas protegidas no backend: apenas admin pode acessar/alterar dados sensíveis.
- Sessão obrigatória para agendar ou acessar dados pessoais.

### 5. Interface Moderna e Responsiva
- Layout escuro, elegante e adaptável a dispositivos móveis.
- Feedback visual: popups, modais de confirmação, mensagens de erro e sucesso.
- Navegação SPA (Single Page Application) sem recarregar a página.

### 6. Agendamento e Pagamento
- Modal de agendamento com seleção de data, horário, corte, voucher e forma de pagamento.
- Modal de resumo de pagamento exibido apenas para clientes e apenas quando a forma de pagamento for diferente de "dinheiro".
- Tela de pagamento estilizada, com resumo dos dados e status.

### 7. Experiência do Usuário
- Atualização dinâmica dos botões e permissões ao logar/deslogar.
- Modais reutilizáveis e estilizados para confirmação de remoção, login, registro, edição de perfil, etc.
- Campos de senha com botão "exibir/ocultar" e validação de confirmação de senha no registro.

## Como Usar

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
   - Registre normalmente e altere o tipo para "admin" no arquivo `backend/arquivos/usuarios.json` (campo `tipo`).

## Estrutura de Pastas

- `backend/` — Código Python (Flask) e arquivos JSON
- `interface/` — HTML, CSS e JS do frontend

## Observações
- O sistema não utiliza banco de dados, apenas arquivos JSON para facilitar testes e deploy local.
- Para produção, recomenda-se adaptar para banco de dados real e HTTPS.

---
Desenvolvido para fins didáticos e laboratoriais. Qualquer dúvida ou sugestão, entre em contato!
