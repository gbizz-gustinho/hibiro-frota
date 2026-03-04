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