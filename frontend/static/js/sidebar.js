function initSidebar() {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = 'index.html';
        return;
    }

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
    
    const userName = user.full_name || user.username;
    const userRole = user.role.toUpperCase();
    
    // For top header user info
    const headerUserName = document.getElementById('header-user-name'); // This might be in the loaded header
    const headerUserRole = document.getElementById('header-user-role');
    if (headerUserName) headerUserName.textContent = userName;
    if (headerUserRole) headerUserRole.textContent = userRole;
    
    const adminManagementLink = document.getElementById('admin-management-link');
    if (user.role === 'superadmin') {
        if (adminManagementLink) {
            adminManagementLink.classList.remove('hidden');
        }
    }
    
    const userManagementLink = document.getElementById('user-management-link');
    if (user.role === 'admin' || user.role === 'superadmin') {
        if (userManagementLink) {
            userManagementLink.classList.remove('hidden');
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

    // User menu dropdown in header
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

document.addEventListener('DOMContentLoaded', initSidebar);

function handleLogout() {
    logout();
}
