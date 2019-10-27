const FIELDS = ['place_id', 'formatted_address', 'geometry.location'];
const TYPES = ['address'];

function initMap(loc) {
    $('#map').empty();
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: loc
    });
    const marker = new google.maps.Marker({
        position: loc,
        map: map,
        title: 'test'
    });
}

function displayPlace(place) {
    $('#usr12').val(place.formatted_address);
    initMap(place.geometry.location);

    $('#narrative').text('Loading...');

    const url = window.location.href + `narrative?place_id=${place.place_id.toString()}`;
    fetch(url).then(function(response) {
        return response.json();
    }).then(function(json) {
        console.log(json);
        if ('narrative' in json) {
            console.log(json.prop_id);
            $('#narrative').text(json.narrative);
        } else if ('error' in json) {
            $('#narrative').text(json.error);
        }
    });
}

function handleOnChange() {
    const query = encodeURI($('#usr12').val());

    $("#results").empty();
    $("#results").append($("<p></p>").text("Loading..."));

    const url = window.location.href + `search?address=${query}`;
    console.log(url);
    fetch(url).then(function(response) {
        return response.json();
    }).then(function(json) {
        console.log(json);
        $("#results").empty();
        for (let i = 0; i < json.properties.length; i++) {
            const property = json.properties[i];
            const row = $("<tr></tr>");
            row.append($("<p></p>").text(`Address: ${property.address}`));
            row.append($("<p></p>").text(`Property ID: ${property.prop_id}`));
            $("#results").append(row);
        }
    });
}

$(function() {
    console.log("index.js is running!");



    /**
    const autocompleteService = new google.maps.places.AutocompleteService();
    const placesService = new google.maps.places.PlacesService(document.getElementById('placesAttribution'));

    const autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('usr12'),
        {
            fields: FIELDS,
            types: TYPES
        }
    );

    autocomplete.addListener('place_changed', function() {
        const place = autocomplete.getPlace();
        console.log(place);
    
        if ('formatted_address' in place) { // if the user selected a complete query
            displayPlace(place);
        } else { // if the user pressed enter prematurely
            autocompleteService.getPlacePredictions(
                {
                    input: place.name,
                    offset: place.name.length,
                    types: TYPES
                },
                function(predictions, status) {
                    if (predictions && predictions.length > 0) {
                        const prediction = predictions[0];
                        placesService.getDetails(
                            {
                                placeId: prediction.place_id,
                                fields: FIELDS
                            },
                            function(predicted_place, status) {
                                console.log(predicted_place);
                                displayPlace(predicted_place);
                            }
                        )
                    } else {
                        $('#map').empty();
                        $('#narrative').text('No results found.');
                    }
                }
            )
        }
    });
    */
});

