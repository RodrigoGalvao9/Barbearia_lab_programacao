// Funções para gerenciar agendamentos
export { carregarAgendamentos, removerAgendamento, mostrarResumoPagamento, abrirModalEditarAgendamento, inicializarAgendamento, mostrarComprovanteAgendamento, aplicarFiltroData };

import { mostrarPopup, abrirModalRemover } from './ui.js';

// Variáveis globais para controle do agendamento e filtro
let corteSelecionado = null;
let voucherAplicado = null;
let valorOriginal = 0;
let valorFinal = 0;
let agendamentosOriginais = []; // Armazena todos os agendamentos
let filtroAtual = 'hoje'; // Filtro padrão

// Função para inicializar funcionalidades de agendamento
function inicializarAgendamento() {
    configurarModalAgendamento();
    configurarFiltroData();
}

// Função para configurar o filtro de data
function configurarFiltroData() {
    const selectFiltro = document.getElementById('select-dia-filtro');
    const btnAplicarFiltro = document.getElementById('btn-aplicar-filtro');
    
    if (selectFiltro) {
        selectFiltro.value = filtroAtual;
        selectFiltro.addEventListener('change', function() {
            filtroAtual = this.value;
            aplicarFiltroData();
        });
    }
    
    if (btnAplicarFiltro) {
        btnAplicarFiltro.addEventListener('click', aplicarFiltroData);
    }
}

// Função para carregar agendamentos da API
function carregarAgendamentos() {
    fetch('/api/agendamentos/', {headers: {'Accept': 'application/json'}})
        .then(res => res.json())
        .then(agendamentos => {
            // Armazena os dados originais para filtros
            agendamentosOriginais = agendamentos || [];
            
            // Aplica o filtro atual (padrão é "hoje")
            aplicarFiltroData();
        })
        .catch(() => {
            const lista = document.getElementById('agendamentos-lista');
            lista.innerHTML = '<p class="erro-dados">Erro ao carregar agendamentos.</p>';
        });
}

// Função para aplicar filtro de data aos agendamentos
function aplicarFiltroData() {
    if (agendamentosOriginais.length === 0) {
        const lista = document.getElementById('agendamentos-lista');
        lista.innerHTML = `
            <div class="sem-dados">
                <p>📅 Nenhum agendamento encontrado para o filtro selecionado.</p>
                <small>Tente selecionar um período diferente ou "Todos" para ver todos os agendamentos.</small>
            </div>
        `;
        return;
    }
    
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    
    const amanha = new Date(hoje);
    amanha.setDate(amanha.getDate() + 1);
    
    const inicioSemana = new Date(hoje);
    const diasParaDomingo = hoje.getDay();
    inicioSemana.setDate(hoje.getDate() - diasParaDomingo);
    
    const fimSemana = new Date(inicioSemana);
    fimSemana.setDate(inicioSemana.getDate() + 6);
    
    const inicioMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    const fimMes = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0);
    
    let agendamentosFiltrados = agendamentosOriginais.filter(ag => {
        if (!ag.data) return false;
        
        const dataAgendamento = new Date(ag.data + 'T00:00:00');
        dataAgendamento.setHours(0, 0, 0, 0);
        
        switch (filtroAtual) {
            case 'hoje':
                return dataAgendamento.getTime() === hoje.getTime();
            case 'amanha':
                return dataAgendamento.getTime() === amanha.getTime();
            case 'semana':
                return dataAgendamento >= inicioSemana && dataAgendamento <= fimSemana;
            case 'mes':
                return dataAgendamento >= inicioMes && dataAgendamento <= fimMes;
            case 'todos':
                return true;
            default:
                return true;
        }
    });
    
    renderizarAgendamentos(agendamentosFiltrados);
}

// Função para determinar o status de um agendamento baseado na data
function obterStatusAgendamento(dataAgendamento) {
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    
    const amanha = new Date(hoje);
    amanha.setDate(amanha.getDate() + 1);
    
    const dataAg = new Date(dataAgendamento + 'T00:00:00');
    dataAg.setHours(0, 0, 0, 0);
    
    if (dataAg.getTime() === hoje.getTime()) {
        return { status: 'hoje', label: 'Hoje', class: 'status-hoje' };
    } else if (dataAg.getTime() === amanha.getTime()) {
        return { status: 'amanha', label: 'Amanhã', class: 'status-amanha' };
    } else if (dataAg > hoje) {
        return { status: 'futuro', label: 'Futuro', class: 'status-futuro' };
    } else {
        return { status: 'passado', label: 'Passado', class: 'status-passado' };
    }
}

// Função para renderizar agendamentos (separada da função de carregamento)
function renderizarAgendamentos(agendamentos) {
    const lista = document.getElementById('agendamentos-lista');
    const tipo = localStorage.getItem('tipo');
    
    if (!Array.isArray(agendamentos) || agendamentos.length === 0) {
        lista.innerHTML = `
            <div class="sem-dados">
                <p>📅 Nenhum agendamento encontrado para o filtro selecionado.</p>
                <small>Tente selecionar um período diferente ou "Todos" para ver todos os agendamentos.</small>
            </div>
        `;
        return;
    }
    
    // Criar estrutura de tabela para admins
    if (tipo === 'admin') {
        lista.innerHTML = `
            <table class="agendamentos-tabela">
                <thead>
                    <tr>
                        <th>👤 Cliente</th>
                        <th>📅 Data</th>
                        <th>⏰ Horário</th>
                        <th>✂️ Corte</th>
                        <th>💳 Pagamento</th>
                        <th>🎫 Voucher</th>
                        <th>💰 Valor</th>
                        <th>🎯 Ações</th>
                    </tr>
                </thead>
                <tbody id="agendamentos-tbody">
                </tbody>
            </table>
        `;
        
        const tbody = document.getElementById('agendamentos-tbody');
        agendamentos.forEach((ag) => {
            const tr = document.createElement('tr');
            const statusInfo = obterStatusAgendamento(ag.data);
            
            // Calcular valor final
            const valorCorte = ag.valor_corte || 0;
            const descontoVoucher = ag.desconto_voucher || 0;
            const valorFinal = ag.valor_final || (valorCorte - descontoVoucher);
            
            // Adicionar classe baseada no status
            tr.className = `agendamento-row ${statusInfo.status}`;
            
            tr.innerHTML = `
                <td class="cliente-nome">${ag.nome_cliente || '-'}</td>
                <td class="data-agendamento">
                    ${ag.data || '-'}
                    <br><small class="${statusInfo.class}">${statusInfo.label}</small>
                </td>
                <td class="horario-agendamento">${ag.horario || '-'}</td>
                <td class="corte-agendamento">${ag.tipo_corte || '-'}</td>
                <td class="pagamento-agendamento">
                    <span class="pagamento-badge pagamento-${ag.pagamento}">
                        ${ag.pagamento || '-'}
                    </span>
                </td>
                <td class="voucher-agendamento">${ag.voucher ? `<span class="voucher-usado">${ag.voucher}</span>` : '<span class="sem-voucher">-</span>'}</td>
                <td class="valor-agendamento">
                    ${valorFinal > 0 ? `<span class="valor-total">R$ ${valorFinal.toFixed(2)}</span>` : '-'}
                    ${descontoVoucher > 0 ? `<br><small class="desconto">-R$ ${descontoVoucher.toFixed(2)}</small>` : ''}
                </td>
                <td class="acoes-agendamento">
                </td>
            `;
            
            // Adicionar botões com event listeners
            const tdAcoes = tr.querySelector('.acoes-agendamento');
            
            const btnEditar = document.createElement('button');
            btnEditar.className = 'btn-editar-agendamento';
            btnEditar.textContent = 'Editar';
            btnEditar.onclick = () => abrirModalEditarAgendamento(ag);
            
            const btnRemover = document.createElement('button');
            btnRemover.className = 'btn-remover-agendamento';
            btnRemover.textContent = 'Remover';
            btnRemover.onclick = () => removerAgendamento(ag.id);
            
            tdAcoes.appendChild(btnEditar);
            tdAcoes.appendChild(btnRemover);
            
            tbody.appendChild(tr);
        });
    } else {
        // Vista em cards moderna para usuários comuns
        lista.innerHTML = `
            <div class="agendamentos-grid">
                ${agendamentos.map(ag => {
                    const statusInfo = obterStatusAgendamento(ag.data);
                    const valorCorte = ag.valor_corte || 0;
                    const descontoVoucher = ag.desconto_voucher || 0;
                    const valorFinal = ag.valor_final || (valorCorte - descontoVoucher);
                    
                    return `
                        <div class="agendamento-card ${statusInfo.status}">
                            <div class="agendamento-header">
                                <h3 class="agendamento-cliente">${ag.nome_cliente || 'Cliente'}</h3>
                                <span class="agendamento-status ${statusInfo.class}">${statusInfo.label}</span>
                            </div>
                            
                            <div class="agendamento-info">
                                <div class="info-item">
                                    <span class="info-label">📅 Data</span>
                                    <span class="info-value">${ag.data || '-'}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">⏰ Horário</span>
                                    <span class="info-value">${ag.horario || '-'}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">✂️ Corte</span>
                                    <span class="info-value">${ag.tipo_corte || '-'}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">💳 Pagamento</span>
                                    <span class="info-value">
                                        <span class="pagamento-badge pagamento-${ag.pagamento}">
                                            ${ag.pagamento || '-'}
                                        </span>
                                    </span>
                                </div>
                            </div>
                            
                            ${ag.voucher ? `
                                <div class="voucher-aplicado">
                                    🎫 Voucher: ${ag.voucher}
                                </div>
                            ` : ''}
                            
                            <div class="agendamento-preco">
                                ${descontoVoucher > 0 ? `
                                    <div class="preco-desconto">R$ ${valorCorte.toFixed(2)}</div>
                                    <div class="preco-final">R$ ${valorFinal.toFixed(2)}</div>
                                    <small>Economia: R$ ${descontoVoucher.toFixed(2)}</small>
                                ` : `
                                    <div class="preco-final">R$ ${valorFinal.toFixed(2)}</div>
                                `}
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }
}

async function removerAgendamento(id) {
    abrirModalRemover('Tem certeza que deseja remover este agendamento?', async () => {
        try {
            const resp = await fetch(`/api/agendamentos/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            
            const data = await resp.json();
            
            if (resp.ok) {
                carregarAgendamentos();
                mostrarPopup(data.mensagem || 'Agendamento removido com sucesso!');
            } else {
                mostrarPopup(data.erro || 'Erro ao remover agendamento.');
            }
        } catch {
            mostrarPopup('Erro ao conectar ao servidor.');
        }
    });
}

// Função para mostrar resumo de pagamento
function mostrarResumoPagamento(agendamento) {
    const modal = document.getElementById('modal-pagamento');
    const resumo = document.getElementById('resumo-pagamento');
    if (!modal || !resumo) return;
    
    // Calcula valores se voucher foi usado
    let valorCorte = agendamento.valor_corte || 0;
    let desconto = agendamento.desconto_voucher || 0;
    let valorFinal = agendamento.valor_final || valorCorte;
    
    resumo.innerHTML = `
        <div style="border: 2px solid #4CAF50; border-radius: 8px; padding: 20px; background: #f9f9f9;">
            <h4 style="color: #4CAF50; margin-top: 0;">✅ Agendamento Confirmado!</h4>
            <div style="color: #333; line-height: 1.6;">
                <strong>Cliente:</strong> ${agendamento.nome_cliente}<br>
                <strong>Data:</strong> ${agendamento.data}<br>
                <strong>Horário:</strong> ${agendamento.horario}<br>
                <strong>Corte:</strong> ${agendamento.tipo_corte}<br>
                <strong>Pagamento:</strong> ${agendamento.pagamento}<br>
                ${agendamento.voucher ? `<strong>Voucher:</strong> ${agendamento.voucher}<br>` : ''}
                <hr style="margin: 15px 0;">
                ${desconto > 0 ? `
                    <div style="text-decoration: line-through; color: #999;">
                        Valor original: R$ ${valorCorte.toFixed(2)}
                    </div>
                    <div style="color: #f44336;">
                        Desconto: -R$ ${desconto.toFixed(2)}
                    </div>
                ` : ''}
                <div style="font-size: 1.3em; font-weight: bold; color: #4CAF50;">
                    Total: R$ ${valorFinal.toFixed(2)}
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

// Função para mostrar comprovante de agendamento
function mostrarComprovanteAgendamento(agendamento) {
    mostrarResumoPagamento(agendamento);
}

// Função para abrir modal de editar agendamento
function abrirModalEditarAgendamento(agendamento) {
    const modal = document.getElementById('modal-editar-agendamento');
    if (!modal) return;
    
    // Preencher campos com dados do agendamento
    document.getElementById('editar-agendamento-nome').value = agendamento.nome_cliente || '';
    document.getElementById('editar-agendamento-data').value = agendamento.data || '';
    document.getElementById('editar-agendamento-horario').value = agendamento.horario || '';
    document.getElementById('editar-agendamento-voucher').value = agendamento.voucher || '';
    document.getElementById('editar-agendamento-pagamento').value = agendamento.pagamento || '';
    
    // Armazenar ID do agendamento sendo editado
    modal.dataset.agendamentoId = agendamento.id;
    
    modal.style.display = 'flex';
}

// ==================== CONFIGURAÇÃO DE MODAL DE AGENDAMENTO ====================

function configurarModalAgendamento() {
    const form = document.getElementById('form-agendamento');
    const modalAgendamento = document.getElementById('modal-agendamento');
    const btnFechar = document.getElementById('fechar-modal-agendamento');
    const selectCorte = document.getElementById('agendamento-corte');
    const selectPagamento = document.getElementById('agendamento-pagamento');
    const btnAplicarVoucher = document.getElementById('btn-aplicar-voucher');
    
    // Carregar opções de cortes
    carregarCortesNoSelect();
    
    // Event listeners
    if (form) {
        form.addEventListener('submit', enviarAgendamento);
    }
    
    if (btnFechar) {
        btnFechar.addEventListener('click', () => {
            modalAgendamento.style.display = 'none';
            limparFormularioAgendamento();
        });
    }
    
    if (selectCorte) {
        selectCorte.addEventListener('change', selecionarCorte);
    }
    
    if (selectPagamento) {
        selectPagamento.addEventListener('change', controlarVoucherSection);
    }
    
    if (btnAplicarVoucher) {
        btnAplicarVoucher.addEventListener('click', aplicarVoucher);
    }
    
    // Event listener para modal de editar agendamento
    const formEditar = document.getElementById('form-editar-agendamento');
    const btnFecharEditar = document.getElementById('fechar-modal-editar-agendamento');
    
    if (formEditar) {
        formEditar.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const modal = document.getElementById('modal-editar-agendamento');
            const agendamentoId = modal.dataset.agendamentoId;
            
            if (!agendamentoId) return;
            
            const dadosAtualizados = {
                nome_cliente: document.getElementById('editar-agendamento-nome').value,
                data: document.getElementById('editar-agendamento-data').value,
                horario: document.getElementById('editar-agendamento-horario').value,
                voucher: document.getElementById('editar-agendamento-voucher').value,
                pagamento: document.getElementById('editar-agendamento-pagamento').value
            };
            
            try {
                const resp = await fetch(`/api/agendamentos/${agendamentoId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify(dadosAtualizados)
                });
                
                const data = await resp.json();
                
                if (resp.ok) {
                    modal.style.display = 'none';
                    carregarAgendamentos();
                    mostrarPopup(data.mensagem || 'Agendamento atualizado com sucesso!');
                } else {
                    document.getElementById('editar-agendamento-erro').textContent = data.erro || 'Erro ao atualizar agendamento';
                }
            } catch (error) {
                console.error('Erro:', error);
                document.getElementById('editar-agendamento-erro').textContent = 'Erro de conexão';
            }
        });
    }
    
    if (btnFecharEditar) {
        btnFecharEditar.addEventListener('click', () => {
            document.getElementById('modal-editar-agendamento').style.display = 'none';
        });
    }
    
    // Event listener para modal de pagamento
    const btnFecharPagamento = document.getElementById('fechar-modal-pagamento');
    if (btnFecharPagamento) {
        btnFecharPagamento.addEventListener('click', () => {
            document.getElementById('modal-pagamento').style.display = 'none';
        });
    }
}

function carregarCortesNoSelect() {
    fetch('/api/cortes/')
        .then(res => res.json())
        .then(cortes => {
            const select = document.getElementById('agendamento-corte');
            if (!select) return;
            
            // Limpar opções existentes (exceto a primeira)
            select.innerHTML = '<option value="">Selecione o corte</option>';
            
            cortes.forEach(corte => {
                const option = document.createElement('option');
                option.value = corte.id;
                option.textContent = `${corte.nome} - R$ ${Number(corte.preco).toFixed(2)}`;
                option.dataset.preco = corte.preco;
                option.dataset.nome = corte.nome;
                select.appendChild(option);
            });
        })
        .catch(console.error);
}

function selecionarCorte() {
    const select = document.getElementById('agendamento-corte');
    const selectedOption = select.options[select.selectedIndex];
    
    if (selectedOption.value) {
        corteSelecionado = {
            id: selectedOption.value,
            nome: selectedOption.dataset.nome,
            preco: parseFloat(selectedOption.dataset.preco)
        };
        valorOriginal = corteSelecionado.preco;
        atualizarResumoValores();
    } else {
        corteSelecionado = null;
        valorOriginal = 0;
        document.getElementById('resumo-valores').style.display = 'none';
    }
}

function controlarVoucherSection() {
    const pagamento = document.getElementById('agendamento-pagamento').value;
    const voucherSection = document.getElementById('voucher-section');
    
    if (pagamento === 'dinheiro') {
        voucherSection.style.display = 'none';
        voucherAplicado = null;
        atualizarResumoValores();
    } else {
        voucherSection.style.display = 'block';
    }
}

function aplicarVoucher() {
    const codigoVoucher = document.getElementById('agendamento-voucher').value.trim();
    
    if (!codigoVoucher) {
        mostrarPopup('Digite um código de voucher válido.', 'erro');
        return;
    }
    
    if (!corteSelecionado) {
        mostrarPopup('Selecione um corte antes de aplicar o voucher.', 'erro');
        return;
    }
    
    fetch('/api/vouchers/validar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ codigo: codigoVoucher })
    })
    .then(res => res.json())
    .then(data => {
        if (data.valido) {
            voucherAplicado = {
                codigo: codigoVoucher,
                porcentagem: data.voucher.porcentagem || 0
            };
            atualizarResumoValores();
            mostrarPopup('Voucher aplicado com sucesso!');
        } else {
            mostrarPopup(data.erro || 'Voucher inválido.', 'erro');
            voucherAplicado = null;
            atualizarResumoValores();
        }
    })
    .catch(() => {
        mostrarPopup('Erro ao validar voucher.', 'erro');
    });
}

function atualizarResumoValores() {
    const resumoDiv = document.getElementById('resumo-valores');
    const valorCorteSpan = document.getElementById('valor-corte');
    const descontoVoucherDiv = document.getElementById('desconto-voucher');
    const valorFinalSpan = document.getElementById('valor-final');
    
    if (!corteSelecionado) {
        resumoDiv.style.display = 'none';
        return;
    }
    
    let desconto = 0;
    if (voucherAplicado && voucherAplicado.porcentagem) {
        desconto = (valorOriginal * voucherAplicado.porcentagem) / 100;
    }
    
    valorFinal = valorOriginal - desconto;
    
    valorCorteSpan.textContent = `Valor do corte: R$ ${valorOriginal.toFixed(2)}`;
    
    if (desconto > 0) {
        descontoVoucherDiv.textContent = `Desconto (${voucherAplicado.porcentagem}%): -R$ ${desconto.toFixed(2)}`;
        descontoVoucherDiv.style.display = 'block';
    } else {
        descontoVoucherDiv.style.display = 'none';
    }
    
    valorFinalSpan.textContent = `Total: R$ ${valorFinal.toFixed(2)}`;
    resumoDiv.style.display = 'block';
}

function limparFormularioAgendamento() {
    corteSelecionado = null;
    voucherAplicado = null;
    valorOriginal = 0;
    valorFinal = 0;
    
    document.getElementById('form-agendamento').reset();
    document.getElementById('resumo-valores').style.display = 'none';
    document.getElementById('agendamento-erro').textContent = '';
}

async function enviarAgendamento(e) {
    e.preventDefault();
    
    if (!corteSelecionado) {
        mostrarPopup('Selecione um corte.', 'erro');
        return;
    }
    
    const agendamentoData = {
        nome_cliente: document.getElementById('agendamento-nome').value,
        tipo_corte: corteSelecionado.nome,
        data: document.getElementById('agendamento-data').value,
        horario: document.getElementById('agendamento-horario').value,
        pagamento: document.getElementById('agendamento-pagamento').value,
        voucher: voucherAplicado ? voucherAplicado.codigo : null,
        valor_corte: valorOriginal,
        desconto_voucher: voucherAplicado ? ((valorOriginal * voucherAplicado.porcentagem) / 100) : 0,
        valor_final: valorFinal
    };
    
    try {
        const resp = await fetch('/api/agendamentos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(agendamentoData)
        });
        
        const data = await resp.json();
        
        if (resp.ok) {
            document.getElementById('modal-agendamento').style.display = 'none';
            carregarAgendamentos();
            mostrarComprovanteAgendamento(agendamentoData);
            limparFormularioAgendamento();
        } else {
            document.getElementById('agendamento-erro').textContent = data.erro || 'Erro ao criar agendamento';
        }
    } catch (error) {
        console.error('Erro:', error);
        document.getElementById('agendamento-erro').textContent = 'Erro de conexão';
    }
}
