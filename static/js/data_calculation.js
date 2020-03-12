async function get_data(){
    let url = '/totaldata';
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
    console.log(globals_by_date);

return globals_by_date;}


