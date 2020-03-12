async function get_data(){
    let url = '/graphdata';
    const response = await fetch(url, {
          method: 'GET',
          mode: 'cors',
          cache: 'no-cache',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json'
          },
          redirect: 'follow',
          referrerPolicy: 'no-referrer',
        });
        let data = await response.json();
        return data['Data']}

async function global_numbers() {
    let parsed = await get_data();
    //console.log(parsed)
    let globals_by_date = {};
    for (let [date, countries] of Object.entries(parsed)) {
        globals_by_date[date] = {};
        let totaldeaths=0;
        let totalconfirmed=0;
        let totalrecovered=0;
        for (let [countryName, value] of Object.entries(countries[0])) {
            totaldeaths += value['Deaths'];
            totalconfirmed += value['ConfirmedCases'];
            totalrecovered += value['Recovered']
        }
        globals_by_date[date]=({'Confirmed':totalconfirmed, 'Deaths':totaldeaths, 'Recovered':totalrecovered});
    }

return globals_by_date;}

async function dict_to_array(){
    globaldict = await global_numbers();
    confirmed = [];
    deaths = [];
    recovered = [];
    dates = []
    for (item in globaldict){
        confirmed.push(globaldict[item]['Confirmed']);
        deaths.push(globaldict[item]['Deaths']);
        recovered.push(globaldict[item]['Recovered']);
        dates.push(item)
    }
    // console.log(confirmed);
    // console.log(deaths);
    // console.log(recovered);
    datalist =[confirmed, deaths, recovered, dates];
return datalist}


