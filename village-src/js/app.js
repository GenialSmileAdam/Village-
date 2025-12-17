const App = {
    init() {
        this.initTheme();
        this.setupThemeToggle();
    },

    initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
    },

    setupThemeToggle() {
        const toggleBtns = document.querySelectorAll('#themeToggle');
        
        toggleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const current = document.documentElement.getAttribute('data-theme');
                const newTheme = current === 'dark' ? 'light' : 'dark';
                
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
            });
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});