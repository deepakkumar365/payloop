checkAuth();

const user = getCurrentUser();
let customers = [];

async function loadData() {
    try {
        [customers] = await Promise.all([
            apiRequest('/customers')
        ]);
        loadShops();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

async function loadShops() {
    try {
        const shops = await apiRequest('/shops');
        displayShops(shops);
    } catch (error) {
        console.error('Error loading shops:', error);
    }
}

function displayShops(shops) {
    const tbody = document.getElementById('shops-table');
    
    if (shops.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-gray-500">No shops found</td></tr>';
        return;
    }
    
    tbody.innerHTML = shops.map(shop => {
        const customer = shop.customer_id ? customers.find(c => c.id === shop.customer_id) : null;
        
        return `
            <tr class="border-b hover:bg-gray-50">
                <td class="py-2 px-4">${shop.name}</td>
                <td class="py-2 px-4">${shop.phone || '-'}</td>
                <td class="py-2 px-4">${shop.address || '-'}</td>
                <td class="py-2 px-4">${customer ? customer.name : '-'}</td>
                <td class="py-2 px-4">
                    <span class="px-2 py-1 rounded text-xs ${shop.is_direct_payer ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'}">
                        ${shop.is_direct_payer ? 'Yes' : 'No'}
                    </span>
                </td>
                <td class="py-2 px-4">
                    <span class="px-2 py-1 rounded text-xs ${shop.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                        ${shop.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td class="py-2 px-4">
                    <button onclick="deleteShop(${shop.id})" class="text-red-600 hover:text-red-800 text-sm">Delete</button>
                </td>
            </tr>
        `;
    }).join('');
}

function showAddShopModal() {
    const select = document.getElementById('shop-customer');
    select.innerHTML = '<option value="">No Customer</option>' + 
        customers.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    
    document.getElementById('shop-modal').classList.remove('hidden');
}

function hideShopModal() {
    document.getElementById('shop-modal').classList.add('hidden');
    document.getElementById('shop-form').reset();
}

document.getElementById('shop-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const customerId = document.getElementById('shop-customer').value;
    
    const shopData = {
        name: document.getElementById('shop-name').value,
        phone: document.getElementById('shop-phone').value,
        address: document.getElementById('shop-address').value,
        customer_id: customerId ? parseInt(customerId) : null,
        is_direct_payer: document.getElementById('shop-direct-payer').checked
    };
    
    try {
        await apiRequest('/shops', {
            method: 'POST',
            body: JSON.stringify(shopData)
        });
        
        hideShopModal();
        loadShops();
    } catch (error) {
        alert('Error creating shop: ' + error.message);
    }
});

async function deleteShop(id) {
    if (!confirm('Are you sure you want to delete this shop?')) {
        return;
    }
    
    try {
        await apiRequest(`/shops/${id}`, {
            method: 'DELETE'
        });
        loadShops();
    } catch (error) {
        alert('Error deleting shop: ' + error.message);
    }
}

loadData();
