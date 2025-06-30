// ==================== AUTENTICAÇÃO E GESTÃO DE USUÁRIOS ====================

// Controle de sessão do usuário no frontend
function setUsuarioLogado(usuario, tipo) {
    localStorage.setItem('usuario', usuario);
    localStorage.setItem('tipo', tipo);
    document.getElementById('btn-login').style.display = 'none';
    document.getElementById('usuario-logado').style.display = 'flex';
    document.getElementById('usuario-nome').textContent = usuario;
    window.atualizarVisibilidadeClientes && window.atualizarVisibilidadeClientes();
    window.carregarCortes && window.carregarCortes();
    window.carregarAgendamentos && window.carregarAgendamentos();
    window.carregarClientes && window.carregarClientes();
    window.exibirBotaoAdicionarVoucher && window.exibirBotaoAdicionarVoucher();
    window.exibirBotaoAdicionarCliente && window.exibirBotaoAdicionarCliente();
}

function limparUsuarioLogado() {
    localStorage.removeItem('usuario');
    localStorage.removeItem('tipo');
    document.getElementById('btn-login').style.display = 'inline';
    document.getElementById('usuario-logado').style.display = 'none';
    document.getElementById('usuario-nome').textContent = '';
    window.atualizarVisibilidadeClientes && window.atualizarVisibilidadeClientes();
    window.carregarCortes && window.carregarCortes();
    window.carregarAgendamentos && window.carregarAgendamentos();
    window.carregarClientes && window.carregarClientes();
    window.exibirBotaoAdicionarVoucher && window.exibirBotaoAdicionarVoucher();
    window.exibirBotaoAdicionarCliente && window.exibirBotaoAdicionarCliente();
}

// Função de logout
async function logout() {
    try {
        const resp = await fetch('/api/usuarios/logout', {
            method: 'POST',
            credentials: 'include'
        });
        
        const data = await resp.json();
          if (resp.ok) {
            limparUsuarioLogado();
            window.mostrarTela ? window.mostrarTela('tela-login') : console.log('mostrarTela não disponível');
            window.mostrarPopup ? window.mostrarPopup(data.mensagem || 'Logout realizado com sucesso!') : console.log('Logout realizado');
        } else {
            window.mostrarPopup ? window.mostrarPopup(data.erro || 'Erro ao fazer logout.') : console.log('Erro ao fazer logout');
        }    } catch {
        // Se houver erro, faz logout local mesmo assim
        limparUsuarioLogado();
        window.mostrarTela ? window.mostrarTela('tela-login') : console.log('mostrarTela não disponível');
        window.mostrarPopup ? window.mostrarPopup('Logout realizado localmente.') : console.log('Logout realizado localmente');
    }
}

// ==================== CONFIGURAÇÕES DOS FORMULÁRIOS ====================

// Configurar formulários de login e registro
function configurarFormularios() {
    const formLogin = document.getElementById('form-login');
    const formRegistro = document.getElementById('form-registro');

    // Formulário de login
    if (formLogin) {
        formLogin.onsubmit = async (e) => {
            e.preventDefault();
            const usuario = document.getElementById('login-usuario').value;
            const senha = document.getElementById('login-senha').value;
            const erro = document.getElementById('login-erro');
            erro.textContent = '';
            
            try {
                const resp = await fetch('/api/usuarios/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                    body: JSON.stringify({usuario, senha})
                });
                
                const data = await resp.json();
                
                if (resp.ok) {
                    const tipo = data.dados ? data.dados.tipo : data.tipo;
                    setUsuarioLogado(usuario, tipo);
                    window.mostrarTela && window.mostrarTela('tela-cortes');
                    window.carregarCortes && window.carregarCortes();
                } else {
                    window.mostrarPopup ? window.mostrarPopup(data.erro || 'Usuário ou senha inválidos.') : 
                                          (erro.textContent = data.erro || 'Usuário ou senha inválidos.');
                }
            } catch {
                window.mostrarPopup ? window.mostrarPopup('Erro ao conectar ao servidor.') : 
                                      (erro.textContent = 'Erro ao conectar ao servidor.');
            }
        };
    }

    // Formulário de registro
    if (formRegistro) {
        formRegistro.onsubmit = async (e) => {
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
                
                const data = await resp.json();
                
                if (resp.ok) {
                    const callback = () => window.mostrarTela && window.mostrarTela('tela-login');
                    window.mostrarPopup ? window.mostrarPopup(data.mensagem || 'Usuário registrado com sucesso!', callback) : 
                                          callback();
                } else {
                    erro.textContent = data.erro || 'Erro ao registrar. Tente outro usuário.';
                }
            } catch {
                erro.textContent = 'Erro ao conectar ao servidor.';
            }
        };
    }
}

// Configurar modal de perfil
function configurarPerfilModal() {
    const btnPerfil = document.getElementById('btn-perfil');
    const modalPerfil = document.getElementById('modal-perfil');
    const fecharModalPerfil = document.getElementById('fechar-modal-perfil');
    const formPerfil = document.getElementById('form-perfil');

    // Abrir modal de perfil
    if (btnPerfil) {
        btnPerfil.onclick = async () => {
            document.getElementById('perfil-nome').value = '';
            document.getElementById('perfil-senha').value = '';
            modalPerfil.style.display = 'flex';
            
            // Buscar vouchers do usuário
            const lista = document.getElementById('perfil-vouchers');
            lista.innerHTML = '<li>Carregando...</li>';
            
            try {
                const resp = await fetch('/api/vouchers/meus-vouchers', {
                    headers: {'Accept': 'application/json'},
                    credentials: 'include'
                });
                
                const data = await resp.json();
                
                if (resp.ok) {
                    const vouchers = data.dados || data;
                    if (!Array.isArray(vouchers) || vouchers.length === 0) {
                        const mensagem = data.mensagem || 'Nenhum voucher encontrado.';
                        lista.innerHTML = `<li>${mensagem}</li>`;
                    } else {
                        lista.innerHTML = '';
                        vouchers.forEach(v => {
                            const isVencido = v.validade && new Date(v.validade) < new Date();
                            const status = v.usado ? 'Usado' : isVencido ? 'Vencido' : 'Ativo';
                            const statusClass = v.usado ? 'usado' : isVencido ? 'vencido' : 'ativo';
                            lista.innerHTML += `<li class="voucher-${statusClass}"><strong>${v.codigo}</strong> - ${v.descricao} (${status})</li>`;
                        });
                    }
                } else {
                    lista.innerHTML = `<li>Erro: ${data.erro || 'Erro ao carregar vouchers.'}</li>`;
                }
            } catch {
                lista.innerHTML = '<li>Erro ao conectar ao servidor.</li>';
            }
        };
    }

    // Fechar modal
    if (fecharModalPerfil) {
        fecharModalPerfil.onclick = () => {
            modalPerfil.style.display = 'none';
        };
    }

    // Formulário de perfil
    if (formPerfil) {
        formPerfil.onsubmit = async (e) => {
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
                    credentials: 'include',
                    body: JSON.stringify({usuario, nome, senha})
                });
                
                const data = await resp.json();
                
                if (resp.ok) {
                    modalPerfil.style.display = 'none';
                    window.mostrarPopup ? window.mostrarPopup(data.mensagem || 'Perfil atualizado com sucesso!') : 
                                          console.log('Perfil atualizado com sucesso!');
                } else {
                    window.mostrarPopup ? window.mostrarPopup(data.erro || 'Erro ao atualizar perfil.') : 
                                          console.log('Erro ao atualizar perfil.');
                }
            } catch {
                window.mostrarPopup ? window.mostrarPopup('Erro ao conectar ao servidor.') : 
                                      console.log('Erro ao conectar ao servidor.');
            }
        };    }
}

// Configurar botão de logout
function configurarLogout() {
    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) {
        btnLogout.onclick = logout;
    }
}

// Verificar se já está logado ao carregar
function verificarSessaoSalva() {
    const usuario = localStorage.getItem('usuario');
    const tipo = localStorage.getItem('tipo');
    if (usuario) setUsuarioLogado(usuario, tipo);
}

// Função principal de inicialização da autenticação
function inicializarAuth() {
    configurarFormularios();
    configurarPerfilModal();
    configurarLogout();
}

// Exporta as funções principais
export { setUsuarioLogado, limparUsuarioLogado, logout, verificarSessaoSalva, inicializarAuth };