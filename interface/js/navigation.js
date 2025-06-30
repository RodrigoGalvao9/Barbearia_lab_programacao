// ==================== NAVEGAÇÃO E CONTROLE DE TELAS ====================
// Exporta as funções principais
export { mostrarTela, inicializarNavegacao };

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

// Configuração da navegação
function configurarNavegacao() {
    const navCortes = document.getElementById('nav-cortes');
    const navAgendamentos = document.getElementById('nav-agendamentos');
    const navVouchers = document.getElementById('nav-vouchers');
    const navClientes = document.getElementById('nav-clientes');    if (navCortes) navCortes.addEventListener('click', e => {
        e.preventDefault();
        mostrarTela('tela-cortes');
        window.carregarCortes && window.carregarCortes();
    });

    if (navAgendamentos) navAgendamentos.addEventListener('click', e => {
        e.preventDefault();
        mostrarTela('tela-agendamentos');
        window.carregarAgendamentos && window.carregarAgendamentos();
    });

    if (navVouchers) navVouchers.addEventListener('click', e => {
        e.preventDefault();
        mostrarTela('tela-vouchers');
        window.carregarVouchers && window.carregarVouchers();
    });    if (navClientes) navClientes.addEventListener('click', e => {
        e.preventDefault();
        mostrarTela('tela-clientes');
        window.carregarClientes && window.carregarClientes();
    });
}

// Função principal de inicialização da navegação
function inicializarNavegacao() {
    configurarNavegacao();
    configurarBotoesInterface();
}

// Configuração de botões de interface
function configurarBotoesInterface() {
    const btnLogin = document.getElementById('btn-login');
    const linkParaRegistro = document.getElementById('link-para-registro');
    const linkParaLogin = document.getElementById('link-para-login');

    if (btnLogin) btnLogin.onclick = () => mostrarTela('tela-login');
    if (linkParaRegistro) linkParaRegistro.onclick = (e) => { e.preventDefault(); mostrarTela('tela-registro'); };
    if (linkParaLogin) linkParaLogin.onclick = (e) => { e.preventDefault(); mostrarTela('tela-login'); };
}