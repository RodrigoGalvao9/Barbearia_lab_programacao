// ==================== UTILITÁRIOS DE INTERFACE ====================
// Exporta as funções principais
export { mostrarPopup, toggleSenha, abrirModalRemover, inicializarUI };

let acaoPosPopup = null;

// Função para mostrar popup de mensagem
function mostrarPopup(mensagem, acao = null) {
    const popup = document.getElementById('popup-mensagem');
    const texto = document.getElementById('popup-texto');
    if (popup && texto) {
        texto.textContent = mensagem;
        popup.style.display = 'flex';
        acaoPosPopup = acao;
    }
}

// Configurar eventos de popup
function configurarPopup() {
    const btnFecharPopup = document.getElementById('popup-fechar');
    if (btnFecharPopup) {
        btnFecharPopup.onclick = () => {
            document.getElementById('popup-mensagem').style.display = 'none';
            if (typeof acaoPosPopup === 'function') acaoPosPopup();
            acaoPosPopup = null;
        };
    }
}

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



// Configurar modais gerais
function configurarModais() {
    // Modal de agendamento
    const btnNovoAgendamento = document.getElementById('btn-novo-agendamento');
    const modalAgendamento = document.getElementById('modal-agendamento');
    const fecharModalAgendamento = document.getElementById('fechar-modal-agendamento');

    if (btnNovoAgendamento) {
        btnNovoAgendamento.onclick = () => {
            modalAgendamento.style.display = 'flex';
        };
    }

    if (fecharModalAgendamento) {
        fecharModalAgendamento.onclick = () => {
            modalAgendamento.style.display = 'none';
        };
    }

    // Modal de pagamento
    const fecharModalPagamento = document.getElementById('fechar-modal-pagamento');
    if (fecharModalPagamento) {
        fecharModalPagamento.onclick = () => {
            document.getElementById('modal-pagamento').style.display = 'none';
        };
    }

    // Modal de perfil
    const fecharModalPerfil = document.getElementById('fechar-modal-perfil');
    if (fecharModalPerfil) {
        fecharModalPerfil.onclick = () => {
            document.getElementById('modal-perfil').style.display = 'none';
        };
    }    // Modal de corte
    const fecharModalCorte = document.getElementById('fechar-modal-corte');
    if (fecharModalCorte) {
        fecharModalCorte.onclick = () => {
            document.getElementById('modal-corte').style.display = 'none';
        };
    }
}

// Função de inicialização da UI
function inicializarUI() {
    configurarPopup();
    configurarModais();
    configurarModalRemover();
}

// Configurar modal de remoção
let removerCallback = null;

function abrirModalRemover(msg, callback) {
    const modalRemover = document.getElementById('modal-remover');
    const texto = document.getElementById('texto-modal-remover');
    if (texto) texto.textContent = msg;
    if (modalRemover) modalRemover.style.display = 'flex';
    removerCallback = callback;
}

function configurarModalRemover() {
    const modalRemover = document.getElementById('modal-remover');
    const btnConfirmarRemover = document.getElementById('confirmar-remover');
    const btnCancelarRemover = document.getElementById('cancelar-remover');

    if (btnConfirmarRemover) {
        btnConfirmarRemover.onclick = (e) => {
            e.preventDefault();
            modalRemover.style.display = 'none';
            if (typeof removerCallback === 'function') removerCallback();
            removerCallback = null;
        };
    }

    if (btnCancelarRemover) {        btnCancelarRemover.onclick = (e) => {
            e.preventDefault();
            modalRemover.style.display = 'none';
            removerCallback = null;
        };
    }
}
