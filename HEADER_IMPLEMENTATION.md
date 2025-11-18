# Top Header Implementation Guide

## Overview
A reusable top header component has been created for the PayLoop application. This header is displayed on all pages for larger screens and contains:
- Application brand name and slogan.
- Logged-in user's name and role.

This guide should be used in conjunction with the `SIDEBAR_IMPLEMENTATION.md` guide to create a unified page layout.

## Files Created

- `frontend/static/html/header.html` - The reusable HTML snippet for the header.
- `HEADER_IMPLEMENTATION.md` - This guide.

## How to Apply to Pages

To add the unified layout with the top header and sidebar to any HTML page, follow these steps.

### 1. Replace the opening `<body>` structure

Replace the existing `<body>` content down to the start of your page-specific `<main>` content with the following structure. This combines the top header and the sidebar layout.

```html
<body class="bg-gray-100 min-h-screen">
    <div class="flex flex-col h-screen">
        <!-- Reusable Top Header -->
        <div id="header-container"></div>

        <div class="flex flex-1 overflow-hidden">
            <!-- Sidebar -->
            <div id="sidebar-overlay" class="hidden fixed inset-0 bg-black opacity-50 lg:hidden z-30"></div>
            <aside id="sidebar" class="fixed lg:relative top-0 left-0 w-64 h-full bg-blue-800 text-white transform -translate-x-full lg:translate-x-0 transition-transform duration-300 ease-in-out z-40 overflow-y-auto">
                <!-- Sidebar content from SIDEBAR_IMPLEMENTATION.md -->
            </aside>

            <!-- Main Content -->
            <div class="flex-1 flex flex-col overflow-hidden">
                <!-- Mobile Header -->
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

### 2. Update JavaScript includes

Ensure your page-specific JavaScript file includes the logic to load `header.html`.

```javascript
document.addEventListener('DOMContentLoaded', () => {
    // Load Header
    fetch('static/html/header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-container').innerHTML = data;
        });

    // Your existing page logic...
});
```

The `sidebar.js` script will automatically populate the user details in the header.