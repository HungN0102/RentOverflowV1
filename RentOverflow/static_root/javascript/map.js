/////////////////// map
let dotMapColor = '#2e8a96'
let fillMapColor = '#45a4b1'
let fillMapOpacity= 0.5

var map = L.map('map').setView([51.505, -0.09], 8);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


var polygon = null;
var polygonCoordinates = [];
var markerGroup = L.layerGroup().addTo(map);


// Function to handle click events on the map
function handleMapClick(event) {
    var lat = event.latlng.lat;
    var lng = event.latlng.lng;

    // Add the clicked coordinates to the polygonCoordinates array
    polygonCoordinates.push([lat, lng]);
    // If a polygon already exists, remove it from the map
    if (polygon) {
        map.removeLayer(polygon);
        markerGroup.clearLayers();
    }

    // Create a new polygon with the updated coordinates and add it to the map
    polygon = L.polygon(polygonCoordinates, {
        color: dotMapColor,
        fillColor: fillMapColor,
        fillOpacity: fillMapOpacity
    }).addTo(map);

    // Add markers at each coordinate of the polygon
    for (var i = 0; i < polygonCoordinates.length; i++) {
        var marker = L.marker(polygonCoordinates[i], {
            icon: L.divIcon({
                className: 'square-marker',
                iconSize: [10, 10],
                html: '<div style="width: 10px; height: 10px; background-color: green;"></div>'
            })
        });
        markerGroup.addLayer(marker);
    } 
}

// Function to handle the "Undo" button click event
function handleUndoButtonClick() {
    // Remove the last coordinate from the polygonCoordinates array
    polygonCoordinates.pop();

    // If a polygon already exists, remove it from the map
    if (polygon) {
        map.removeLayer(polygon);
        markerGroup.clearLayers();
    }

    // Create a new polygon with the updated coordinates and add it to the map
    polygon = L.polygon(polygonCoordinates, {
        color: dotMapColor,
        fillColor: fillMapColor,
        fillOpacity: fillMapOpacity
    }).addTo(map);

    // Add markers at each coordinate of the polygon
    for (var i = 0; i < polygonCoordinates.length; i++) {
        var marker = L.marker(polygonCoordinates[i], {
            icon: L.divIcon({
                className: 'square-marker',
                iconSize: [10, 10],
                html: '<div style="width: 10px; height: 10px; background-color: green;"></div>'
            })
        });
        markerGroup.addLayer(marker);
    } 
}

// Function to handle the "Clear" button click event
function handleClearButtonClick() {
    // If a polygon already exists, remove it from the map
    if (polygon) {
        map.removeLayer(polygon);
        markerGroup.clearLayers();
    }

    polygon = null
    polygonCoordinates = [];

    polygon = L.polygon(polygonCoordinates, {
        color: dotMapColor,
        fillColor: fillMapColor,
        fillOpacity: fillMapOpacity
    }).addTo(map);

    // Add markers at each coordinate of the polygon
    for (var i = 0; i < polygonCoordinates.length; i++) {
        var marker = L.marker(polygonCoordinates[i], {
            icon: L.divIcon({
                className: 'square-marker',
                iconSize: [10, 10],
                html: '<div style="width: 10px; height: 10px; background-color: green;"></div>'
            })
        });
        markerGroup.addLayer(marker);
    }  
}

// Attach the click event handler to the map
map.on('click', handleMapClick);

// Attach the click event undo to the map
var undoButton = document.querySelector('.map-undo')
undoButton.addEventListener('click', handleUndoButtonClick);

// Attach the click event undo to the map
var clearButton = document.querySelector('.map-clear')
clearButton.addEventListener('click', handleClearButtonClick);
document.getElementById('map').style.cursor = 'crosshair'

/////// Function to handle the "View" button click event
function handleViewButtonClick() {
    if (polygonCoordinates.length < 3) {
        alert('Please have atleast 3 points on the map!')
    } else {
        let polygonSearch = document.querySelector('#polygonSearch');
        polygonSearch.value = JSON.stringify(polygonCoordinates)

        let polygonSendButton = document.querySelector('#polygonSendButton');
        polygonSendButton.click()
    }
}

// Attach the click event submit to the map
var submitButton = document.querySelector('.map-submit')
submitButton.addEventListener('click', handleViewButtonClick);