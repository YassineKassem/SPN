document.addEventListener('DOMContentLoaded', function () {
    // Récupérer les données JSON transmises depuis Flask
    var carOwnerCounts = JSON.parse('{{ car_owner_counts_json | safe }}');

    // Extraire les clés (propriétaires de voitures) et les valeurs (nombre de voitures)
    var labels = Object.keys(carOwnerCounts);
    var data = Object.values(carOwnerCounts);

    // Créer un nouveau graphique à barres avec Chart.js
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Nombre de voitures',
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});
