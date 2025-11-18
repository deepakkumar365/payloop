checkAuth();

const user = getCurrentUser();
let customers = [];
let shops = [];

async function loadData() {
    try {
        [customers, shops] = await Promise.all([
            apiRequest('/customers'),
            apiRequest('/shops')
        ]);
        
        populateCustomerDropdown();
        loadPayments();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function populateCustomerDropdown() {
    const select = document.getElementById('payment-customer');
    select.innerHTML = '<option value="">Select Customer</option>' + 
        customers.map(c => `<option value="${c.id}" data-amount="${c.collection_amount}">${c.name} - ${c.phone}</option>`).join('');
    
    select.addEventListener('change', (e) => {
        const selectedOption = e.target.options[e.target.selectedIndex];
        if (selectedOption.value) {
            document.getElementById('payment-amount').value = selectedOption.dataset.amount;
            populateShopDropdown(parseInt(selectedOption.value));
        }
    });
}

function populateShopDropdown(customerId) {
    const select = document.getElementById('payment-shop');
    const customerShops = shops.filter(s => s.customer_id === customerId);
    
    select.innerHTML = '<option value="">No Shop</option>' + 
        customerShops.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
}

async function loadPayments() {
    try {
        const payments = await apiRequest('/payments?limit=50');
        displayPayments(payments);
    } catch (error) {
        console.error('Error loading payments:', error);
    }
}

function displayPayments(payments) {
    const tbody = document.getElementById('payments-table');
    
    if (payments.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center py-4 text-gray-500">No payments found</td></tr>';
        return;
    }
    
    tbody.innerHTML = payments.map(payment => {
        const customer = customers.find(c => c.id === payment.customer_id);
        const shop = payment.shop_id ? shops.find(s => s.id === payment.shop_id) : null;
        
        return `
            <tr class="border-b hover:bg-gray-50">
                <td class="py-2 px-4">${new Date(payment.payment_date).toLocaleString()}</td>
                <td class="py-2 px-4">${customer ? customer.name : 'Unknown'}</td>
                <td class="py-2 px-4">${shop ? shop.name : '-'}</td>
                <td class="py-2 px-4 font-bold text-green-600">₹${parseFloat(payment.amount).toFixed(2)}</td>
                <td class="py-2 px-4">${payment.notes || '-'}</td>
            </tr>
        `;
    }).join('');
}

document.getElementById('payment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const customerId = document.getElementById('payment-customer').value;
    const shopId = document.getElementById('payment-shop').value;
    const amount = document.getElementById('payment-amount').value;
    const notes = document.getElementById('payment-notes').value;
    
    if (!customerId) {
        alert('Please select a customer');
        return;
    }
    
    const paymentData = {
        customer_id: parseInt(customerId),
        shop_id: shopId ? parseInt(shopId) : null,
        amount: parseFloat(amount),
        notes: notes
    };
    
    try {
        await apiRequest('/payments', {
            method: 'POST',
            body: JSON.stringify(paymentData)
        });
        
        document.getElementById('payment-form').reset();
        alert('Payment collected successfully!');
        loadPayments();
    } catch (error) {
        alert('Error collecting payment: ' + error.message);
    }
});

loadData();
