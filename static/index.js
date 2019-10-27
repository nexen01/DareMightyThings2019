const FIELDS = ['place_id', 'formatted_address', 'geometry', 'photos'];
const TYPES = ['address'];
let searchQueryCount = 0;
let narrativeQueryCount = 0;

function initMap(geometry) {
    const streetViewService = new google.maps.StreetViewService();

    $('#map').empty();
    $('#streetview').empty();
    const map = new google.maps.Map(
        document.getElementById('map'),
        {
            zoom: 16,
            center: geometry.location
        }
    );
    map.fitBounds(geometry.viewport);

    streetViewService.getPanorama(
        {
            location: geometry.location
        },
        function (streetViewPanoramaData, status) {
            if (status === google.maps.StreetViewStatus.OK) {
                const streetview = new google.maps.StreetViewPanorama(
                    document.getElementById('streetview'),
                    {
                        position: geometry.location
                    }
                );
                map.setStreetView(streetview);
            } else {
                const marker = new google.maps.Marker({
                    position: geometry.location,
                    map: map,
                    title: 'Property'
                });
                $('#streetview').append($("<p></p>").text("Could not find a StreetView for this property."));
            }
        }
    );

    return map;
}

function displayPlace(place, prop_id) {
    console.log(place);
    $('#addressheader').text(place.formatted_address);
    const map = initMap(place.geometry);

    $('#narrative').text('Loading...');
    $('#facts').empty();

    const narrativeQueryID = ++narrativeQueryCount;
    const url = window.location.href + `narrative?prop_id=${prop_id.toString()}`;
    fetch(url).then(function(response) {
        return response.json();
    }).then(function(json) {
        if (narrativeQueryID != narrativeQueryCount) return;
        if ('narrative' in json) {
            $('#narrative').text(json.narrative);
            const list = $("#facts");
            list.empty();
            let bounds = place.geometry.viewport;
            for (let i in json.facts) {
                fact = json.facts[i];
                const entry = $('<li></li>').attr('id', i.toString());
                entry.text(fact.name + " is a " + fact.rating + " star rated establishment located " + fact.distance + " from this property");          
                list.append(entry);
                latLng = {lng: Number(fact.lng), lat: Number(fact.lat)}
                const marker = new google.maps.Marker({
                    position: latLng,
                    map: map
                });
                bounds.extend(latLng)
            }
            map.fitBounds(bounds);
        } else if ('error' in json) {
            $('#narrative').text(json.error);
        }
    });
}

function tree(data) {    
    
}

$(function() {
    console.log("index.js is running!");

    const placesService = new google.maps.places.PlacesService(document.getElementById('placesAttribution'));

    $('#searchbox').on('input', function() {
        const query = encodeURI($(this).val());
        const searchQueryID = ++searchQueryCount;
    
        $("#results").empty();
    
        if (query.length == 0) return;
    
        $("#results").append($("<p></p>").text("Loading..."));
    
        const url = window.location.href + `search?address=${query}`;
        fetch(url).then(function(response) {
            return response.json();
        }).then(function(json) {
            if (searchQueryCount != searchQueryID) return; // dont load the results if the user inputted a more recent query
            $("#results").empty();
            for (let i = 0; i < Math.min(json.properties.length, 10); i++) {
                const property = json.properties[i];
                const fullAddress = property.address + ", " + property.city + ", " + property.state;
                const row = $("<p></p>").attr("class", "row searchresult").text(fullAddress);
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

