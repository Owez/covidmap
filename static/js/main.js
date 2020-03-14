



function zoomfactor(zoom){
    let factor = 13;
    if (zoom >= 50000) {
        var endzoom = zoom * 13;
    }
    else {
        var endzoom = zoom * 25;
    }
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


function areascheme(lat, lng, province, spot_size) {
    //console.log(spot_size)
    var confirmed = L.circle([lat, lng], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: zoomfactor(spot_size)
    }).addTo(mymap);
    var text2 = (`${province} | Confirmed: ${spot_size}`);
    let hovertext = confirmed.bindPopup(text2);
    hovertext.on('mouseover', function (e) {
    this.openPopup();
    });
    hovertext.on('mouseout', function (e) {
    this.closePopup();
    });

}

async function province_data_grab(){
        let url = '/provincedata';
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
        for (province in data['Data']) {
           // console.log(data['Data'][province]['confirmed']);
             areascheme(data['Data'][province]['latitude'], data['Data'][province]['longitude'], province,  data['Data'][province]['confirmed']);
            //}
        }}

province_data_grab();