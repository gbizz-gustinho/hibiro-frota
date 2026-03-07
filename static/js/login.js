// =========================================
// static/js/login.js - Scripts específicos da página de Login/Registro
// =========================================

// Função para alternar entre formulários de Login e Cadastro
function toggleForms(showFormId) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm && registerForm) { // Garante que os elementos existem
        loginForm.style.display = (showFormId === 'loginForm'? 'block' : 'none');
        registerForm.style.display = (showFormId === 'registerForm'? 'block' : 'none');

        // Adiciona/remove a classe 'active' para transições CSS
        if (showFormId === 'loginForm') {
            loginForm.classList.add('active');
            registerForm.classList.remove('active');
        } else {
            registerForm.classList.add('active');
            loginForm.classList.remove('active');
        }
    }
}

// Lógica a ser executada quando o DOM estiver completamente carregado (apenas para a página de login)
document.addEventListener('DOMContentLoaded', () => {
    // Event Listeners para alternar forms
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');

    if (showRegisterLink) {
        showRegisterLink.addEventListener('click', function(e) {
            e.preventDefault(); // Previne o comportamento padrão do link
            toggleForms('registerForm');
        });
    }

    if (showLoginLink) {
        showLoginLink.addEventListener('click', function(e) {
            e.preventDefault(); // Previne o comportamento padrão do link
            toggleForms('loginForm');
        });
    }

    // Script para o "olhinho" de mostrar/esconder senha
    document.querySelectorAll('.toggle-password').forEach(function(icon) {
        icon.addEventListener('click', function() {
            var targetId = this.dataset.target;
            var passwordInput = document.getElementById(targetId);
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });

    // Manter o formulário correto (Login ou Cadastro) aberto após um POST ou erro
    // As variáveis {{ request.url_rule.endpoint }} e {{ request.form.nome }} vêm do Jinja2/Flask
    // Esta parte precisa ser renderizada PELO JINJA2 NO HTML.
    // Para evitar que o JS falhe se for carregado direto do arquivo.js (onde {{...}} não existe),
    // vamos renderizar os valores do Flask como variáveis JS aqui.
    
    const currentEndpoint = "{{ request.url_rule.endpoint }}"; // Renderiza 'auth.login' ou 'auth.register'
    const requestMethod = "{{ request.method }}"; // Renderiza 'GET' ou 'POST'
    const requestFormNome = "{{ request.form.nome or '' }}"; // Renderiza o nome se existir, senão string vazia

    const hasFlashedMessages = document.querySelector('.flash-messages-container.alert')!== null;
    let formToDisplay = 'loginForm'; // Padrão é mostrar o login

    // Heurística: se houve um POST para 'auth.register' OU se há mensagens flash e o 'nome' foi postado (indicando tentativa de registro)
    if (
        (currentEndpoint === "auth.register" && requestMethod === "POST") ||
        (hasFlashedMessages && requestFormNome!== '' ) 
    ) {
        formToDisplay = 'registerForm';
    }

    // Aplica a exibição correta dos formulários
    toggleForms(formToDisplay); // A função toggleForms já adiciona a classe 'active'
});