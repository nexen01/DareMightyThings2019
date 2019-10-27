const FIELDS = ['place_id', 'formatted_address', 'geometry', 'photos'];
const TYPES = ['address'];
let queryCount = 0;

function initMap(geometry) {
    $('#map').empty();
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: geometry.location
    });
    const marker = new google.maps.Marker({
        position: geometry.location,
        map: map,
        title: 'test'
    });
    map.fitBounds(geometry.viewport);
}

function createImage(photos) {
    $('#image').empty();
    if (photos.length == 0) return;
    const photo = photos[0];
    
}

function displayPlace(place, prop_id) {
    $('#usr12').val(place.formatted_address);
    initMap(place.geometry);

    $('#narrative').text('Loading...');

    const url = window.location.href + `narrative?prop_id=${prop_id.toString()}`;
    fetch(url).then(function(response) {
        return response.json();
    }).then(function(json) {
        if ('narrative' in json) {
            $('#narrative').text(json.narrative);
        } else if ('error' in json) {
            $('#narrative').text(json.error);
        }
    });
}

$(function() {
    console.log("index.js is running!");

    const placesService = new google.maps.places.PlacesService(document.getElementById('placesAttribution'));

    $('#usr12').on('input', function() {
        const query = encodeURI($(this).val());
        const queryID = ++queryCount;
    
        $("#results").empty();
    
        if (query.length == 0) return;
    
        $("#results").append($("<p></p>").text("Loading..."));
    
        const url = window.location.href + `search?address=${query}`;
        fetch(url).then(function(response) {
            return response.json();
        }).then(function(json) {
            if (queryCount != queryID) return; // dont load the results if the user inputted a more recent query
            $("#results").empty();
            for (let i = 0; i < Math.min(json.properties.length, 10); i++) {
                const property = json.properties[i];
                let row = $("<tr></tr>").attr("class", "searchresult");
                if (i == 0) row = row.attr('id', 'selected');
                row.append($("<p></p>").text(`Address: ${property.address}`));
                //row.append($("<p></p>").text(`Property ID: ${property.prop_id}`));
                const fullAddress = property.address + ", " + property.city + ", " + property.state;
                row.click(function() {
                    placesService.findPlaceFromQuery(
                        {
                            query: fullAddress,
                            fields: FIELDS
                        },
                        function(places, status) {
                            if (places.length > 0) {
                                displayPlace(places[0], property.prop_id);
                            } else {
                                alert(`Could not find ${fullAddress} on Google Maps`);
                            }
                        }
                    );
                });
                $("#results").append(row);
            }
        });
    });
});

