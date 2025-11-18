checkAuth();

const user = getCurrentUser();

if (user.role !== 'superadmin') {
    alert('Access denied. Superadmin only.');
    window.location.href = 'dashboard.html';
}

let currentEditAdminId = null;
let currentPasswordAdminId = null;

async function loadAdmins() {
    try {
        const admins = await apiRequest('/users/admins/list');
        displayAdmins(admins);
    } catch (error) {
        console.error('Error loading admins:', error);
    }
}

function displayAdmins(admins) {
    const tbody = document.getElementById('admins-table');
    
    if (admins.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-gray-500">No admins found</td></tr>';
        return;
    }
    
    tbody.innerHTML = admins.map(a => {
        const createdAt = new Date(a.created_at).toLocaleDateString();
        return `
        <tr class="border-b hover:bg-gray-50">
            <td class="py-2 px-4">${a.username}</td>
            <td class="py-2 px-4">${a.email}</td>
            <td class="py-2 px-4">${a.full_name || '-'}</td>
            <td class="py-2 px-4">
                <span class="px-2 py-1 rounded text-xs ${a.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                    ${a.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td class="py-2 px-4">${createdAt}</td>
            <td class="py-2 px-4 space-x-2">
                <button onclick="showEditAdminModal(${a.id})" class="text-blue-600 hover:text-blue-800 text-sm">Edit</button>
                <button onclick="showPasswordModal(${a.id})" class="text-yellow-600 hover:text-yellow-800 text-sm">Change Password</button>
                ${a.id !== user.id ? `<button onclick="deleteAdmin(${a.id})" class="text-red-600 hover:text-red-800 text-sm">Delete</button>` : ''}
            </td>
        </tr>
        `;
    }).join('');
}

function showAddAdminModal() {
    currentEditAdminId = null;
    document.getElementById('modal-title').textContent = 'Add Admin';
    document.getElementById('admin-username').disabled = false;
    document.getElementById('password-field').style.display = 'block';
    document.getElementById('admin-form').reset();
    document.getElementById('admin-modal').classList.remove('hidden');
}

function closeAdminModal() {
    document.getElementById('admin-modal').classList.add('hidden');
    document.getElementById('admin-form').reset();
    currentEditAdminId = null;
}

async function showEditAdminModal(adminId) {
    try {
        const admin = await apiRequest(`/users/admins/${adminId}`);
        currentEditAdminId = adminId;
        
        document.getElementById('edit-email').value = admin.email;
        document.getElementById('edit-fullname').value = admin.full_name || '';
        document.getElementById('edit-status').value = admin.is_active ? 'true' : 'false';
        
        document.getElementById('edit-modal').classList.remove('hidden');
    } catch (error) {
        alert('Error loading admin details: ' + error.message);
    }
}

function closeEditModal() {
    document.getElementById('edit-modal').classList.add('hidden');
    currentEditAdminId = null;
}

function showPasswordModal(adminId) {
    currentPasswordAdminId = adminId;
    document.getElementById('password-form').reset();
    document.getElementById('password-modal').classList.remove('hidden');
}

function closePasswordModal() {
    document.getElementById('password-modal').classList.add('hidden');
    currentPasswordAdminId = null;
}

document.getElementById('admin-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const adminData = {
        username: document.getElementById('admin-username').value,
        email: document.getElementById('admin-email').value,
        full_name: document.getElementById('admin-fullname').value,
        password: document.getElementById('admin-password').value,
        role: 'admin'
    };
    
    try {
        await apiRequest('/users', {
            method: 'POST',
            body: JSON.stringify(adminData)
        });
        
        closeAdminModal();
        loadAdmins();
        alert('Admin created successfully');
    } catch (error) {
        alert('Error creating admin: ' + error.message);
    }
});

document.getElementById('edit-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!currentEditAdminId) {
        alert('No admin selected');
        return;
    }
    
    const updateData = {
        email: document.getElementById('edit-email').value,
        full_name: document.getElementById('edit-fullname').value,
        is_active: document.getElementById('edit-status').value === 'true'
    };
    
    try {
        await apiRequest(`/users/admins/${currentEditAdminId}`, {
            method: 'PUT',
            body: JSON.stringify(updateData)
        });
        
        closeEditModal();
        loadAdmins();
        alert('Admin updated successfully');
    } catch (error) {
        alert('Error updating admin: ' + error.message);
    }
});

document.getElementById('password-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!currentPasswordAdminId) {
        alert('No admin selected');
        return;
    }
    
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    if (newPassword !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }
    
    const passwordData = {
        current_password: '',
        new_password: newPassword
    };
    
    try {
        await apiRequest(`/users/admins/${currentPasswordAdminId}/password`, {
            method: 'PUT',
            body: JSON.stringify(passwordData)
        });
        
        closePasswordModal();
        alert('Password changed successfully');
    } catch (error) {
        alert('Error changing password: ' + error.message);
    }
});

async function deleteAdmin(id) {
    if (!confirm('Are you sure you want to delete this admin?')) {
        return;
    }
    
    try {
        await apiRequest(`/users/admins/${id}`, {
            method: 'DELETE'
        });
        loadAdmins();
        alert('Admin deleted successfully');
    } catch (error) {
        alert('Error deleting admin: ' + error.message);
    }
}

loadAdmins();
