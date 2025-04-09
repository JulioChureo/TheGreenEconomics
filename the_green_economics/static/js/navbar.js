document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    // Estado del menú desde localStorage
    let isMenuOpen = localStorage.getItem('menuOpen') === 'true';
    
    // Función para actualizar el layout
    function updateLayout() {
        if (isMenuOpen) {
            sidebar.classList.remove('-translate-x-full');
            mainContent.classList.add('md:ml-72', 'ml-0');
        } else {
            sidebar.classList.add('-translate-x-full');
            mainContent.classList.remove('md:ml-72', 'ml-0');
        }
    }
    
    // Función para alternar el menú
    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
        localStorage.setItem('menuOpen', isMenuOpen);
        updateLayout();
    }
    
    // Event listeners
    menuToggle.addEventListener('click', toggleMenu);
    
    // Inicialización adaptativa
    if (window.innerWidth >= 768 && !localStorage.getItem('menuOpen')) {
        isMenuOpen = true; // Estado inicial abierto solo en desktop
    }
    
    updateLayout();
    
    // Ajustar en resize
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            mainContent.classList.remove('ml-0');
        } else {
            mainContent.classList.remove('md:ml-72');
        }
        updateLayout();
    });
});