async function get_data(){
    let url = '/data';
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
        var data = await response.json();
        return data['Data']}

async function global_numbers(){
    let data = await get_data();
    let total_deaths = 0;
    let total_confirmed = 0;
    let total_recovered = 0;
    let count = 0;
    console.log(data);
    for (country in data){
        total_deaths += data[country]['deaths'];
        total_confirmed += data[country]['confirmed'];
        total_recovered += data[country]['recovered'];

        console.log('Country: ' + country + ' Deaths: ' + data[country]['deaths'] + ' Recovered: ' + data[country]['recovered'] + ' Confirmed: ' + data[country]['confirmed'] );
    }
    console.log('Total Deaths: ' + total_deaths);
    console.log('Total Confirmed: ' + total_confirmed);
    console.log('Total Recovered: ' + total_recovered);
    total_stats =
}
