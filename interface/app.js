// Função para alternar telas
function mostrarTela(telaId) {
    document.querySelectorAll('.tela').forEach(tela => tela.style.display = 'none');
    document.getElementById(telaId).style.display = 'block';
    // Atualiza navbar
    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
    if (telaId === 'tela-cortes') document.getElementById('nav-cortes').classList.add('active');
    if (telaId === 'tela-agendamentos') document.getElementById('nav-agendamentos').classList.add('active');
    if (telaId === 'tela-vouchers') document.getElementById('nav-vouchers').classList.add('active');
    if (telaId === 'tela-clientes') document.getElementById('nav-clientes').classList.add('active');
}

// Navegação
const navCortes = document.getElementById('nav-cortes');
const navAgendamentos = document.getElementById('nav-agendamentos');
const navVouchers = document.getElementById('nav-vouchers');
const navClientes = document.getElementById('nav-clientes');

navCortes.addEventListener('click', e => {
    e.preventDefault();
    mostrarTela('tela-cortes');
    carregarCortes();
});
navAgendamentos.addEventListener('click', e => {
    e.preventDefault();
    mostrarTela('tela-agendamentos');
    carregarAgendamentos();
});
navVouchers.addEventListener('click', e => {
    e.preventDefault();
    mostrarTela('tela-vouchers');
    carregarVouchers();
});
if (navClientes) navClientes.addEventListener('click', e => {
    e.preventDefault();
    mostrarTela('tela-clientes');
    carregarClientes();
});

document.addEventListener('DOMContentLoaded', () => {
    mostrarTela('tela-cortes');
    carregarCortes();
});

// Função para carregar cortes da API
function carregarCortes() {
    fetch('/api/cortes/', {headers: {'Accept': 'application/json'}})
        .then(res => res.json())
        .then(cortes => {
            window._cortes = cortes;
            const tbody = document.querySelector('#tabela-cortes tbody');
            const tipo = localStorage.getItem('tipo');
            tbody.innerHTML = '';
            // Exibe coluna de ações apenas para admin
            const thAcoes = document.getElementById('th-acoes-cortes');
            if (thAcoes) thAcoes.style.display = (tipo === 'admin') ? '' : 'none';
            if (!Array.isArray(cortes) || cortes.length === 0) {
                tbody.innerHTML = `<tr><td colspan="${tipo === 'admin' ? 4 : 3}">Nenhum corte cadastrado.</td></tr>`;
                return;
            }
            cortes.forEach((corte, idx) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${corte.nome || ''}</td>
                    <td>${corte.descricao || ''}</td>
                    <td>${corte.preco ? 'R$ ' + Number(corte.preco).toFixed(2) : ''}</td>
                `;
                if (tipo === 'admin') {
                    const tdAcoes = document.createElement('td');
                    tdAcoes.style.whiteSpace = 'nowrap';
                    const btnEditar = document.createElement('button');
                    btnEditar.className = 'btn-editar-corte';
                    btnEditar.textContent = 'Editar';
                    btnEditar.onclick = () => abrirModalEditarCorte(window._cortes[idx]);
                    const btnRemover = document.createElement('button');
                    btnRemover.className = 'btn-remover-corte';
                    btnRemover.textContent = 'Remover';
                    btnRemover.onclick = () => removerCorte(window._cortes[idx].id);
                    tdAcoes.appendChild(btnEditar);
                    tdAcoes.appendChild(btnRemover);
                    tr.appendChild(tdAcoes);
                }
                tbody.appendChild(tr);
            });
            // Botão adicionar corte
            exibirBotaoAdicionarCorte();
        })
        .catch(() => {
            const tbody = document.querySelector('#tabela-cortes tbody');
            tbody.innerHTML = '<tr><td colspan="4">Erro ao carregar cortes.</td></tr>';
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

// Função para carregar agendamentos da API
function carregarAgendamentos() {
    fetch('/api/agendamentos/', {headers: {'Accept': 'application/json'}})
        .then(res => res.json())
        .then(agendamentos => {
            const lista = document.getElementById('agendamentos-lista');
            lista.innerHTML = '';
            const tipo = localStorage.getItem('tipo');
            if (!Array.isArray(agendamentos) || agendamentos.length === 0) {
                lista.innerHTML = '<p>Nenhum agendamento encontrado.</p>';
                return;
            }
            agendamentos.forEach((ag, idx) => {
                const div = document.createElement('div');
                div.className = 'agendamento-item';
                div.innerHTML = `<strong>${ag.nome_cliente || ''}</strong> - ${ag.data || ''} - ${ag.horario || ''}`;
                if (tipo === 'admin') {
                    const btnEditar = document.createElement('button');
                    btnEditar.className = 'btn-editar-agendamento';
                    btnEditar.textContent = 'Editar';
                    btnEditar.onclick = () => abrirModalEditarAgendamento(ag);
                    const btnRemover = document.createElement('button');
                    btnRemover.className = 'btn-remover-agendamento';
                    btnRemover.textContent = 'Remover';
                    btnRemover.onclick = () => removerAgendamento(ag.id);
                    div.appendChild(btnEditar);
                    div.appendChild(btnRemover);
                }
                lista.appendChild(div);
            });
        })
        .catch(() => {
            const lista = document.getElementById('agendamentos-lista');
            lista.innerHTML = '<p>Erro ao carregar agendamentos.</p>';
        });
}
async function removerAgendamento(id) {
    abrirModalRemover('Tem certeza que deseja remover este agendamento?', async () => {
        try {
            const resp = await fetch(`/api/agendamentos/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            if (resp.ok) {
                carregarAgendamentos();
                mostrarPopup('Agendamento removido com sucesso!');
            } else {
                const data = await resp.json();
                mostrarPopup(data.erro || 'Erro ao remover agendamento.');
            }
        } catch {
            mostrarPopup('Erro ao conectar ao servidor.');
        }
    });
}

// Função para carregar vouchers da API
function carregarVouchers() {
    fetch('/api/vouchers/', {headers: {'Accept': 'application/json'}})
        .then(res => res.json())
        .then(vouchers => {
            const lista = document.getElementById('vouchers-lista');
            lista.innerHTML = '';
            if (!Array.isArray(vouchers) || vouchers.length === 0) {
                lista.innerHTML = '<p>Nenhum voucher disponível.</p>';
                return;
            }
            vouchers.forEach(voucher => {
                const div = document.createElement('div');
                div.className = 'voucher-item';
                div.innerHTML = `<strong>${voucher.codigo || ''}</strong> - ${voucher.descricao || ''}`;
                lista.appendChild(div);
            });
        })
        .catch(() => {
            const lista = document.getElementById('vouchers-lista');
            lista.innerHTML = '<p>Erro ao carregar vouchers.</p>';
        });
}

// Carregar clientes com botões admin
function carregarClientes() {
    fetch('/api/clientes/', {headers: {'Accept': 'application/json'}})
        .then(res => res.json())
        .then(clientes => {
            window._clientes = clientes;
            const tbody = document.querySelector('#tabela-clientes tbody');
            const tipo = localStorage.getItem('tipo');
            tbody.innerHTML = '';
            const thAcoes = document.getElementById('th-acoes-clientes');
            if (thAcoes) thAcoes.style.display = (tipo === 'admin') ? '' : 'none';
            if (!Array.isArray(clientes) || clientes.length === 0) {
                tbody.innerHTML = `<tr><td colspan="${tipo === 'admin' ? 4 : 3}">Nenhum cliente cadastrado.</td></tr>`;
                return;
            }
            clientes.forEach((cliente, idx) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${cliente.nome || ''}</td>
                    <td>${cliente.telefone || ''}</td>
                    <td>${cliente.email || ''}</td>
                `;
                if (tipo === 'admin') {
                    const tdAcoes = document.createElement('td');
                    tdAcoes.style.whiteSpace = 'nowrap';
                    const btnEditar = document.createElement('button');
                    btnEditar.className = 'btn-editar-cliente';
                    btnEditar.textContent = 'Editar';
                    // btnEditar.onclick = () => abrirModalEditarCliente(window._clientes[idx]);
                    const btnRemover = document.createElement('button');
                    btnRemover.className = 'btn-remover-cliente';
                    btnRemover.textContent = 'Remover';
                    btnRemover.onclick = () => removerCliente(window._clientes[idx].id);
                    tdAcoes.appendChild(btnEditar);
                    tdAcoes.appendChild(btnRemover);
                    tr.appendChild(tdAcoes);
                }
                tbody.appendChild(tr);
            });
        })
        .catch(() => {
            const tbody = document.querySelector('#tabela-clientes tbody');
            tbody.innerHTML = '<tr><td colspan="4">Erro ao carregar clientes.</td></tr>';
        });
}
async function removerCliente(id) {
    if (!confirm('Tem certeza que deseja remover este cliente?')) return;
    try {
        const resp = await fetch(`/api/clientes/${id}`, {method: 'DELETE'});
        if (resp.ok) {
            carregarClientes();
            mostrarPopup('Cliente removido com sucesso!');
        } else {
            const data = await resp.json();
            mostrarPopup(data.erro || 'Erro ao remover cliente.');
        }
    } catch {
        mostrarPopup('Erro ao conectar ao servidor.');
    }
}

const btnLogin = document.getElementById('btn-login');
const linkParaRegistro = document.getElementById('link-para-registro');
const linkParaLogin = document.getElementById('link-para-login');
const formLogin = document.getElementById('form-login');
const formRegistro = document.getElementById('form-registro');
const formAgendamento = document.getElementById('form-agendamento');
const btnNovoAgendamento = document.getElementById('btn-novo-agendamento');
const modalAgendamento = document.getElementById('modal-agendamento');
const fecharModalAgendamento = document.getElementById('fechar-modal-agendamento');

if (btnLogin) btnLogin.onclick = () => mostrarTela('tela-login');
if (linkParaRegistro) linkParaRegistro.onclick = (e) => { e.preventDefault(); mostrarTela('tela-registro'); };
if (linkParaLogin) linkParaLogin.onclick = (e) => { e.preventDefault(); mostrarTela('tela-login'); };

// Função para alternar visibilidade da senha
function toggleSenha(idInput, btn) {
    const input = document.getElementById(idInput);
    if (input.type === 'password') {
        input.type = 'text';
        btn.innerHTML = '&#128064;';
    } else {
        input.type = 'password';
        btn.innerHTML = '&#128065;';
    }
}

// Controle de sessão do usuário no frontend
// Atualiza tabelas/lists ao logar/deslogar para refletir permissões
function setUsuarioLogado(usuario, tipo) {
    localStorage.setItem('usuario', usuario);
    localStorage.setItem('tipo', tipo);
    document.getElementById('btn-login').style.display = 'none';
    document.getElementById('usuario-logado').style.display = 'flex';
    document.getElementById('usuario-nome').textContent = usuario;
    atualizarVisibilidadeClientes();
    carregarCortes();
    carregarAgendamentos();
    carregarClientes();
}
function limparUsuarioLogado() {
    localStorage.removeItem('usuario');
    localStorage.removeItem('tipo');
    document.getElementById('btn-login').style.display = 'inline';
    document.getElementById('usuario-logado').style.display = 'none';
    document.getElementById('usuario-nome').textContent = '';
    atualizarVisibilidadeClientes();
    carregarCortes();
    carregarAgendamentos();
    carregarClientes();
}

// Ao carregar, verifica se já está logado
window.addEventListener('DOMContentLoaded', () => {
    const usuario = localStorage.getItem('usuario');
    const tipo = localStorage.getItem('tipo');
    if (usuario) setUsuarioLogado(usuario, tipo);
});

// Ajuste no login para salvar sessão no frontend
if (formLogin) formLogin.onsubmit = async (e) => {
    e.preventDefault();
    const usuario = document.getElementById('login-usuario').value;
    const senha = document.getElementById('login-senha').value;
    const erro = document.getElementById('login-erro');
    erro.textContent = '';
    try {
        const resp = await fetch('/api/usuarios/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({usuario, senha})
        });
        if (resp.ok) {
            const data = await resp.json();
            setUsuarioLogado(usuario, data.tipo);
            mostrarTela('tela-cortes');
        } else {
            const data = await resp.json();
            mostrarPopup(data.erro || 'Usuário ou senha inválidos.');
        }
    } catch {
        mostrarPopup('Erro ao conectar ao servidor.');
    }
};

if (formRegistro) formRegistro.onsubmit = async (e) => {
    e.preventDefault();
    const usuario = document.getElementById('registro-usuario').value;
    const senha = document.getElementById('registro-senha').value;
    const confirmarSenha = document.getElementById('registro-confirmar-senha').value;
    const nome = document.getElementById('registro-nome').value;
    const erro = document.getElementById('registro-erro');
    erro.textContent = '';
    if (senha !== confirmarSenha) {
        erro.textContent = 'As senhas não coincidem.';
        return;
    }
    try {
        const resp = await fetch('/api/usuarios/registrar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({usuario, senha, nome})
        });
        if (resp.ok) {
            mostrarTela('tela-login');
        } else {
            erro.textContent = 'Erro ao registrar. Tente outro usuário.';
        }
    } catch {
        erro.textContent = 'Erro ao conectar ao servidor.';
    }
};

if (btnNovoAgendamento) btnNovoAgendamento.onclick = () => {
    modalAgendamento.style.display = 'flex';
};
if (fecharModalAgendamento) fecharModalAgendamento.onclick = () => {
    modalAgendamento.style.display = 'none';
};

let acaoPosPopup = null;

function mostrarPopup(mensagem, acao = null) {
    const popup = document.getElementById('popup-mensagem');
    const texto = document.getElementById('popup-texto');
    if (popup && texto) {
        texto.textContent = mensagem;
        popup.style.display = 'flex';
        acaoPosPopup = acao;
    }
}
const btnFecharPopup = document.getElementById('popup-fechar');
if (btnFecharPopup) btnFecharPopup.onclick = () => {
    document.getElementById('popup-mensagem').style.display = 'none';
    if (typeof acaoPosPopup === 'function') acaoPosPopup();
    acaoPosPopup = null;
};

if (formAgendamento) formAgendamento.onsubmit = async (e) => {
    e.preventDefault();
    const nome_cliente = document.getElementById('agendamento-nome').value;
    const data = document.getElementById('agendamento-data').value;
    const horario = document.getElementById('agendamento-horario').value;
    const voucher = document.getElementById('agendamento-voucher').value;
    const pagamento = document.getElementById('agendamento-pagamento').value;
    const erro = document.getElementById('agendamento-erro');
    erro.textContent = '';
    try {
        const resp = await fetch('/api/agendamentos/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({nome_cliente, data, horario, voucher, pagamento})
        });
        if (resp.ok) {
            modalAgendamento.style.display = 'none';
            carregarAgendamentos();
            // Só mostra tela de pagamento para não-admin e pagamento diferente de dinheiro
            if (localStorage.getItem('tipo') !== 'admin') {
                let agendamento = {nome_cliente, data, horario, voucher, pagamento};
                try {
                    const dataResp = await resp.json();
                    agendamento = {...agendamento, ...dataResp};
                } catch {}
                console.log('Agendamento criado:', agendamento);
                if (agendamento.pagamento && agendamento.pagamento !== 'dinheiro') {
                    mostrarResumoPagamento(agendamento);
                } else {
                    console.log('Pagamento em dinheiro, não exibe modal de pagamento.');
                }
            }
        } else {
            let data;
            try { data = await resp.json(); } catch { data = null; }
            if (resp.status === 401) {
                modalAgendamento.style.display = 'none';
                mostrarPopup(data && data.erro ? data.erro : 'É necessário estar logado para agendar.', () => mostrarTela('tela-login'));
            } else if (data && data.erro) {
                mostrarPopup(data.erro);
            } else {
                mostrarPopup('Erro ao agendar. Verifique os dados.');
            }
        }
    } catch {
        mostrarPopup('Erro ao conectar ao servidor.');
    }
};

// Função para exibir o modal de pagamento (falsa tela)
function mostrarResumoPagamento(agendamento) {
    const modal = document.getElementById('modal-pagamento');
    const resumo = document.getElementById('resumo-pagamento');
    if (!modal || !resumo) return;
    resumo.innerHTML = `
        <strong>Cliente:</strong> ${agendamento.nome_cliente}<br>
        <strong>Data:</strong> ${agendamento.data}<br>
        <strong>Horário:</strong> ${agendamento.horario}<br>
        <strong>Voucher:</strong> ${agendamento.voucher || 'Nenhum'}<br>
        <strong>Pagamento:</strong> ${agendamento.pagamento || 'Não informado'}<br>
        <strong>Status:</strong> <span style="color:#ffb300">Aguardando pagamento</span>
    `;
    modal.style.display = 'flex';
}
const fecharModalPagamento = document.getElementById('fechar-modal-pagamento');
if (fecharModalPagamento) fecharModalPagamento.onclick = () => {
    document.getElementById('modal-pagamento').style.display = 'none';
};

// Logout
const btnLogout = document.getElementById('btn-logout');
if (btnLogout) btnLogout.onclick = async () => {
    await fetch('/api/usuarios/logout', {method: 'POST'});
    limparUsuarioLogado();
    mostrarTela('tela-cortes');
};

// Abrir e fechar modal de perfil
const btnPerfil = document.getElementById('btn-perfil');
const modalPerfil = document.getElementById('modal-perfil');
const fecharModalPerfil = document.getElementById('fechar-modal-perfil');
const formPerfil = document.getElementById('form-perfil');

// Exibir vouchers do usuário logado no modal de perfil
if (btnPerfil) btnPerfil.onclick = async () => {
    document.getElementById('perfil-nome').value = '';
    document.getElementById('perfil-senha').value = '';
    modalPerfil.style.display = 'flex';
    // Buscar vouchers do usuário
    const usuario = localStorage.getItem('usuario');
    const lista = document.getElementById('perfil-vouchers');
    lista.innerHTML = '<li>Carregando...</li>';
    try {
        const resp = await fetch('/api/vouchers/', {headers: {'Accept': 'application/json'}});
        if (resp.ok) {
            const vouchers = await resp.json();
            const meus = vouchers.filter(v => v.usuario === usuario);
            if (meus.length === 0) {
                lista.innerHTML = '<li>Nenhum voucher encontrado.</li>';
            } else {
                lista.innerHTML = '';
                meus.forEach(v => {
                    lista.innerHTML += `<li><strong>${v.codigo}</strong> - ${v.descricao}</li>`;
                });
            }
        } else {
            lista.innerHTML = '<li>Erro ao carregar vouchers.</li>';
        }
    } catch {
        lista.innerHTML = '<li>Erro ao conectar ao servidor.</li>';
    }
};
if (fecharModalPerfil) fecharModalPerfil.onclick = () => {
    modalPerfil.style.display = 'none';
};
if (formPerfil) formPerfil.onsubmit = async (e) => {
    e.preventDefault();
    const nome = document.getElementById('perfil-nome').value;
    const senha = document.getElementById('perfil-senha').value;
    const usuario = localStorage.getItem('usuario');
    const erro = document.getElementById('perfil-erro');
    erro.textContent = '';
    try {
        const resp = await fetch(`/api/usuarios/editar`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({usuario, nome, senha})
        });
        if (resp.ok) {
            modalPerfil.style.display = 'none';
            mostrarPopup('Perfil atualizado com sucesso!');
        } else {
            const data = await resp.json();
            mostrarPopup(data.erro || 'Erro ao atualizar perfil.');
        }
    } catch {
        mostrarPopup('Erro ao conectar ao servidor.');
    }
};

// Modal de adicionar/editar corte (admin)
const modalCorte = document.getElementById('modal-corte');
const formCorte = document.getElementById('form-corte');
const fecharModalCorte = document.getElementById('fechar-modal-corte');
const tituloModalCorte = document.getElementById('titulo-modal-corte');
let corteEditandoId = null;

function abrirModalAdicionarCorte() {
    corteEditandoId = null;
    tituloModalCorte.textContent = 'Adicionar Corte';
    formCorte.reset();
    modalCorte.style.display = 'flex';
}
function abrirModalEditarCorte(corte) {
    corteEditandoId = corte.id;
    tituloModalCorte.textContent = 'Editar Corte';
    document.getElementById('corte-nome').value = corte.nome;
    document.getElementById('corte-descricao').value = corte.descricao;
    document.getElementById('corte-preco').value = corte.preco;
    modalCorte.style.display = 'flex';
}
if (fecharModalCorte) fecharModalCorte.onclick = () => {
    modalCorte.style.display = 'none';
};
if (formCorte) formCorte.onsubmit = async (e) => {
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

// Corrige duplicidade: não redeclara navClientes
// Função para ocultar link/tela clientes para não-admin
function atualizarVisibilidadeClientes() {
    const tipo = localStorage.getItem('tipo');
    const navClientesEl = document.getElementById('nav-clientes');
    const telaClientes = document.getElementById('tela-clientes');
    if (navClientesEl) navClientesEl.style.display = (tipo === 'admin') ? '' : 'none';
    if (telaClientes && tipo !== 'admin') telaClientes.style.display = 'none';
}
window.addEventListener('DOMContentLoaded', atualizarVisibilidadeClientes);
window.addEventListener('storage', atualizarVisibilidadeClientes);
if (navClientes) navClientes.addEventListener('click', e => {
    e.preventDefault();
    if (localStorage.getItem('tipo') !== 'admin') {
        alert('Acesso restrito! Apenas administradores podem acessar a área de clientes.');
        return;
    }
    mostrarTela('tela-clientes');
    carregarClientes();
});
// Modal de confirmação de remoção reutilizável
let removerCallback = null;
const modalRemover = document.getElementById('modal-remover');
const btnConfirmarRemover = document.getElementById('confirmar-remover');
const btnCancelarRemover = document.getElementById('cancelar-remover');
function abrirModalRemover(msg, callback) {
    document.getElementById('texto-modal-remover').textContent = msg;
    modalRemover.style.display = 'flex';
    removerCallback = callback;
}
if (btnConfirmarRemover) btnConfirmarRemover.onclick = (e) => {
    e.preventDefault();
    modalRemover.style.display = 'none';
    if (typeof removerCallback === 'function') removerCallback();
    removerCallback = null;
};
if (btnCancelarRemover) btnCancelarRemover.onclick = (e) => {
    e.preventDefault();
    modalRemover.style.display = 'none';
    removerCallback = null;
};
// Substitui confirm em removerCorte para usar modal
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

// Modal de edição de agendamento (reutiliza modal já existente)
let agendamentoEditandoId = null;
function abrirModalEditarAgendamento(agendamento) {
    agendamentoEditandoId = agendamento.id;
    document.getElementById('editar-agendamento-nome').value = agendamento.nome_cliente;
    document.getElementById('editar-agendamento-data').value = agendamento.data;
    document.getElementById('editar-agendamento-horario').value = agendamento.horario;
    document.getElementById('editar-agendamento-voucher').value = agendamento.voucher || '';
    document.getElementById('editar-agendamento-pagamento').value = agendamento.pagamento || '';
    document.getElementById('modal-editar-agendamento').style.display = 'flex';
}
const formEditarAgendamento = document.getElementById('form-editar-agendamento');
const fecharModalEditarAgendamento = document.getElementById('fechar-modal-editar-agendamento');
if (fecharModalEditarAgendamento) fecharModalEditarAgendamento.onclick = () => {
    document.getElementById('modal-editar-agendamento').style.display = 'none';
};
if (formEditarAgendamento) formEditarAgendamento.onsubmit = async (e) => {
    e.preventDefault();
    const nome_cliente = document.getElementById('editar-agendamento-nome').value;
    const data = document.getElementById('editar-agendamento-data').value;
    const horario = document.getElementById('editar-agendamento-horario').value;
    const voucher = document.getElementById('editar-agendamento-voucher').value;
    const pagamento = document.getElementById('editar-agendamento-pagamento').value;
    const erro = document.getElementById('editar-agendamento-erro');
    erro.textContent = '';
    try {
        const resp = await fetch(`/api/agendamentos/${agendamentoEditandoId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({nome_cliente, data, horario, voucher, pagamento})
        });
        if (resp.ok) {
            document.getElementById('modal-editar-agendamento').style.display = 'none';
            carregarAgendamentos();
            mostrarPopup('Agendamento atualizado com sucesso!');
        } else {
            const data = await resp.json();
            mostrarPopup(data.erro || 'Erro ao atualizar agendamento.');
        }
    } catch {
        mostrarPopup('Erro ao conectar ao servidor.');
    }
};
