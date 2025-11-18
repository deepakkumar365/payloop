document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('error-message');
    
    errorDiv.classList.add('hidden');
    
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch('http://localhost:8000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }
        
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        
        const userResponse = await fetch('http://localhost:8000/api/users/me', {
            headers: {
                'Authorization': `Bearer ${data.access_token}`
            }
        });
        
        const user = await userResponse.json();
        localStorage.setItem('user', JSON.stringify(user));
        
        window.location.href = 'dashboard.html';
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.remove('hidden');
    }
});
