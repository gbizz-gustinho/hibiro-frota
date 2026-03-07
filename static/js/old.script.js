document.addEventListener('DOMContentLoaded', () => {
    // Lógica para o menu hambúrguer e sidebar colapsável/expansível
    const hamburgerMenu = document.getElementById('hamburgerMenu');
    const sidebar = document.getElementById('sidebar');

    if (hamburgerMenu && sidebar) {
        hamburgerMenu.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            hamburgerMenu.classList.toggle('active');
        });
    }

    // Lógica para submenus colapsáveis
    const menuItemsWithSubmenu = document.querySelectorAll('.sidebar .has-submenu .menu-item');

    menuItemsWithSubmenu.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault(); // Evita que o link navegue para #
            const parentLi = item.closest('li');
            parentLi.classList.toggle('active'); // Ativa/desativa a classe 'active' no item pai
        });
    });

    // Lógica para fechar a sidebar ao clicar fora (apenas em mobile)
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 1024 && sidebar && hamburgerMenu) { // Apenas para telas menores
            if (!sidebar.contains(e.target) && !hamburgerMenu.contains(e.target) && sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
                hamburgerMenu.classList.remove('active');
            }
        }
    });

    // ALTERAÇÃO 1: Nome do usuário agora é dinâmico pelo Flask. 
    // A linha abaixo foi comentada para não sobrescrever o nome real do banco de dados.
    /*
    const userNameElement = document.getElementById('userName');
    if (userNameElement) {
        userNameElement.textContent = "Admin"; 
    }
    */

    // ALTERAÇÃO 2: Adicionada a lógica de alternância Login/Cadastro (movida do HTML)
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');

    if (showRegisterLink && showLoginLink) {
        showRegisterLink.addEventListener('click', (e) => {
            e.preventDefault();
            loginForm.classList.remove('active');
            registerForm.classList.add('active');
        });

        showLoginLink.addEventListener('click', (e) => {
            e.preventDefault();
            registerForm.classList.remove('active');
            loginForm.classList.add('active');
        });
    }
});

function toggleMenu() {
    const navLinks = document.getElementById('nav-links');
    navLinks.classList.toggle('active');
    
    // Opcional: Animação simples nas barrinhas
    const bars = document.querySelectorAll('.bar');
    bars[0].classList.toggle('rotate1');
    bars[1].classList.toggle('fade');
    bars[2].classList.toggle('rotate2');
}

// =========================================
// static/js/script.js - Scripts Globais (Carregados em todas as páginas)
// =========================================

// Função para alternar o tema (continua sendo global)
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'light'? 'dark' : 'light';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('hibiro-theme-public', newTheme);
    updateThemeToggleIcon(newTheme);
}

// Função para atualizar o ícone do botão de tema (continua sendo global)
function updateThemeToggleIcon(theme) {
    const themeToggleBtn = document.getElementById('themeToggle');
    if (themeToggleBtn) {
        themeToggleBtn.innerHTML = theme === 'dark'? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    }
}

// Lógica principal a ser executada quando o DOM estiver completamente carregado para script.js
document.addEventListener('DOMContentLoaded', () => {
    // Aplica o tema salvo no localStorage ao carregar a página
    const savedTheme = localStorage.getItem('hibiro-theme-public') || 'dark'; // Inicia com DARK como padrão
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeToggleIcon(savedTheme);
    
    const themeToggleBtn = document.getElementById('themeToggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }

    // Script para o menu mobile (site público)
    const mobileMenuIcon = document.querySelector('.mobile-menu-icon');
    const navLinks = document.getElementById('nav-links');

    if (mobileMenuIcon && navLinks) {
        mobileMenuIcon.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            // Opcional: para animar o ícone do hambúrguer, adicione classes específicas
            // mobileMenuIcon.classList.toggle('active'); 
        });

        // Fecha o menu ao clicar em um link (se o menu for overlay/fullscreen)
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuIcon.classList.remove('active');
            });
        });
        // Fecha o menu ao clicar no botão de tema (se ele estiver dentro do menu mobile)
        const themeToggleButtonInMenu = navLinks.querySelector('#themeToggle');
        if (themeToggleButtonInMenu) {
            themeToggleButtonInMenu.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuIcon.classList.remove('active');
            });
        }
    }
});

// Função toggleMenu, se for usada por um onclick no HTML (mobile-menu-icon)
// É melhor ter o event listener acima, mas se você ainda usar onclick, mantenha esta função.
function toggleMenu() {
    const navLinks = document.getElementById('nav-links');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
    // Opcional: Animação simples nas barrinhas
    const bars = document.querySelectorAll('.mobile-menu-icon.bar'); // Ajuste o seletor se necessário
    if (bars.length === 3) {
        bars[0].classList.toggle('rotate1');
        bars[1].classList.toggle('fade');
        bars[2].classList.toggle('rotate2');
    }
}