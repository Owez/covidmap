const europe_countries = ['Albania','Andorra','Armenia','Austria','Azerbaijan','Belarus','Belgium','Bosnia','Herzegovina','Bulgaria','Croatia','Cyprus','Czechia','Denmark','Estonia','Finland','France','Georgia','Germany','Greece','Hungary','Iceland','Ireland','Italy','Kazakhstan','Kosovo','Latvia','Liechtenstein','Lithuania','Luxembourg','Malta','Moldova','Monaco','Montenegro','Netherlands','North Macedonia','Macedonia','Norway','Poland','Portugal','Romania','Russia','San Marino','Serbia', 'Slovakia',
'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', 'UK', 'Vatican City', 'Holy See'];
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
        return data}


async function global_numbers() {
    let pd = await get_data();
    let parsed = pd['Data'];
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
console.log(globals_by_date);
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



async function china_graph_gather() {
    let pd = await get_data();
    let parsed = pd['Data'];
    //console.log(parsed)
    let globals_by_date = {};
    for (let [date, countries] of Object.entries(parsed)) {
        globals_by_date[date] = {};
        let totaldeaths=0;
        let totalconfirmed=0;
        let totalrecovered=0;
        for (let [countryName, value] of Object.entries(countries[0])) {
          if (countryName == 'Mainland China' || countryName=='Hong Kong' || countryName=='China'){
                totaldeaths += value['Deaths'];
                totalconfirmed += value['ConfirmedCases'];
                totalrecovered += value['Recovered']
        }}
        globals_by_date[date]=({'Confirmed':totalconfirmed, 'Deaths':totaldeaths, 'Recovered':totalrecovered});
    }
    return globals_by_date}
async function china_graph_data(){
    globaldict = await china_graph_gather();
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


async function europe_graph_gather() {
    let pd = await get_data();
    let parsed = pd['Data'];
    //console.log(parsed)
    let globals_by_date = {};
    for (let [date, countries] of Object.entries(parsed)) {
        globals_by_date[date] = {};
        let totaldeaths=0;
        let totalconfirmed=0;
        let totalrecovered=0;
        for (let [countryName, value] of Object.entries(countries[0])) {
          if (europe_countries.includes(countryName)){
                totaldeaths += value['Deaths'];
                totalconfirmed += value['ConfirmedCases'];
                totalrecovered += value['Recovered']
        }}
        globals_by_date[date]=({'Confirmed':totalconfirmed, 'Deaths':totaldeaths, 'Recovered':totalrecovered});
    }
    return globals_by_date}
async function europe_graph_data(){
    globaldict = await europe_graph_gather();
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

async function us_graph_gather() {
    let pd = await get_data();
    let parsed = pd['Data'];
    //console.log(parsed)
    let globals_by_date = {};
    for (let [date, countries] of Object.entries(parsed)) {
        globals_by_date[date] = {};
        let totaldeaths=0;
        let totalconfirmed=0;
        let totalrecovered=0;
        for (let [countryName, value] of Object.entries(countries[0])) {
          if (countryName == 'US'){
                totaldeaths += value['Deaths'];
                totalconfirmed += value['ConfirmedCases'];
                totalrecovered += value['Recovered']
        }}
        globals_by_date[date]=({'Confirmed':totalconfirmed, 'Deaths':totaldeaths, 'Recovered':totalrecovered});
    }
    console.log(globals_by_date);
    return globals_by_date}
async function us_graph_data(){
    globaldict = await us_graph_gather();
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

