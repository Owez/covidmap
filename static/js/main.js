function zoomfactor(zoom){
    const factor = 100;
    let endzoom = zoom * factor;
return endzoom;}


var mymap = L.map('mapid').setView([51.505, -0.09], 3);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic25lYWt5a2l3aSIsImEiOiJjazduZWRmc3EwMjMwM2R0N3J0amZoc3NlIn0.18IXK7pkL0TIsvOKGSJaPQ', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'your.mapbox.access.token'
}).addTo(mymap);

var confirmed = L.circle([51.508, -0.11], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: zoomfactor(1)
}).addTo(mymap);


async function get_coords(){
    let url = '/coords';
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
        console.log(data);
        for (country in data['Data']){
            console.log('Country: ' + country + ' Latitude: ' + data['Data'][country]['Latitude'] + ' Longitude: ' + data['Data'][country]['Longitude']);

        }
        return data}





