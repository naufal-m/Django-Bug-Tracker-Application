$(document).ready(function () {
    $('form.update-status-form').on('submit', function (event) {
        event.preventDefault();

        var form = $(this);
        var formData = new FormData(form[0]);
        var url = form.attr('action');
        var command = form.find('input[name="command"]').val(); // Get the command value

        formData.append('command', command);    // Append the command

        console.log('Command Value:', command);


        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            contentType: false,  // set content type to false for FormData
            processData: false,  // Disable processData for FormData
            success: function (data) {
                console.log(data);
                var successMessage = '<p class="text-success">' + data.message + '</p>';
                $('.success-message').html(successMessage);

//                // Clear the command field
                form.find('input[name="command"]').val('');

                // Refresh the page after a delay
                setTimeout(function () {
                    location.reload();
                }, 3000); // 3000 milliseconds (3 seconds) delay
            },
            error: function (xhr) {
                // Handle error if needed
            }
        });
    });
});
