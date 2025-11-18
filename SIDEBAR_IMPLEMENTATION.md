# Sidebar Navigation Implementation Guide

## Overview
A responsive sidebar navigation with mobile compatibility has been implemented for the PayLoop application. The sidebar includes:
- User information display
- Navigation links to all main pages
- Role-based access to Admin Management (superadmins only)
- User Management (admins)
- Logout button

## Features

### Desktop (lg screens and above)
- Sidebar is always visible on the left
- Full width layout with content on the right

### Mobile (smaller than lg)
- Hamburger menu button appears in the top navbar
- Sidebar slides in from the left (fixed positioning)
- Semi-transparent overlay appears behind sidebar
- Sidebar automatically closes when a link is clicked

## Files Created/Modified

### New Files
- `frontend/static/js/sidebar.js` - Sidebar initialization and event handling
- `frontend/static/html/navbar.html` - Reusable navbar component (reference)
- `SIDEBAR_IMPLEMENTATION.md` - This file

### Modified Files
- `frontend/dashboard.html` - Added sidebar navigation
- `frontend/customers.html` - Added sidebar navigation
- `frontend/users.html` - Added sidebar navigation

## How to Apply to Other Pages

To add the sidebar to any other HTML page (e.g., payments.html, shops.html), follow these steps:

### 1. Replace the opening body structure

**Before:**
```html
<body class="bg-gray-100 min-h-screen">
    <nav class="bg-blue-600 text-white p-4">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold">PayLoop</h1>
            <div class="flex items-center space-x-4">
                <a href="dashboard.html" class="hover:underline">Dashboard</a>
                <button onclick="logout()" class="bg-red-500 hover:bg-red-700 px-4 py-2 rounded text-sm">
                    Logout
                </button>
            </div>
        </div>
    </nav>
    
    <div class="container mx-auto p-4">
```

**After:**
```html
<body class="bg-gray-100 min-h-screen">
    <div class="flex h-screen">
        <div id="sidebar-overlay" class="hidden fixed inset-0 bg-black opacity-50 lg:hidden z-30"></div>
        
        <aside id="sidebar" class="fixed lg:relative top-0 left-0 w-64 h-screen bg-blue-800 text-white transform -translate-x-full lg:translate-x-0 transition-transform duration-300 ease-in-out z-40 overflow-y-auto">
            <div class="p-6 border-b border-blue-700">
                <h1 class="text-2xl font-bold">PayLoop</h1>
                <p class="text-blue-200 text-sm mt-2">Vendor Collection System</p>
            </div>
            
            <nav class="p-6 space-y-4">
                <div class="mb-6 pb-6 border-b border-blue-700">
                    <div class="text-xs text-blue-200 uppercase font-semibold mb-2">User Info</div>
                    <p id="user-name-display" class="font-semibold text-lg"></p>
                    <p id="user-role-display" class="text-blue-300 text-sm"></p>
                </div>
                
                <a href="dashboard.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Dashboard</a>
                <a href="customers.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Customers</a>
                <a href="payments.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Payments</a>
                <a href="shops.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Shops</a>
                <a href="loans.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Loans</a>
                <a href="subscriptions.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Subscriptions</a>
                <a href="usage.html" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition">Usage Billing</a>
                
                <div class="pt-6 border-t border-blue-700">
                    <a href="users.html" id="user-management-link" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition bg-orange-600 hover:bg-orange-700 hidden">Manage Users</a>
                    <a href="users.html" id="admin-management-link" class="sidebar-link block px-4 py-2 rounded hover:bg-blue-700 transition bg-red-600 hover:bg-red-700 hidden mt-2">Manage Admins</a>
                </div>
                
                <div class="pt-6 border-t border-blue-700">
                    <button onclick="handleLogout()" class="w-full bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition">Logout</button>
                </div>
            </nav>
        </aside>
        
        <div class="flex-1 flex flex-col overflow-hidden">
            <nav class="bg-white shadow-md p-4 lg:hidden flex items-center justify-between">
                <button id="hamburger-btn" class="text-gray-600 hover:text-gray-900 focus:outline-none">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
                <h1 class="text-xl font-bold text-gray-800">Page Title Here</h1>
                <div class="w-6"></div>
            </nav>
            
            <main class="flex-1 overflow-auto bg-gray-100">
                <div class="container mx-auto p-4">
```

### 2. Close the main structure properly

**Before:**
```html
    </div>
    
    <script src="static/js/config.js"></script>
    <script src="static/js/page.js"></script>
</body>
</html>
```

**After:**
```html
                </div>
            </main>
        </div>
    </div>
    
    <script src="static/js/config.js"></script>
    <script src="static/js/auth.js"></script>
    <script src="static/js/sidebar.js"></script>
    <script src="static/js/page.js"></script>
</body>
</html>
```

### 3. Update the page title in mobile header
In the mobile navbar, change:
```html
<h1 class="text-xl font-bold text-gray-800">Page Title Here</h1>
```
to the appropriate page title.

## Role-Based Access

### Admin Management Link (Superadmin Only)
- Visible only to superadmins
- Controlled by `id="admin-management-link"`
- Hidden by default, shown automatically via `sidebar.js`

### User Management Link (Admin or Superadmin)
- Visible to admins and superadmins
- Controlled by `id="user-management-link"`
- Hidden by default, shown automatically via `sidebar.js`

## Sidebar Behavior

### Initialization (sidebar.js)
1. Checks user authentication
2. Displays user name and role in sidebar
3. Shows/hides role-specific management links
4. Sets up hamburger menu toggle
5. Closes sidebar automatically on link click on mobile

### Mobile Functionality
- Hamburger button toggles sidebar visibility
- Overlay click closes sidebar
- Sidebar links auto-close on mobile
- Smooth slide-in/out animation

## Styling Details

- **Sidebar Background**: `bg-blue-800`
- **Sidebar Text**: White (`text-white`)
- **Hover Effect**: `hover:bg-blue-700`
- **Links**: Padded with `px-4 py-2`
- **Admin Link**: Red background (`bg-red-600`)
- **User Link**: Orange background (`bg-orange-600`)
- **Responsive**: Uses `lg:` breakpoint (1024px)

## JavaScript Requirements

Ensure these scripts are loaded in this order:
1. `static/js/config.js` - API configuration
2. `static/js/auth.js` - Authentication utilities
3. `static/js/sidebar.js` - Sidebar initialization
4. Page-specific JS (e.g., `static/js/customers.js`)

## Mobile Dimensions

- **Sidebar Width**: 256px (w-64)
- **Breakpoint**: 1024px (lg)
- **Below 1024px**: Mobile view with hamburger menu

## Already Updated Pages

✅ dashboard.html
✅ customers.html
✅ users.html

## Remaining Pages to Update

- payments.html
- shops.html
- loans.html
- subscriptions.html
- usage.html
