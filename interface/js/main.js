// Arquivo principal para inicialização da aplicação
import { inicializarNavegacao, mostrarTela } from './navigation.js';
import { inicializarUI, toggleSenha, mostrarPopup, abrirModalRemover } from './ui.js';
import { inicializarAuth, verificarSessaoSalva } from './auth.js';
import { carregarVouchers, exibirBotaoAdicionarVoucher, usarVoucher, abrirModalAdicionarVoucher, abrirModalEditarVoucher } from './vouchers.js';
import { carregarCortes } from './cortes.js';
import { carregarAgendamentos, mostrarResumoPagamento, abrirModalEditarAgendamento, inicializarAgendamento, mostrarComprovanteAgendamento } from './agendamentos.js';
import { carregarClientes, atualizarVisibilidadeClientes, exibirBotaoAdicionarCliente, abrirModalAdicionarCliente, abrirModalEditarCliente } from './clientes.js';

// Função principal de inicialização
function inicializarApp() {
    console.log('Inicializando aplicação da barbearia...');
    
    // Torna as funções disponíveis globalmente PRIMEIRO
    window.toggleSenha = toggleSenha;
    window.carregarCortes = carregarCortes;
    window.carregarAgendamentos = carregarAgendamentos;
    window.carregarVouchers = carregarVouchers;
    window.carregarClientes = carregarClientes;
    window.mostrarTela = mostrarTela;
    window.atualizarVisibilidadeClientes = atualizarVisibilidadeClientes;
    window.mostrarPopup = mostrarPopup;    
    window.exibirBotaoAdicionarVoucher = exibirBotaoAdicionarVoucher;
    window.exibirBotaoAdicionarCliente = exibirBotaoAdicionarCliente;
    window.abrirModalRemover = abrirModalRemover;
    window.mostrarResumoPagamento = mostrarResumoPagamento;
    window.mostrarComprovanteAgendamento = mostrarComprovanteAgendamento;
    window.abrirModalEditarAgendamento = abrirModalEditarAgendamento;
    window.usarVoucher = usarVoucher;
    window.abrirModalAdicionarVoucher = abrirModalAdicionarVoucher;
    window.abrirModalEditarVoucher = abrirModalEditarVoucher;
    window.abrirModalAdicionarCliente = abrirModalAdicionarCliente;
    window.abrirModalEditarCliente = abrirModalEditarCliente;   
    inicializarNavegacao();
    inicializarUI();
    inicializarAgendamento();
    
    // Aguarda um pouco para garantir que o DOM esteja totalmente carregado
    setTimeout(() => {
        inicializarAuth();
        
        // Verifica se já está logado (depois que as funções estão disponíveis)
        verificarSessaoSalva();
        
        // Atualiza visibilidade baseada no estado atual
        atualizarVisibilidadeClientes();
        exibirBotaoAdicionarVoucher();
        exibirBotaoAdicionarCliente();
        
        // Carrega a tela inicial baseada no estado de login
        const usuarioLogado = localStorage.getItem('usuario');
        if (usuarioLogado) {
            // Se está logado, mostra a tela de cortes
            mostrarTela('tela-cortes');
            carregarCortes();
        } else {
            // Se não está logado, mostra a tela de login
            mostrarTela('tela-login');
        }
        
        console.log('Aplicação inicializada com sucesso!');
    }, 100);
}

// Inicializa quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', inicializarApp);

// Exporta função principal para uso em outros módulos se necessário
export { inicializarApp };
