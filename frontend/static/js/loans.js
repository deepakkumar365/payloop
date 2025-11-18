document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadLayout();

    loadLoans();
    populateCustomersDropdown();

    const loanForm = document.getElementById('loan-form');
    if (loanForm) {
        loanForm.addEventListener('submit', handleLoanFormSubmit);
    }
});

function loadLoans() {
    apiRequest('/loans')
    .then(data => {
        const loansTable = document.getElementById('loans-table');
        if (data.length === 0) {
            loansTable.innerHTML = '<tr><td colspan="7" class="text-center py-4">No loans found.</td></tr>';
            return;
        }
        loansTable.innerHTML = data.map(loan => `
            <tr class="border-b">
                <td class="py-2 px-4">${loan.customer_name}</td>
                <td class="py-2 px-4">₹${loan.principal_amount.toFixed(2)}</td>
                <td class="py-2 px-4">₹${loan.total_repayable.toFixed(2)}</td>
                <td class="py-2 px-4">${loan.repayment_frequency}</td>
                <td class="py-2 px-4">${new Date(loan.start_date).toLocaleDateString()}</td>
                <td class="py-2 px-4"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${loan.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">${loan.status}</span></td>
                <td class="py-2 px-4">
                    <button class="text-blue-500 hover:underline text-sm">Details</button>
                </td>
            </tr>
        `).join('');
    })
    .catch(error => console.error('Error fetching loans:', error));
}

function populateCustomersDropdown() {
    const customerSelect = document.getElementById('loan-customer');
    if (!customerSelect) return;

    apiRequest('/customers')
    .then(data => {
        customerSelect.innerHTML = '<option value="">Select Customer</option>';
        data.forEach(customer => {
            customerSelect.innerHTML += `<option value="${customer.id}">${customer.name}</option>`;
        });
    })
    .catch(error => console.error('Error fetching customers:', error));
}

function handleLoanFormSubmit(event) {
    event.preventDefault();
    console.log('Loan form submitted');
    hideLoanModal();
}

function showAddLoanModal() {
    document.getElementById('loan-modal').classList.remove('hidden');
}

function hideLoanModal() {
    document.getElementById('loan-modal').classList.add('hidden');
}

function showLoanDetailModal() {
    document.getElementById('loan-detail-modal').classList.remove('hidden');
}

function hideLoanDetailModal() {
    document.getElementById('loan-detail-modal').classList.add('hidden');
}

function showLoanPaymentModal() {
    document.getElementById('loan-payment-modal').classList.remove('hidden');
}

function hideLoanPaymentModal() {
    document.getElementById('loan-payment-modal').classList.add('hidden');
}