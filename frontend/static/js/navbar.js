function initNavbar() {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = 'index.html';
        return;
    }

    const headerContainer = document.getElementById('header-container');
    if (!headerContainer) return;

    const userName = user.full_name || user.username;
    const userRole = user.role.toUpperCase();

    const headerHTML = `
        <nav class="bg-white shadow-md">
            <div class="flex items-center justify-between px-6 py-4">
                <div class="flex items-center space-x-4 flex-1 lg:hidden">
                    <button id="hamburger-btn" class="text-gray-600 hover:text-gray-900 focus:outline-none">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                    </button>
                    <div>
                        <h1 class="text-xl font-bold text-gray-800">PayLoop</h1>
                        <p class="text-xs text-gray-500">Vendor Collection System</p>
                    </div>
                </div>

                <div class="hidden lg:flex items-center">
                    <div>
                        <h1 class="text-2xl font-bold text-gray-800">PayLoop</h1>
                        <p class="text-xs text-gray-500">Vendor Collection System</p>
                    </div>
                </div>

                <div class="flex items-center space-x-6">
                    <div class="hidden md:flex items-center space-x-2">
                        <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                            ${userName.charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <p class="text-sm font-semibold text-gray-800" id="header-user-name">${userName}</p>
                            <p class="text-xs text-gray-500" id="header-user-role">${userRole}</p>
                        </div>
                    </div>

                    <button id="user-menu-button" class="flex md:hidden w-10 h-10 bg-blue-600 rounded-full items-center justify-center text-white font-bold focus:outline-none">
                        ${userName.charAt(0).toUpperCase()}
                    </button>

                    <div id="user-menu-dropdown" class="hidden absolute right-6 top-16 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                        <div class="px-4 py-2 border-b border-gray-200">
                            <p class="text-sm font-semibold text-gray-800" id="header-user-name-mobile">${userName}</p>
                            <p class="text-xs text-gray-500" id="header-user-role-mobile">${userRole}</p>
                        </div>
                        <button onclick="handleLogout()" class="w-full text-left px-4 py-2 text-red-600 hover:bg-gray-100 transition">
                            Logout
                        </button>
                    </div>

                    <button onclick="handleLogout()" class="hidden md:block px-4 py-2 text-red-600 hover:bg-red-50 rounded transition font-semibold">
                        Logout
                    </button>
                </div>
            </div>
        </nav>
    `;

    headerContainer.innerHTML = headerHTML;
}

document.addEventListener('DOMContentLoaded', initNavbar);
