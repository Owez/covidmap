function zoomfactor(zoom){
    const factor = 100;
    let endzoom = zoom * factor;
return endzoom;}






var mymap = L.map('mapid').setView([41.153332, 20.168331], 3);
const accesskey = 'pk.eyJ1Ijoic25lYWt5a2l3aSIsImEiOiJjazduZWRmc3EwMjMwM2R0N3J0amZoc3NlIn0.18IXK7pkL0TIsvOKGSJaPQ'
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + accesskey, {
    attribution: 'CovidMap ©',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: accesskey
}).addTo(mymap);

get_coords();


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
           // console.log('Country: ' + country + ' Latitude: ' + data['Data'][country]['Latitude'] + ' Longitude: ' + data['Data'][country]['Longitude']);
              areascheme(parseInt(data['Data'][country]['Latitude']), parseInt(data['Data'][country]['Longitude']), country);
        }
        return data}

function areascheme(lat, lng, country) {
    var confirmed = L.circle([lat, lng], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: zoomfactor(500)
    }).addTo(mymap);
    confirmed.bindPopup(country)
}

