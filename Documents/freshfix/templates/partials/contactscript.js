

$(document).ready(function () {
    $('#addServiceForm').on('submit', function (event) {
        event.preventDefault();

        // Disable button
        $('#addServiceButton').text('Adding...').attr('disabled', true);

        // Collect data
        const header = $('#header').val();
        const paragraph = $('#paragraph').val();
        const headerone = $('#headerone').val();
        const headertwo = $('#headertwo').val();
        const headerthree = $('#headerthree').val();
        const paragraphone = $('#paragraphone').val();
        const paragraphtwo = $('#paragraphtwo').val();
        const paragraphthree = $('#paragraphthree').val();
        const csrfToken = $('meta[name="csrf-token"]').attr('content');

        // Validate fields
        if (!header || !paragraph || !headerone) {
            $('#responseMessage').html('<div class="alert alert-danger">Please fill all required fields.</div>');
            $('#addServiceButton').text('Add Team').attr('disabled', false);
            return;
        }

        // AJAX Request
        const formData = new FormData();
        formData.append('header', header);
        formData.append('paragraph', paragraph);
        formData.append('headerone', headerone);
        formData.append('headertwo', headertwo);
        formData.append('headerthree', headerthree);
        formData.append('paragraphone', paragraphone);
        formData.append('paragraphtwo', paragraphtwo);
        formData.append('paragraphthree', paragraphthree);
        formData.append('csrfmiddlewaretoken', csrfToken);

        if ($('#imageone')[0].files.length > 0) {
            formData.append('imageone', $('#imageone')[0].files[0]);
        }

        if ($('#imagetwo')[0].files.length > 0) {
            formData.append('imagetwo', $('#imagetwo')[0].files[0]);
        }  
                        

        $.ajax({
            url: "{% url 'fresh:add_us' %}", // Replace with your URL
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#responseMessage').html('<div class="alert alert-success">' + response.message + '</div>');
                $('#addServiceButton').text('Add Team').attr('disabled', false);
                $('#addServiceForm')[0].reset();
            },
            error: function (xhr) {
                const error = xhr.responseJSON ? xhr.responseJSON.message : 'An error occurred.';
                $('#responseMessage').html('<div class="alert alert-danger">' + error + '</div>');
                $('#addServiceButton').text('Add Team').attr('disabled', false);
            }
        });
    });
});
