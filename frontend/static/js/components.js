function loadLayoutComponents() {
    const layoutHTML = `
        <nav class="bg-white shadow-md">
            <div class="flex items-center justify-between px-6 py-2">
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
                            <span id="user-avatar">U</span>
                        </div>
                        <div>
                            <p class="text-sm font-semibold text-gray-800" id="header-user-name">User</p>
                            <p class="text-xs text-gray-500" id="header-user-role">Role</p>
                        </div>
                    </div>

                    <button id="user-menu-button" class="flex md:hidden w-10 h-10 bg-blue-600 rounded-full items-center justify-center text-white font-bold focus:outline-none">
                        <span id="user-avatar-mobile">U</span>
                    </button>

                    <div id="user-menu-dropdown" class="hidden absolute right-6 top-16 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                        <div class="px-4 py-2 border-b border-gray-200">
                            <p class="text-sm font-semibold text-gray-800" id="header-user-name-mobile">User</p>
                            <p class="text-xs text-gray-500" id="header-user-role-mobile">Role</p>
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
        
        <div class="flex flex-1 overflow-hidden">
            <div id="sidebar-overlay" class="hidden fixed inset-0 bg-black opacity-50 lg:hidden z-30"></div>

            <aside id="sidebar" class="fixed lg:relative top-0 left-0 w-64 h-full bg-blue-800 text-white transform -translate-x-full lg:translate-x-0 transition-transform duration-300 ease-in-out z-40 overflow-y-auto">
                <nav class="p-6 space-y-4">
                    <a href="dashboard.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Dashboard</a>
                    <a href="customers.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Customers</a>
                    <a href="payments.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Payments</a>
                    <a href="shops.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Shops</a>
                    <a href="loans.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Loans</a>
                    <a href="subscriptions.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Subscriptions</a>
                    <a href="usage.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Usage Billing</a>
                    <a href="users.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Admin Users</a>
                </nav>
            </aside>
            
            <div class="flex-1 flex flex-col overflow-hidden">
                <main id="main-content" class="flex-1 overflow-auto bg-gray-100"></main>
            </div>
        </div>
    `;

    const wrapper = document.querySelector('.flex.flex-col.h-screen');
    if (wrapper) {
        wrapper.innerHTML = layoutHTML;
    }

    const pageTemplate = document.getElementById('page-content');
    if (pageTemplate) {
        const mainContent = document.getElementById('main-content');
        const content = pageTemplate.content.cloneNode(true);
        mainContent.appendChild(content);
    }
}
