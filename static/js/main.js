var map = new ol.map({
    target: 'map',
    layers: [
        new ol.layer.Title({
            source: new ol.source.OSM()
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([37.41, 8.82]),
        zoom: 4
    })
});