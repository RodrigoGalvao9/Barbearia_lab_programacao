// Funções para gerenciar clientes
export { carregarClientes, removerCliente, atualizarVisibilidadeClientes, abrirModalAdicionarCliente, abrirModalEditarCliente, exibirBotaoAdicionarCliente };

import { mostrarPopup, abrirModalRemover } from './ui.js';

// ==================== FUNCIONALIDADES DE ADMIN PARA CLIENTES ====================

// Variáveis para controle do modal de cliente
let clienteEditandoId = null;

// Função para exibir botão de adicionar cliente para admin
function exibirBotaoAdicionarCliente() {
    const tipo = localStorage.getItem('tipo');
    const btnAdicionarCliente = document.getElementById('btn-adicionar-cliente');
    if (tipo === 'admin' && btnAdicionarCliente) {
        btnAdicionarCliente.style.display = 'inline-block';
    } else if (btnAdicionarCliente) {
        btnAdicionarCliente.style.display = 'none';
    }
}

// Função para abrir modal de adicionar cliente
function abrirModalAdicionarCliente() {
    clienteEditandoId = null;
    const modalCliente = document.getElementById('modal-cliente');
    const tituloModalCliente = document.getElementById('titulo-modal-cliente');
    const formCliente = document.getElementById('form-cliente');
    
    tituloModalCliente.textContent = 'Adicionar Cliente';
    formCliente.reset();
    modalCliente.style.display = 'flex';
}

// Função para abrir modal de editar cliente
function abrirModalEditarCliente(cliente) {
    clienteEditandoId = cliente.id;
    const modalCliente = document.getElementById('modal-cliente');
    const tituloModalCliente = document.getElementById('titulo-modal-cliente');
    
    tituloModalCliente.textContent = 'Editar Cliente';
    document.getElementById('cliente-nome').value = cliente.nome;
    document.getElementById('cliente-telefone').value = cliente.telefone;
    document.getElementById('cliente-email').value = cliente.email;
    modalCliente.style.display = 'flex';
}

// Carregar clientes com design moderno
function carregarClientes() {
    fetch('/api/clientes/', {headers: {'Accept': 'application/json'}})
        .then(res => res.json())
        .then(clientes => {
            window._clientes = clientes;
            const container = document.getElementById('clientes-lista');
            const tipo = localStorage.getItem('tipo');
            
            if (!Array.isArray(clientes) || clientes.length === 0) {
                container.innerHTML = '<p class="sem-dados">Nenhum cliente cadastrado.</p>';
                return;
            }
            
            // Criar estrutura de tabela moderna
            if (tipo === 'admin') {                container.innerHTML = `
                    <table class="clientes-tabela">
                        <thead>
                            <tr>
                                <th>👤 Cliente</th>
                                <th>📱 Telefone</th>
                                <th>📧 Email</th>
                                <th>🎯 Ações</th>
                            </tr>
                        </thead>
                        <tbody id="clientes-tbody">
                        </tbody>
                    </table>
                `;
                
                const tbody = document.getElementById('clientes-tbody');
                clientes.forEach((cliente, idx) => {
                    const tr = document.createElement('tr');
                    
                    tr.innerHTML = `
                        <td class="cliente-nome">
                            <strong>${cliente.nome || '-'}</strong>
                        </td>
                        <td class="cliente-telefone">
                            ${cliente.telefone ? `<a href="tel:${cliente.telefone}" class="link-telefone">${cliente.telefone}</a>` : '-'}
                        </td>
                        <td class="cliente-email">
                            ${cliente.email ? `<a href="mailto:${cliente.email}" class="link-email">${cliente.email}</a>` : '-'}
                        </td>
                        <td class="acoes-cliente">
                        </td>
                    `;
                    
                    // Adicionar botões com event listeners
                    const tdAcoes = tr.querySelector('.acoes-cliente');
                    
                    const btnEditar = document.createElement('button');
                    btnEditar.className = 'btn-editar-cliente';
                    btnEditar.textContent = 'Editar';
                    btnEditar.onclick = () => abrirModalEditarCliente(cliente);
                    
                    const btnRemover = document.createElement('button');
                    btnRemover.className = 'btn-remover-cliente';
                    btnRemover.textContent = 'Remover';
                    btnRemover.onclick = () => removerCliente(cliente.id);
                    
                    tdAcoes.appendChild(btnEditar);
                    tdAcoes.appendChild(btnRemover);
                    
                    tbody.appendChild(tr);
                });
            } else {
                // Vista simplificada para usuários comuns
                container.innerHTML = `
                    <div class="clientes-grid">
                        ${clientes.map(cliente => `
                            <div class="cliente-card">
                                <h4>${cliente.nome || 'Nome não informado'}</h4>
                                <p>📱 ${cliente.telefone || 'Telefone não informado'}</p>
                                <p>📧 ${cliente.email || 'Email não informado'}</p>
                            </div>
                        `).join('')}
                    </div>
                `;
            }
            
            // Exibe botão de adicionar cliente para admin
            exibirBotaoAdicionarCliente();
        })
        .catch(() => {
            const container = document.getElementById('clientes-lista');
            container.innerHTML = '<p class="erro-dados">Erro ao carregar clientes.</p>';
        });
}

async function removerCliente(id) {
    abrirModalRemover('Tem certeza que deseja remover este cliente?', async () => {
        try {
            const resp = await fetch(`/api/clientes/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            
            const data = await resp.json();
            
            if (resp.ok) {
                carregarClientes();
                mostrarPopup(data.mensagem || 'Cliente removido com sucesso!');
            } else {
                mostrarPopup(data.erro || 'Erro ao remover cliente.');
            }
        } catch {
            mostrarPopup('Erro ao conectar ao servidor.');
        }
    });
}

// Função para ocultar link/tela clientes para não-admin
function atualizarVisibilidadeClientes() {
    const tipo = localStorage.getItem('tipo');
    const navClientesEl = document.getElementById('nav-clientes');
    const telaClientes = document.getElementById('tela-clientes');
    if (navClientesEl) navClientesEl.style.display = (tipo === 'admin') ? '' : 'none';
    if (telaClientes && tipo !== 'admin') telaClientes.style.display = 'none';
}

// Inicialização dos eventos relacionados a clientes
document.addEventListener('DOMContentLoaded', () => {
    const navClientes = document.getElementById('nav-clientes');
    const btnAdicionarCliente = document.getElementById('btn-adicionar-cliente');
    const modalCliente = document.getElementById('modal-cliente');
    const formCliente = document.getElementById('form-cliente');
    const fecharModalCliente = document.getElementById('fechar-modal-cliente');
    
    // Listener para navegação de clientes com verificação de permissão
    if (navClientes) {
        navClientes.addEventListener('click', e => {
            e.preventDefault();
            if (localStorage.getItem('tipo') !== 'admin') {
                alert('Acesso restrito! Apenas administradores podem acessar a área de clientes.');
                return;
            }
            window.mostrarTela('tela-clientes');
            carregarClientes();
        });
    }

    // Botão adicionar cliente
    if (btnAdicionarCliente) {
        btnAdicionarCliente.onclick = abrirModalAdicionarCliente;
    }

    // Fechar modal
    if (fecharModalCliente) {
        fecharModalCliente.onclick = () => {
            modalCliente.style.display = 'none';
        };
    }

    // Formulário de cliente
    if (formCliente) {
        formCliente.onsubmit = async (e) => {
            e.preventDefault();
            const nome = document.getElementById('cliente-nome').value;
            const telefone = document.getElementById('cliente-telefone').value;
            const email = document.getElementById('cliente-email').value;
            const erro = document.getElementById('cliente-erro');
            erro.textContent = '';

            try {
                let resp;
                const body = {nome, telefone, email};
                
                if (clienteEditandoId) {
                    resp = await fetch(`/api/clientes/${clienteEditandoId}`, {
                        method: 'PUT',
                        headers: {'Content-Type': 'application/json'},
                        credentials: 'include',
                        body: JSON.stringify(body)
                    });
                } else {
                    resp = await fetch('/api/clientes/', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        credentials: 'include',
                        body: JSON.stringify(body)
                    });
                }

                const data = await resp.json();

                if (resp.ok) {
                    modalCliente.style.display = 'none';
                    carregarClientes();
                    window.mostrarPopup(data.mensagem || 'Cliente salvo com sucesso!');
                } else {
                    window.mostrarPopup(data.erro || 'Erro ao salvar cliente.');
                }
            } catch {
                window.mostrarPopup('Erro ao conectar ao servidor.');
            }
        };
    }

    // Atualiza visibilidade dos clientes ao carregar a página
    atualizarVisibilidadeClientes();
});

// Eventos para atualizar visibilidade quando o storage muda
window.addEventListener('storage', atualizarVisibilidadeClientes);
