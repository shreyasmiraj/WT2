$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);

        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data, req, resp) {
                $("#result-image-div").css("display", "block")
                $("#upload-image-div").css("display", "none")
                $('#classValue').html("The given image is a " + resp["responseJSON"]["classValue"])
                console.log('Success!');
            },
        });
    });
});


$(function() {
    $('#upload-more-btn').click(function() {
 
        $("#result-image-div").css("display", "none")
        $("#upload-image-div").css("display", "block")
         $.ajax({
            type: 'POST',
            url: '/',
            contentType: false,
            cache: false,
            processData: false,
            success: function(data, req, resp) {

                console.log('Success!');
            },
        });
    });
});