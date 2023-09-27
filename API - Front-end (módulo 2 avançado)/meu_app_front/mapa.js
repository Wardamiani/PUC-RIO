/*
  --------------------------------------------------------------------------------------
  API externa 2 - Mapa
  --------------------------------------------------------------------------------------
*/

let map;

async function initMap() {

    const position = { lat: -25.4284, lng: -49.2733 };

    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

    map = new Map(document.getElementById("map"), {
        zoom: 14,
        center: position,
        mapId: "DEMO_MAP_ID",
      });

    new google.maps.Marker({
        map: map,
        position: position,
        title: "Hotel",
        label: "H",
        animation: google.maps.Animation.DROP,        
    });

    new google.maps.TrafficLayer({map});   
     
    const bikeLayer = new google.maps.BicyclingLayer();

    bikeLayer.setMap(map);
}

initMap();



