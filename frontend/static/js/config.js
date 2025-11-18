const API_BASE_URL = 'http://localhost:8000/api';

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
}

function getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function setCurrentUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function logout() {
    removeToken();
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        logout();
        return;
    }
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'An error occurred');
    }
    
    if (response.status === 204) {
        return null;
    }
    
    return await response.json();
}

function checkAuth() {
    if (!getToken()) {
        window.location.href = 'index.html';
    }
}
