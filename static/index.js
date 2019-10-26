function handleSubmit() {
    const address = $('#usr12').val();
    console.log(`Querying with address ${address}...`);
    const url = window.location.href + 'narrative?address=' + address;
    fetch(url).then(function(response) {
        return response.json();
    }).then(function(json) {
        $('#narrative').text(json.narrative);
    });
}

$(function() {
    console.log("test");
});

