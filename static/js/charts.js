async function chartinit(){
    var speedCanvas = document.getElementById("myChart");



    var dt = await dict_to_array();
    var confirmedlist = dt[0];
    var deathslist = dt[1];
    var recoveredlist = dt[2];
    var dates = dt[3];





    var confirmed = {
        label: "Confirmed Cases",
        data: confirmedlist,
        lineTension: 0,
        fill: false,
        borderColor: 'red'
      };

    var recovered = {
        label: "Recovered Cases",
        data: recoveredlist,
        lineTension: 0,
        fill: false,
      borderColor: 'blue'
      };
    var deaths = {
        label: "Deceased Cases",
        data: deathslist,
        lineTension: 0,
        fill: false,
      borderColor: 'gray'
      };

    var casedata = {
      labels: dates,
      datasets: [confirmed, recovered, deaths]
    };

    var chartOptions = {
      legend: {
        display: true,
        position: 'top',
        labels: {
          boxWidth: 80,
          fontColor: 'black'
        }
      }
    };

    var lineChart = new Chart(speedCanvas, {
      type: 'line',
      data: casedata,
      options: chartOptions
    });}

chartinit()