function graphsettings(data){
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: ['January', 'February', 'March'],
            datasets: [{
                label: 'Confirmed Cases',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: [500, 7000, 30]
            }]
        },

        // Configuration options go here
        options: {}
    });
}
graphsettings();