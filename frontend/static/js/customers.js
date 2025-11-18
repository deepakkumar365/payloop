checkAuth();

const user = getCurrentUser();

async function loadCustomers() {
    try {
        const customers = await apiRequest('/customers');
        displayCustomers(customers);
    } catch (error) {
        console.error('Error loading customers:', error);
    }
}

function displayCustomers(customers) {
    const tbody = document.getElementById('customers-table');
    
    if (customers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center py-4 text-gray-500">No customers found</td></tr>';
        return;
    }
    
    tbody.innerHTML = customers.map(customer => `
        <tr class="border-b hover:bg-gray-50">
            <td class="py-2 px-4">${customer.name}</td>
            <td class="py-2 px-4">${customer.phone}</td>
            <td class="py-2 px-4">${customer.address || '-'}</td>
            <td class="py-2 px-4"><span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">${customer.collection_cycle}</span></td>
            <td class="py-2 px-4">₹${parseFloat(customer.collection_amount).toFixed(2)}</td>
            <td class="py-2 px-4">
                <span class="px-2 py-1 rounded text-xs ${
                    customer.payment_type === 'LOAN' ? 'bg-cyan-100 text-cyan-800' :
                    customer.payment_type === 'SUBSCRIPTION' ? 'bg-indigo-100 text-indigo-800' :
                    customer.payment_type === 'USAGE_BASED' ? 'bg-pink-100 text-pink-800' :
                    'bg-gray-100 text-gray-800'
                }">
                    ${customer.payment_type || 'Regular'}
                </span>
            </td>
            <td class="py-2 px-4">
                <span class="px-2 py-1 rounded text-xs ${customer.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                    ${customer.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td class="py-2 px-4">
                <button onclick="deleteCustomer(${customer.id})" class="text-red-600 hover:text-red-800 text-sm">Delete</button>
            </td>
        </tr>
    `).join('');
}

function showAddCustomerModal() {
    document.getElementById('customer-modal').classList.remove('hidden');
}

function hideCustomerModal() {
    document.getElementById('customer-modal').classList.add('hidden');
    document.getElementById('customer-form').reset();
}

document.getElementById('customer-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const paymentType = document.getElementById('customer-payment-type').value;
    
    const customerData = {
        name: document.getElementById('customer-name').value,
        phone: document.getElementById('customer-phone').value,
        address: document.getElementById('customer-address').value,
        payment_type: paymentType || null,
        collection_cycle: document.getElementById('customer-cycle').value,
        collection_amount: parseFloat(document.getElementById('customer-amount').value),
        agent_id: user.role === 'admin' ? user.id : user.id
    };
    
    try {
        await apiRequest('/customers', {
            method: 'POST',
            body: JSON.stringify(customerData)
        });
        
        hideCustomerModal();
        loadCustomers();
    } catch (error) {
        alert('Error creating customer: ' + error.message);
    }
});

async function deleteCustomer(id) {
    if (!confirm('Are you sure you want to delete this customer?')) {
        return;
    }
    
    try {
        await apiRequest(`/customers/${id}`, {
            method: 'DELETE'
        });
        loadCustomers();
    } catch (error) {
        alert('Error deleting customer: ' + error.message);
    }
}

loadCustomers();
