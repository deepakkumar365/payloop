checkAuth();

const user = getCurrentUser();
let customers = [];
let usageBillings = [];
let usageRecords = [];
let usageBills = [];
let currentBillingId = null;
let currentBillId = null;

async function loadData() {
    try {
        [customers, usageBillings] = await Promise.all([
            apiRequest('/customers'),
            apiRequest('/usage')
        ]);
        
        populateCustomerDropdown();
        populateUsageRecordDropdown();
        displayUsageBillings();
        loadAllRecordsAndBills();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function populateCustomerDropdown() {
    const select = document.getElementById('usage-customer');
    select.innerHTML = '<option value="">Select Customer</option>' + 
        customers.filter(c => c.payment_type === 'USAGE_BASED').map(c => `<option value="${c.id}">${c.name} - ${c.phone}</option>`).join('');
}

function populateUsageRecordDropdown() {
    const select = document.getElementById('usage-record-billing');
    select.innerHTML = '<option value="">Select Billing</option>' + 
        usageBillings.map(b => `<option value="${b.id}">${b.service_name}</option>`).join('');
}

function displayUsageBillings() {
    const tbody = document.getElementById('usage-billings-table');
    
    if (usageBillings.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-gray-500">No usage billings found</td></tr>';
        return;
    }
    
    tbody.innerHTML = usageBillings.map(billing => {
        const customer = customers.find(c => c.id === billing.customer_id);
        
        return `
            <tr class="border-b hover:bg-gray-50">
                <td class="py-2 px-4">${customer ? customer.name : 'Unknown'}</td>
                <td class="py-2 px-4 font-semibold">${billing.service_name}</td>
                <td class="py-2 px-4">₹${parseFloat(billing.rate_per_unit).toFixed(2)} / ${billing.rate_type}</td>
                <td class="py-2 px-4">${new Date(billing.start_date).toLocaleDateString()}</td>
                <td class="py-2 px-4">
                    <span class="px-2 py-1 rounded text-xs ${billing.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                        ${billing.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td class="py-2 px-4">
                    <button onclick="viewBillingDetails(${billing.id})" class="text-blue-600 hover:text-blue-800 text-sm">View</button>
                </td>
            </tr>
        `;
    }).join('');
}

async function loadAllRecordsAndBills() {
    try {
        let allRecords = [];
        let allBills = [];
        
        for (const billing of usageBillings) {
            try {
                const records = await apiRequest(`/usage/${billing.id}/records`);
                allRecords.push(...records);
            } catch (e) {
                // Continue
            }
            
            try {
                const bills = await apiRequest(`/usage/${billing.id}/bills`);
                allBills.push(...bills);
            } catch (e) {
                // Continue
            }
        }
        
        usageRecords = allRecords;
        usageBills = allBills;
        
        displayUsageRecords();
        displayUsageBills();
    } catch (error) {
        console.error('Error loading records and bills:', error);
    }
}

function displayUsageRecords() {
    const tbody = document.getElementById('usage-records-table');
    
    if (usageRecords.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center py-3 text-gray-500 text-sm">No records found</td></tr>';
        return;
    }
    
    tbody.innerHTML = usageRecords.slice(-20).map(record => {
        const billing = usageBillings.find(b => b.id === record.usage_billing_id);
        
        return `
            <tr class="border-b hover:bg-gray-50">
                <td class="py-2 px-3 text-sm">${billing ? billing.service_name : 'Unknown'}</td>
                <td class="py-2 px-3 text-sm">${new Date(record.usage_date).toLocaleDateString()}</td>
                <td class="py-2 px-3 text-sm font-semibold">${parseFloat(record.quantity_used).toFixed(2)}</td>
            </tr>
        `;
    }).join('');
}

function displayUsageBills() {
    const tbody = document.getElementById('usage-bills-table');
    
    if (usageBills.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center py-3 text-gray-500 text-sm">No bills found</td></tr>';
        return;
    }
    
    tbody.innerHTML = usageBills.map(bill => {
        return `
            <tr class="border-b hover:bg-gray-50">
                <td class="py-2 px-3 text-sm font-mono">${bill.bill_number}</td>
                <td class="py-2 px-3 text-sm font-bold text-blue-600">₹${parseFloat(bill.amount_due).toFixed(2)}</td>
                <td class="py-2 px-3 text-sm">
                    <span class="px-2 py-1 rounded text-xs ${
                        bill.status === 'FULLY_PAID' ? 'bg-green-100 text-green-800' :
                        bill.status === 'PARTIALLY_PAID' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                    }">
                        ${bill.status}
                    </span>
                </td>
                <td class="py-2 px-3 text-sm">
                    <button onclick="showUsagePaymentModal(${bill.id})" class="text-green-600 hover:text-green-800">Pay</button>
                </td>
            </tr>
        `;
    }).join('');
}

async function viewBillingDetails(billingId) {
    try {
        const billing = usageBillings.find(b => b.id === billingId);
        const records = await apiRequest(`/usage/${billingId}/records`);
        const bills = await apiRequest(`/usage/${billingId}/bills`);
        
        const detailHtml = `
            <div class="space-y-4">
                <div>
                    <label class="block text-gray-700 text-sm font-bold">Service:</label>
                    <p class="text-gray-900 font-semibold">${billing.service_name}</p>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-gray-700 text-sm font-bold">Rate:</label>
                        <p class="text-blue-600 font-bold">₹${parseFloat(billing.rate_per_unit).toFixed(2)}</p>
                    </div>
                    <div>
                        <label class="block text-gray-700 text-sm font-bold">Rate Type:</label>
                        <p class="text-gray-900">${billing.rate_type}</p>
                    </div>
                </div>
                <div>
                    <label class="block text-gray-700 text-sm font-bold mb-2">Recent Usage Records (${records.length} total):</label>
                    <div class="space-y-1 max-h-32 overflow-y-auto">
                        ${records.slice(-10).map(r => `
                            <div class="bg-gray-50 p-2 rounded text-xs">
                                <p class="font-semibold">${new Date(r.usage_date).toLocaleDateString()}: ${parseFloat(r.quantity_used).toFixed(2)} units</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div>
                    <label class="block text-gray-700 text-sm font-bold mb-2">Bills (${bills.length} total):</label>
                    <div class="space-y-1 max-h-32 overflow-y-auto">
                        ${bills.map(b => `
                            <div class="bg-gray-50 p-2 rounded text-xs">
                                <p class="font-semibold">${b.bill_number}: ₹${parseFloat(b.amount_due).toFixed(2)} (${b.status})</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        // You could show this in a modal if needed
        console.log('Billing Details:', detailHtml);
        alert('Billing Details loaded. Check console for details.');
    } catch (error) {
        alert('Error loading details: ' + error.message);
    }
}

function showAddUsageModal() {
    document.getElementById('usage-modal').classList.remove('hidden');
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('usage-start-date').value = today;
}

function hideUsageModal() {
    document.getElementById('usage-modal').classList.add('hidden');
    document.getElementById('usage-form').reset();
}

function showAddUsageRecordModal() {
    if (usageBillings.length === 0) {
        alert('Please create a usage billing first');
        return;
    }
    document.getElementById('usage-record-modal').classList.remove('hidden');
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('usage-record-date').value = today;
}

function hideUsageRecordModal() {
    document.getElementById('usage-record-modal').classList.add('hidden');
    document.getElementById('usage-record-form').reset();
}

function showUsagePaymentModal(billId) {
    currentBillId = billId;
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('usage-payment-date').value = today;
    document.getElementById('usage-payment-modal').classList.remove('hidden');
}

function hideUsagePaymentModal() {
    document.getElementById('usage-payment-modal').classList.add('hidden');
    document.getElementById('usage-payment-form').reset();
}

document.getElementById('usage-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const customerId = document.getElementById('usage-customer').value;
    const serviceName = document.getElementById('usage-service').value;
    const rate = document.getElementById('usage-rate').value;
    const rateType = document.getElementById('usage-rate-type').value;
    const startDate = document.getElementById('usage-start-date').value;
    
    if (!customerId) {
        alert('Please select a customer');
        return;
    }
    
    const billingData = {
        customer_id: parseInt(customerId),
        service_name: serviceName,
        rate_per_unit: parseFloat(rate),
        rate_type: rateType,
        start_date: new Date(startDate).toISOString()
    };
    
    try {
        await apiRequest('/usage', {
            method: 'POST',
            body: JSON.stringify(billingData)
        });
        
        hideUsageModal();
        alert('Usage billing created successfully!');
        loadData();
    } catch (error) {
        alert('Error creating usage billing: ' + error.message);
    }
});

document.getElementById('usage-record-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const billingId = document.getElementById('usage-record-billing').value;
    const usageDate = document.getElementById('usage-record-date').value;
    const quantity = document.getElementById('usage-record-quantity').value;
    
    if (!billingId) {
        alert('Please select a billing');
        return;
    }
    
    const billing = usageBillings.find(b => b.id === parseInt(billingId));
    
    const recordData = {
        usage_billing_id: parseInt(billingId),
        customer_id: billing.customer_id,
        usage_date: usageDate,
        quantity_used: parseFloat(quantity)
    };
    
    try {
        await apiRequest(`/usage/${billingId}/records`, {
            method: 'POST',
            body: JSON.stringify(recordData)
        });
        
        hideUsageRecordModal();
        alert('Usage record added successfully!');
        loadData();
    } catch (error) {
        alert('Error adding usage record: ' + error.message);
    }
});

document.getElementById('usage-payment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const amount = document.getElementById('usage-payment-amount').value;
    const paymentDate = document.getElementById('usage-payment-date').value;
    const paymentMode = document.getElementById('usage-payment-mode').value;
    
    if (!currentBillId) {
        alert('Bill not found');
        return;
    }
    
    const bill = usageBills.find(b => b.id === currentBillId);
    
    const paymentData = {
        usage_bill_id: currentBillId,
        customer_id: bill.customer_id,
        amount_paid: parseFloat(amount),
        payment_date: new Date(paymentDate).toISOString(),
        payment_mode: paymentMode
    };
    
    try {
        await apiRequest(`/usage/bills/${currentBillId}/payments`, {
            method: 'POST',
            body: JSON.stringify(paymentData)
        });
        
        hideUsagePaymentModal();
        alert('Payment recorded successfully!');
        loadData();
    } catch (error) {
        alert('Error recording payment: ' + error.message);
    }
});

loadData();
