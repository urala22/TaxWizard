document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Tax data visualization
    if (document.getElementById('taxDataChart')) {
        renderTaxDataChart();
    }

    // Error distribution chart
    if (document.getElementById('errorDistributionChart')) {
        renderErrorDistributionChart();
    }

    // Tax optimization chart
    if (document.getElementById('optimizationChart')) {
        renderOptimizationChart();
    }
});

function renderTaxDataChart() {
    const ctx = document.getElementById('taxDataChart').getContext('2d');
    
    // Get data from data attributes
    const chartElement = document.getElementById('taxDataChart');
    const income = parseFloat(chartElement.dataset.income || 0);
    const deductions = parseFloat(chartElement.dataset.deductions || 0);
    const taxableIncome = parseFloat(chartElement.dataset.taxableIncome || 0);
    const taxLiability = parseFloat(chartElement.dataset.taxLiability || 0);
    
    const taxDataChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Income', 'Deductions', 'Taxable Income', 'Tax Liability'],
            datasets: [{
                label: 'Tax Overview',
                data: [income, deductions, taxableIncome, taxLiability],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '$' + context.raw.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function renderErrorDistributionChart() {
    const ctx = document.getElementById('errorDistributionChart').getContext('2d');
    
    // Get data from data attributes
    const chartElement = document.getElementById('errorDistributionChart');
    const highErrors = parseInt(chartElement.dataset.highErrors || 0);
    const mediumErrors = parseInt(chartElement.dataset.mediumErrors || 0);
    const lowErrors = parseInt(chartElement.dataset.lowErrors || 0);
    
    const errorDistributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['High Severity', 'Medium Severity', 'Low Severity'],
            datasets: [{
                data: [highErrors, mediumErrors, lowErrors],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                }
            }
        }
    });
}

function renderOptimizationChart() {
    const ctx = document.getElementById('optimizationChart').getContext('2d');
    
    // Get data from the page
    const optimizationItems = document.querySelectorAll('.optimization-item');
    const labels = [];
    const savings = [];
    
    optimizationItems.forEach(item => {
        labels.push(item.querySelector('.strategy-name').textContent);
        // Extract the number from "$X,XXX.XX" format
        const savingsText = item.querySelector('.potential-savings').textContent;
        const savingsAmount = parseFloat(savingsText.replace(/[^0-9.-]+/g, ''));
        savings.push(savingsAmount);
    });
    
    const optimizationChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Potential Savings ($)',
                data: savings,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y', // This makes the bar chart horizontal
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '$' + context.raw.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}
