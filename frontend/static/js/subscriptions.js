checkAuth();

const user = getCurrentUser();
let customers = [];
let subscriptions = [];
let bills = [];
let currentBillId = null;

async function loadData() {
    try {
        [customers, subscriptions, bills] = await Promise.all([
            apiRequest('/customers'),
            apiRequest('/subscriptions'),
            apiRequest('/subscriptions/1/bills').catch(() => [])
        ]);
        
        populateCustomerDropdown();
        displaySubscriptions();
        loadAllBills();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function populateCustomerDropdown() {
    const select = document.getElementById('subscription-customer');
    select.innerHTML = '<option value="">Select Customer</option>' + 
        customers.filter(c => c.payment_type === 'SUBSCRIPTION').map(c => `<option value="${c.id}">${c.name} - ${c.phone}</option>`).join('');
}

function displaySubscriptions() {
    const tbody = document.getElementById('subscriptions-table');
    
    if (subscriptions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-gray-500">No subscriptions found</td></tr>';
        return;
    }
    
    tbody.innerHTML = subscriptions.map(sub => {
        const customer = customers.find(c => c.id === sub.customer_id);
        
        return `
            <tr class="border-b hover:bg-gray-50">
                <td class="py-2 px-4">${customer ? customer.name : 'Unknown'}</td>
                <td class="py-2 px-4 font-bold text-blue-600">₹${parseFloat(sub.subscription_amount).toFixed(2)}</td>
                <td class="py-2 px-4"><span class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs">${sub.billing_cycle}</span></td>
                <td class="py-2 px-4">${new Date(sub.start_date).toLocaleDateString()}</td>
                <td class="py-2 px-4">
                    <span class="px-2 py-1 rounded text-xs ${sub.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                        ${sub.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td class="py-2 px-4">
                    <button onclick="viewSubscriptionBills(${sub.id})" class="text-blue-600 hover:text-blue-800 text-sm">View Bills</button>
                </td>
            </tr>
        `;
    }).join('');
}

async function loadAllBills() {
    const tbody = document.getElementById('bills-table');
    tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-gray-500">Loading...</td></tr>';
    
    try {
        const allBills = [];
        for (const sub of subscriptions) {
            try {
                const subBills = await apiRequest(`/subscriptions/${sub.id}/bills`);
                allBills.push(...subBills);
            } catch (e) {
                continue;
            }
        }
        displayBills(allBills);
    } catch (error) {
        console.error('Error loading bills:', error);
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-gray-500">Error loading bills</td></tr>';
    }
}

function displayBills(billsList) {
    const tbody = document.getElementById('bills-table');
    
    if (billsList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-gray-500">No bills found</td></tr>';
        return;
    }
    
    tbody.innerHTML = billsList.map(bill => {
        const customer = customers.find(c => c.id === bill.customer_id);
        const periodStart = new Date(bill.billing_period_start).toLocaleDateString();
        const periodEnd = new Date(bill.billing_period_end).toLocaleDateString();
        
        return `
            <tr class="border-b hover:bg-gray-50">
                <td class="py-2 px-4 font-mono text-sm">${bill.bill_number}</td>
                <td class="py-2 px-4">${customer ? customer.name : 'Unknown'}</td>
                <td class="py-2 px-4 text-xs">${periodStart} - ${periodEnd}</td>
                <td class="py-2 px-4 font-bold text-blue-600">₹${parseFloat(bill.amount_due).toFixed(2)}</td>
                <td class="py-2 px-4 font-bold text-green-600">₹${parseFloat(bill.amount_paid || 0).toFixed(2)}</td>
                <td class="py-2 px-4">
                    <span class="px-2 py-1 rounded text-xs ${
                        bill.status === 'FULLY_PAID' ? 'bg-green-100 text-green-800' :
                        bill.status === 'PARTIALLY_PAID' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                    }">
                        ${bill.status}
                    </span>
                </td>
                <td class="py-2 px-4">
                    <button onclick="showBillPaymentModal(${bill.id})" class="text-green-600 hover:text-green-800 text-sm">Pay</button>
                </td>
            </tr>
        `;
    }).join('');
}

async function viewSubscriptionBills(subscriptionId) {
    try {
        const subBills = await apiRequest(`/subscriptions/${subscriptionId}/bills`);
        displayBills(subBills);
    } catch (error) {
        alert('Error loading bills: ' + error.message);
    }
}

function showAddSubscriptionModal() {
    document.getElementById('subscription-modal').classList.remove('hidden');
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('subscription-start-date').value = today;
}

function hideSubscriptionModal() {
    document.getElementById('subscription-modal').classList.add('hidden');
    document.getElementById('subscription-form').reset();
}

function showBillPaymentModal(billId) {
    currentBillId = billId;
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('bill-payment-date').value = today;
    document.getElementById('bill-payment-modal').classList.remove('hidden');
}

function hideBillPaymentModal() {
    document.getElementById('bill-payment-modal').classList.add('hidden');
    document.getElementById('bill-payment-form').reset();
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadLayout();
    loadData();

    document.getElementById('subscription-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const customerId = document.getElementById('subscription-customer').value;
        const amount = document.getElementById('subscription-amount').value;
        const cycle = document.getElementById('subscription-cycle').value;
        const startDate = document.getElementById('subscription-start-date').value;
        
        if (!customerId) {
            alert('Please select a customer');
            return;
        }
        
        const subscriptionData = {
            customer_id: parseInt(customerId),
            subscription_amount: parseFloat(amount),
            billing_cycle: cycle,
            start_date: new Date(startDate).toISOString()
        };
        
        try {
            await apiRequest('/subscriptions', {
                method: 'POST',
                body: JSON.stringify(subscriptionData)
            });
            
            hideSubscriptionModal();
            alert('Subscription created successfully!');
            loadData();
        } catch (error) {
            alert('Error creating subscription: ' + error.message);
        }
    });

    document.getElementById('bill-payment-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const amount = document.getElementById('bill-payment-amount').value;
        const paymentDate = document.getElementById('bill-payment-date').value;
        const paymentMode = document.getElementById('bill-payment-mode').value;
        
        if (!currentBillId) {
            alert('Bill not found');
            return;
        }
        
        try {
            let bill = null;
            for (const sub of subscriptions) {
                try {
                    const subBills = await apiRequest(`/subscriptions/${sub.id}/bills`);
                    bill = subBills.find(b => b.id === currentBillId);
                    if (bill) break;
                } catch (e) {
                    continue;
                }
            }
            
            if (!bill) {
                alert('Bill not found');
                return;
            }
            
            const paymentData = {
                bill_id: currentBillId,
                customer_id: bill.customer_id,
                amount_paid: parseFloat(amount),
                payment_date: new Date(paymentDate).toISOString(),
                payment_mode: paymentMode
            };
            
            await apiRequest(`/subscriptions/bills/${currentBillId}/payments`, {
                method: 'POST',
                body: JSON.stringify(paymentData)
            });
            
            hideBillPaymentModal();
            alert('Payment recorded successfully!');
            loadData();
        } catch (error) {
            alert('Error recording payment: ' + error.message);
        }
    });
});
