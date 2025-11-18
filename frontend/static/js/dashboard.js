document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    
    loadLayout();

    const user = getCurrentUser();

    fetchDashboardData(user.role);

    function fetchDashboardData(role) {
        // Fetch stats
        apiRequest('/stats/summary')
            .then(data => {
                document.getElementById('total-customers').textContent = data.total_customers;
                document.getElementById('total-shops').textContent = data.total_shops;
                document.getElementById('today-collections').textContent = `₹${data.today_collections.toFixed(2)}`;

                if (role === 'agent') {
                    document.getElementById('stats-label').textContent = 'My Collections';
                    document.getElementById('total-agents').textContent = `₹${data.agent_total_collections.toFixed(2)}`;
                } else {
                    document.getElementById('stats-label').textContent = 'Total Agents';
                    document.getElementById('total-agents').textContent = data.total_agents;
                }
            })
            .catch(error => console.error('Error fetching stats:', error));

        // Fetch recent payments
        apiRequest('/payments/recent')
            .then(data => {
                const recentPaymentsDiv = document.getElementById('recent-payments');
                if (data.length === 0) {
                    recentPaymentsDiv.innerHTML = '<p class="text-gray-500 text-sm">No recent payments.</p>';
                    return;
                }
                recentPaymentsDiv.innerHTML = data.map(p => `
                    <div class="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
                        <div>
                            <p class="font-semibold">${p.customer_name}</p>
                            <p class="text-sm text-gray-500">${new Date(p.payment_date).toLocaleDateString()}</p>
                        </div>
                        <p class="font-bold text-green-600">₹${p.amount.toFixed(2)}</p>
                    </div>
                `).join('');
            })
            .catch(error => {
                console.error('Error fetching recent payments:', error);
                const recentPaymentsDiv = document.getElementById('recent-payments');
                recentPaymentsDiv.innerHTML = '<p class="text-red-500 text-sm">Error loading recent payments.</p>';
            });
    }
});