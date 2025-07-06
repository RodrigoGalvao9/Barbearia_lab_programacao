// ==================== FUNCIONALIDADES DE VOUCHERS ====================
// Exporta as funções principais
export { carregarVouchers, usarVoucher, abrirModalAdicionarVoucher, abrirModalEditarVoucher, removerVoucher, exibirBotaoAdicionarVoucher };

import { mostrarPopup, abrirModalRemover } from './ui.js';

// Variáveis para controle do modal de voucher
let voucherEditandoId = null;

// Função para carregar vouchers com design moderno
function carregarVouchers() {
    const usuario = localStorage.getItem('usuario');
    const tipo = localStorage.getItem('tipo');
    
    // Define qual endpoint usar baseado no estado de login
    let endpoint;
    if (!usuario) {
        endpoint = '/api/vouchers/';
    } else if (tipo === 'admin') {
        endpoint = '/api/vouchers/';
    } else {
        endpoint = '/api/vouchers/meus-vouchers';
    }

    fetch(endpoint, {
        headers: {'Accept': 'application/json'},
        credentials: 'include'
    })
        .then(res => res.json())
        .then(data => {
            const vouchers = data.dados || data;
            const container = document.getElementById('vouchers-lista');
            
            if (!Array.isArray(vouchers) || vouchers.length === 0) {
                container.innerHTML = '<p class="sem-dados">Nenhum voucher disponível.</p>';
                return;
            }
            
            // Criar estrutura de tabela moderna para admin
            if (tipo === 'admin') {
                container.innerHTML = `
                    <table class="vouchers-tabela">
                        <thead>
                            <tr>
                                <th>🎫 Código</th>
                                <th>📝 Descrição</th>
                                <th>💸 Desconto</th>
                                <th>📅 Validade</th>
                                <th>👤 Usuário</th>
                                <th>📊 Status</th>
                                <th>🎯 Ações</th>
                            </tr>
                        </thead>
                        <tbody id="vouchers-tbody">
                        </tbody>
                    </table>
                `;
                
                const tbody = document.getElementById('vouchers-tbody');
                vouchers.forEach(voucher => {
                    const tr = document.createElement('tr');
                    
                    // Determinar status do voucher
                    const isVencido = voucher.validade && new Date(voucher.validade) < new Date();
                    const isUsado = voucher.usado;
                    let statusBadge, statusClass;
                    
                    if (isUsado) {
                        statusBadge = '<span class="status-usado">Usado</span>';
                        statusClass = 'voucher-usado-row';
                    } else if (isVencido) {
                        statusBadge = '<span class="status-vencido">Vencido</span>';
                        statusClass = 'voucher-vencido-row';
                    } else {
                        statusBadge = '<span class="status-ativo">Ativo</span>';
                        statusClass = 'voucher-ativo-row';
                    }
                    
                    tr.className = statusClass;
                    tr.innerHTML = `
                        <td class="voucher-codigo">
                            <code>${voucher.codigo}</code>
                        </td>
                        <td class="voucher-descricao">
                            ${voucher.descricao || '-'}
                        </td>
                        <td class="voucher-desconto">
                            <span class="desconto-badge">${voucher.porcentagem || 0}% OFF</span>
                        </td>
                        <td class="voucher-validade">
                            ${voucher.validade || 'Sem validade'}
                        </td>
                        <td class="voucher-usuario">
                            ${voucher.usuario || '<em>Público</em>'}
                        </td>
                        <td class="voucher-status">
                            ${statusBadge}
                        </td>
                        <td class="acoes-voucher">
                        </td>
                    `;
                    
                    // Adicionar botões para admin
                    const tdAcoes = tr.querySelector('.acoes-voucher');
                    
                    const btnEditar = document.createElement('button');
                    btnEditar.className = 'btn-editar-voucher';
                    btnEditar.textContent = 'Editar';
                    btnEditar.onclick = () => abrirModalEditarVoucher(voucher);
                    
                    const btnRemover = document.createElement('button');
                    btnRemover.className = 'btn-remover-voucher';
                    btnRemover.textContent = 'Remover';
                    btnRemover.onclick = () => removerVoucher(voucher.id);
                    
                    tdAcoes.appendChild(btnEditar);
                    tdAcoes.appendChild(btnRemover);
                    
                    tbody.appendChild(tr);
                });
            } else {
                // Vista em cards para usuários
                container.innerHTML = `
                    <div class="vouchers-grid">
                        ${vouchers.map(voucher => {
                            const isVencido = voucher.validade && new Date(voucher.validade) < new Date();
                            const isUsado = voucher.usado;
                            let statusClass = 'voucher-card';
                            
                            if (isUsado) statusClass += ' usado';
                            else if (isVencido) statusClass += ' vencido';
                            else statusClass += ' ativo';
                            
                            return `
                                <div class="${statusClass}">
                                    <div class="voucher-desconto-badge">${voucher.porcentagem || 0}% OFF</div>
                                    <h3>${voucher.codigo}</h3>
                                    <p>${voucher.descricao || 'Voucher de desconto'}</p>
                                    <div class="voucher-detalhes">
                                        <small>Válido até: ${voucher.validade || 'Sem validade'}</small>
                                        ${voucher.usuario === usuario ? '<br><small class="voucher-pessoal">Seu voucher pessoal</small>' : ''}
                                    </div>
                                    <div class="voucher-status">
                                        ${isUsado ? '<span class="status-usado">Usado</span>' : 
                                          isVencido ? '<span class="status-vencido">Vencido</span>' : 
                                          '<span class="status-ativo">Ativo</span>'}
                                    </div>
                                    ${!isUsado && !isVencido ? `<button class="btn-usar-voucher" onclick="window.usarVoucher('${voucher.codigo}')">Usar Voucher</button>` : ''}
                                </div>
                            `;
                        }).join('')}
                    </div>
                `;
            }
            
            // Exibe botão de adicionar voucher para admin
            exibirBotaoAdicionarVoucher();
        })
        .catch(() => {
            const container = document.getElementById('vouchers-lista');
            container.innerHTML = '<p class="erro-dados">Erro ao carregar vouchers.</p>';
        });
}

// ==================== FUNCIONALIDADES DE ADMIN PARA VOUCHERS ====================

// Função para exibir botão de adicionar voucher para admin
function exibirBotaoAdicionarVoucher() {
    const tipo = localStorage.getItem('tipo');
    const btnAdicionarVoucher = document.getElementById('btn-adicionar-voucher');
    if (tipo === 'admin' && btnAdicionarVoucher) {
        btnAdicionarVoucher.style.display = 'inline-block';
    } else if (btnAdicionarVoucher) {
        btnAdicionarVoucher.style.display = 'none';
    }
}

// Função para abrir modal de adicionar voucher
function abrirModalAdicionarVoucher() {
    voucherEditandoId = null;
    const modalVoucher = document.getElementById('modal-voucher');
    const tituloModalVoucher = document.getElementById('titulo-modal-voucher');
    const formVoucher = document.getElementById('form-voucher');
    
    tituloModalVoucher.textContent = 'Adicionar Voucher';
    formVoucher.reset();
    modalVoucher.style.display = 'flex';
}

// Função para abrir modal de editar voucher
function abrirModalEditarVoucher(voucher) {
    voucherEditandoId = voucher.id;
    const modalVoucher = document.getElementById('modal-voucher');
    const tituloModalVoucher = document.getElementById('titulo-modal-voucher');
    
    tituloModalVoucher.textContent = 'Editar Voucher';
    document.getElementById('voucher-codigo').value = voucher.codigo;
    document.getElementById('voucher-descricao').value = voucher.descricao;
    document.getElementById('voucher-desconto').value = voucher.porcentagem;
    document.getElementById('voucher-validade').value = voucher.validade || '';
    document.getElementById('voucher-usuario').value = voucher.usuario || '';
    modalVoucher.style.display = 'flex';
}

// Função para remover voucher
function removerVoucher(id) {
    abrirModalRemover('Tem certeza que deseja remover este voucher?', async () => {
        try {
            const resp = await fetch(`/api/vouchers/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            
            const data = await resp.json();
            
            if (resp.ok) {
                carregarVouchers();
                mostrarPopup(data.mensagem || 'Voucher removido com sucesso!');
            } else {
                mostrarPopup(data.erro || 'Erro ao remover voucher!', 'erro');
            }
        } catch (error) {
            console.error('Erro:', error);
            mostrarPopup('Erro de conexão ao remover voucher!', 'erro');
        }
    });
}

// ==================== FUNCIONALIDADES DE USUÁRIO ====================

// Função para usar voucher - disponível globalmente
function usarVoucher(codigo) {
    const usuario = localStorage.getItem('usuario');
    if (!usuario) {
        mostrarPopup('Você precisa estar logado para usar vouchers!', 'erro');
        return;
    }
    
    fetch('/api/vouchers/usar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ codigo })
    })
    .then(res => res.json())
    .then(data => {
        if (data.sucesso) {
            mostrarPopup(data.mensagem || 'Voucher usado com sucesso!');
            carregarVouchers(); // Recarrega a lista para atualizar o status
        } else {
            mostrarPopup(data.erro || 'Erro ao usar voucher!', 'erro');
        }
    })
    .catch(() => {
        mostrarPopup('Erro de conexão ao usar voucher!', 'erro');
    });
}

// Torna a função usarVoucher disponível globalmente
window.usarVoucher = usarVoucher;

// ==================== EVENTOS DO MODAL ====================

// Event listener para o formulário de voucher
document.addEventListener('DOMContentLoaded', function() {
    const formVoucher = document.getElementById('form-voucher');
    if (formVoucher) {
        formVoucher.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const voucherData = {
                codigo: document.getElementById('voucher-codigo').value,
                descricao: document.getElementById('voucher-descricao').value,
                porcentagem: parseInt(document.getElementById('voucher-desconto').value),
                validade: document.getElementById('voucher-validade').value || null,
                usuario: document.getElementById('voucher-usuario').value || null
            };
            
            try {
                const url = voucherEditandoId ? `/api/vouchers/${voucherEditandoId}` : '/api/vouchers/';
                const method = voucherEditandoId ? 'PUT' : 'POST';
                
                const resp = await fetch(url, {
                    method,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify(voucherData)
                });
                
                const data = await resp.json();
                
                if (resp.ok) {
                    document.getElementById('modal-voucher').style.display = 'none';
                    carregarVouchers();
                    mostrarPopup(data.mensagem || (voucherEditandoId ? 'Voucher atualizado' : 'Voucher criado') + ' com sucesso!');
                } else {
                    document.getElementById('voucher-erro').textContent = data.erro || 'Erro ao salvar voucher';
                }
            } catch (error) {
                console.error('Erro:', error);
                document.getElementById('voucher-erro').textContent = 'Erro de conexão';
            }
        });
    }
    
    // Botão para fechar modal
    const fecharModalVoucher = document.getElementById('fechar-modal-voucher');
    if (fecharModalVoucher) {
        fecharModalVoucher.addEventListener('click', function() {
            document.getElementById('modal-voucher').style.display = 'none';
        });
    }
    
    // Botão adicionar voucher
    const btnAdicionarVoucher = document.getElementById('btn-adicionar-voucher');
    if (btnAdicionarVoucher) {
        btnAdicionarVoucher.addEventListener('click', abrirModalAdicionarVoucher);
    }
});
