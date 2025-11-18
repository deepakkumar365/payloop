function loadLayout() {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = 'index.html';
        return;
    }

    loadLayoutComponents();
    initializeLayout(user);
}

function initializeLayout(user) {
    const userName = user.full_name || user.username;
    const userRole = user.role.toUpperCase();
    const userInitial = userName.charAt(0).toUpperCase();

    document.getElementById('user-avatar').textContent = userInitial;
    document.getElementById('user-avatar-mobile').textContent = userInitial;
    document.getElementById('header-user-name').textContent = userName;
    document.getElementById('header-user-role').textContent = userRole;
    document.getElementById('header-user-name-mobile').textContent = userName;
    document.getElementById('header-user-role-mobile').textContent = userRole;

    const hamburger = document.getElementById('hamburger-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (hamburger && sidebar) {
        hamburger.addEventListener('click', () => {
            sidebar.classList.toggle('translate-x-0');
            overlay.classList.toggle('hidden');
        });

        if (overlay) {
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('translate-x-0');
                overlay.classList.add('hidden');
            });
        }
    }

    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 768) {
                sidebar.classList.remove('translate-x-0');
                overlay.classList.add('hidden');
            }
        });
    });

    const userMenuButton = document.getElementById('user-menu-button');
    const userMenuDropdown = document.getElementById('user-menu-dropdown');

    if (userMenuButton && userMenuDropdown) {
        userMenuButton.addEventListener('click', (event) => {
            event.stopPropagation();
            userMenuDropdown.classList.toggle('hidden');
        });

        document.addEventListener('click', (event) => {
            if (!userMenuButton.contains(event.target)) {
                userMenuDropdown.classList.add('hidden');
            }
        });
    }
}

function handleLogout() {
    removeToken();
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', loadLayout);
