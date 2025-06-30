// Funções para gerenciar cortes
export { carregarCortes, exibirBotaoAdicionarCorte, abrirModalAdicionarCorte, abrirModalEditarCorte, removerCorte };

import { mostrarPopup, abrirModalRemover } from './ui.js';

// Função para carregar cortes com design moderno
function carregarCortes() {
    fetch('/api/cortes/', {headers: {'Accept': 'application/json'}})
        .then(res => res.json())
        .then(cortes => {
            window._cortes = cortes;
            const container = document.getElementById('cortes-lista');
            const tipo = localStorage.getItem('tipo');
            
            if (!Array.isArray(cortes) || cortes.length === 0) {
                container.innerHTML = '<p class="sem-dados">Nenhum corte cadastrado.</p>';
                return;
            }
            
            // Criar estrutura de tabela moderna
            if (tipo === 'admin') {                container.innerHTML = `
                    <table class="cortes-tabela">
                        <thead>
                            <tr>
                                <th>✂️ Corte</th>
                                <th>📝 Descrição</th>
                                <th>💰 Preço</th>
                                <th>🔥 Popularidade</th>
                                <th>🎯 Ações</th>
                            </tr>
                        </thead>
                        <tbody id="cortes-tbody">
                        </tbody>
                    </table>
                `;
                
                const tbody = document.getElementById('cortes-tbody');
                cortes.forEach((corte, idx) => {
                    const tr = document.createElement('tr');
                    
                    // Simular popularidade baseada no ID (menor ID = mais popular)
                    const popularidade = Math.max(1, 6 - (corte.id || 1));
                    const estrelas = '⭐'.repeat(Math.min(popularidade, 5));
                    
                    tr.innerHTML = `
                        <td class="corte-nome">
                            <strong>${corte.nome || '-'}</strong>
                        </td>
                        <td class="corte-descricao">
                            ${corte.descricao || '-'}
                        </td>
                        <td class="corte-preco">
                            <span class="preco-valor">R$ ${Number(corte.preco || 0).toFixed(2)}</span>
                        </td>
                        <td class="corte-popularidade">
                            ${estrelas}
                        </td>
                        <td class="acoes-corte">
                        </td>
                    `;
                    
                    // Adicionar botões com event listeners
                    const tdAcoes = tr.querySelector('.acoes-corte');
                    
                    const btnEditar = document.createElement('button');
                    btnEditar.className = 'btn-editar-corte';
                    btnEditar.textContent = 'Editar';
                    btnEditar.onclick = () => abrirModalEditarCorte(corte);
                    
                    const btnRemover = document.createElement('button');
                    btnRemover.className = 'btn-remover-corte';
                    btnRemover.textContent = 'Remover';
                    btnRemover.onclick = () => removerCorte(corte.id);
                    
                    tdAcoes.appendChild(btnEditar);
                    tdAcoes.appendChild(btnRemover);
                    
                    tbody.appendChild(tr);
                });
            } else {
                // Vista em cards para usuários comuns
                container.innerHTML = `
                    <div class="cortes-grid">
                        ${cortes.map(corte => `
                            <div class="corte-card">
                                <h3>${corte.nome || 'Corte'}</h3>
                                <p class="corte-descricao">${corte.descricao || 'Descrição não informada'}</p>
                                <div class="corte-preco">R$ ${Number(corte.preco || 0).toFixed(2)}</div>
                            </div>
                        `).join('')}
                    </div>
                `;
            }
            
            // Botão adicionar corte
            exibirBotaoAdicionarCorte();
        })
        .catch(() => {
            const container = document.getElementById('cortes-lista');
            container.innerHTML = '<p class="erro-dados">Erro ao carregar cortes.</p>';
        });
}

function exibirBotaoAdicionarCorte() {
    const tipo = localStorage.getItem('tipo');
    const tabela = document.getElementById('tabela-cortes');
    if (tipo === 'admin' && tabela && !document.getElementById('btn-adicionar-corte')) {
        const btn = document.createElement('button');
        btn.id = 'btn-adicionar-corte';
        btn.textContent = 'Adicionar Corte';
        btn.onclick = abrirModalAdicionarCorte;
        btn.className = 'btn-editar-corte';
        tabela.parentElement.insertBefore(btn, tabela);
    }
    if (tipo !== 'admin' && document.getElementById('btn-adicionar-corte')) {
        document.getElementById('btn-adicionar-corte').remove();
    }
}

// Modal de adicionar/editar corte (admin)
let corteEditandoId = null;

function abrirModalAdicionarCorte() {
    corteEditandoId = null;
    const modalCorte = document.getElementById('modal-corte');
    const tituloModalCorte = document.getElementById('titulo-modal-corte');
    const formCorte = document.getElementById('form-corte');
    
    tituloModalCorte.textContent = 'Adicionar Corte';
    formCorte.reset();
    modalCorte.style.display = 'flex';
}

function abrirModalEditarCorte(corte) {
    corteEditandoId = corte.id;
    const modalCorte = document.getElementById('modal-corte');
    const tituloModalCorte = document.getElementById('titulo-modal-corte');
    
    tituloModalCorte.textContent = 'Editar Corte';
    document.getElementById('corte-nome').value = corte.nome;
    document.getElementById('corte-descricao').value = corte.descricao;
    document.getElementById('corte-preco').value = corte.preco;
    modalCorte.style.display = 'flex';
}

async function removerCorte(id) {
    abrirModalRemover('Tem certeza que deseja remover este corte?', async () => {
        try {
            const resp = await fetch(`/api/cortes/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            if (resp.ok) {
                carregarCortes();
                mostrarPopup('Corte removido com sucesso!');
            } else {
                const data = await resp.json();
                mostrarPopup(data.erro || 'Erro ao remover corte.');
            }
        } catch {
            mostrarPopup('Erro ao conectar ao servidor.');
        }
    });
}

// Inicialização dos eventos do modal de corte
document.addEventListener('DOMContentLoaded', () => {
    const modalCorte = document.getElementById('modal-corte');
    const formCorte = document.getElementById('form-corte');
    const fecharModalCorte = document.getElementById('fechar-modal-corte');

    if (fecharModalCorte) {
        fecharModalCorte.onclick = () => {
            modalCorte.style.display = 'none';
        };
    }

    if (formCorte) {
        formCorte.onsubmit = async (e) => {
            e.preventDefault();
            const nome = document.getElementById('corte-nome').value;
            const descricao = document.getElementById('corte-descricao').value;
            const preco = parseFloat(document.getElementById('corte-preco').value);
            const erro = document.getElementById('corte-erro');
            erro.textContent = '';
            try {
                let resp;
                if (corteEditandoId) {
                    resp = await fetch(`/api/cortes/${corteEditandoId}`, {
                        method: 'PUT',
                        headers: {'Content-Type': 'application/json'},
                        credentials: 'include',
                        body: JSON.stringify({nome, descricao, preco})
                    });
                } else {
                    resp = await fetch('/api/cortes/', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        credentials: 'include',
                        body: JSON.stringify({nome, descricao, preco})
                    });
                }
                if (resp.ok) {
                    modalCorte.style.display = 'none';
                    carregarCortes();
                    mostrarPopup('Corte salvo com sucesso!');
                } else {
                    const data = await resp.json();
                    mostrarPopup(data.erro || 'Erro ao salvar corte.');
                }
            } catch {
                mostrarPopup('Erro ao conectar ao servidor.');
            }
        };
    }
});
