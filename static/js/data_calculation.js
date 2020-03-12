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
    let data = await get_data();
    await console.log(data);
    count = 0;

    for (date in data) {
        count += 1;
        await console.log(data[date]);

    }
    await console.log(count);
}

