/////////////////// hamburger 
hamburger = document.querySelector(".navbar-hamburger");
hamburger.onclick = function() {
    var navmain = document.querySelector('.navbar-main');
    navmain.classList.toggle('active');
}

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

// Function to handle click events on the map
function handleMapClick(event) {
    var lat = event.latlng.lat;
    var lng = event.latlng.lng;

    // Add the clicked coordinates to the polygonCoordinates array
    polygonCoordinates.push([lat, lng]);
    // If a polygon already exists, remove it from the map
    if (polygon) {
        map.removeLayer(polygon);
    }

    // Create a new polygon with the updated coordinates and add it to the map
    polygon = L.polygon(polygonCoordinates, {
        color: dotMapColor,
        fillColor: fillMapColor,
        fillOpacity: fillMapOpacity
    }).addTo(map);
}

// Function to handle the "Undo" button click event
function handleUndoButtonClick() {
    // Remove the last coordinate from the polygonCoordinates array
    polygonCoordinates.pop();

    // If a polygon already exists, remove it from the map
    if (polygon) {
        map.removeLayer(polygon);
    }

    // Create a new polygon with the updated coordinates and add it to the map
    polygon = L.polygon(polygonCoordinates, {
        color: dotMapColor,
        fillColor: fillMapColor,
        fillOpacity: fillMapOpacity
    }).addTo(map);
}

// Function to handle the "Clear" button click event
function handleClearButtonClick() {
    // If a polygon already exists, remove it from the map
    if (polygon) {
        map.removeLayer(polygon);
    }

    polygon = null
    polygonCoordinates = [];

    polygon = L.polygon(polygonCoordinates, {
        color: dotMapColor,
        fillColor: fillMapColor,
        fillOpacity: fillMapOpacity
    }).addTo(map);
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

/////////////////// send polygons to product-list
$(document).on('click', '#view-properties-button', function(e) {
    e.preventDefault();

    // Convert polygonCoordinates to JSON string
    var coordinates = JSON.stringify(polygonCoordinates);

    $.ajax({
        type:'POST',
        url:'{% url 'property_list' %}',
        data: {
            coordinates:coordinates,        
            csrfmiddlewaretoken: '{{csrf_token}}',
            action: 'post'
        },

        success: function(response) {
            console.log('Coordinates sent to Django');
            if (response.redirect_url) {
                var redirectURL = '/property/property-list/?coordinates=' + encodeURIComponent(coordinates);
                window.location.href = redirectURL;
            }
        },

        error: function(xhr, errmsg, err) {
            console.error('Error sending coordinates to Django');
        }
    });
});