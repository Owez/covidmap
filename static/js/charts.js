function generatedatelist(datelist){
    let newlist = [];
    newlist.push('January');
    let months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July',8:'August', 9:'September', 10:'October', 11:'November', 12:'December'};
    for (item in datelist){
        let date = datelist[item];
        let day = date.slice(3,5);
        if (day=='01'){
            let month = parseInt(datelist[item].slice(0,2));
            newlist.push(months[month]);
        }
        else{
            newlist.push("")
        }
    }
    //console.log(newlist);
    return newlist;}


async function global_graph_init(){
    var speedCanvas = document.getElementById("GlobalChart");


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
          boxWidth: 30,
          fontColor: 'blue'
        }
      }
    };

    var lineChart = new Chart(speedCanvas, {
      type: 'line',
      data: casedata,
      options: chartOptions
    });}



async function china_graph_init(){
    var speedCanvas = document.getElementById("ChinaChart");


    var dt = await china_graph_data();
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
          boxWidth: 30,
          fontColor: 'blue'
        }
      }
    };

    var lineChart = new Chart(speedCanvas, {
      type: 'line',
      data: casedata,
      options: chartOptions
    });}
async function europe_graph_init(){
    var speedCanvas = document.getElementById("EuropeChart");


    var dt = await europe_graph_data();
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
          boxWidth: 30,
          fontColor: 'blue'
        }
      }
    };

    var lineChart = new Chart(speedCanvas, {
      type: 'line',
      data: casedata,
      options: chartOptions
    });}
async function us_graph_init(){
    var speedCanvas = document.getElementById("USChart");


    var dt = await us_graph_data();
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
          boxWidth: 30,
          fontColor: 'blue'
        }
      }
    };

    var lineChart = new Chart(speedCanvas, {
      type: 'line',
      data: casedata,
      options: chartOptions
    });}

global_graph_init();
china_graph_init();
us_graph_init();
europe_graph_init();