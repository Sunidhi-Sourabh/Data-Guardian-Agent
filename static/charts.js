const riskData = JSON.parse(document.getElementById("risk-data").textContent);
const patternData = JSON.parse(document.getElementById("pattern-data").textContent);

new Chart(document.getElementById('riskChart'), {
    type: 'pie',
    data: {
        labels: Object.keys(riskData),
        datasets: [{
            data: Object.values(riskData),
            backgroundColor: ['#dc3545', '#fd7e14', '#198754', '#6c757d']
        }]
    }
});

new Chart(document.getElementById('patternChart'), {
    type: 'bar',
    data: {
        labels: Object.keys(patternData),
        datasets: [{
            label: 'Matches',
            data: Object.values(patternData),
            backgroundColor: '#0d6efd'
        }]
    },
    options: {
        indexAxis: 'y'
    }
});
