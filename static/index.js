function handleSubmit() {
    const address = $('#usr12').val();
    console.log(`Querying with address ${address}...`);
    const url = window.location.href + 'narrative?address=' + address;
    fetch(url).then(function(response) {
        return response.json();
    }).then(function(json) {
        $('#narrative').text(json.narrative);
        $('#gmaps-view').empty();
        $('#gmaps-view').append($(
            `<iframe src=${json.maps_src_url} width='600' height='450' allowfullscreen frameborder="0" style="border:0"></iframe>`
        ));
    });
}

$(function() {
    console.log("test");
});

