// statusupdate.js
$(document).ready(function () {
    $('form.update-status-form').on('submit', function (event) {
        event.preventDefault();

        var form = $(this);
        var formData = form.serialize();
//        var formdata = new FormData(form[0]);
        var url = form.attr('action');
        var command = form.find('#command').val(); // Get the command value

        // Add the command to the formData
        formData += '&command=' + encodeURIComponent(command);

        // Append the command to the FormData object
//        formData.append('command', command);

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
//            processData: false,  // Don't process the data
//            contentType: false,  // Don't set content type
            success: function (data) {
                // Update the success message in the modal body
                var modal = form.closest('.modal');
                var successMessage = '<p class="text-success">' + data.message + '</p>';
                modal.find('.modal-body .success-message').html(successMessage);

                // Clear the command field
                form.find('#command').val('');

                // Update the history section
                var history = $('.modal-footer .history');  // Select the correct history section
                var historyEntry = '<p>' + data.history_entry + '</p>';
                history.append(historyEntry);

                // Close the modal after a delay
                setTimeout(function () {
                    modal.modal('hide');
                }, 2000); // 2000 milliseconds (2 seconds) delay
            },
            error: function (xhr) {
                // Handle error if needed
            }
        });
    });
    $('.modal').on('hidden.bs.modal', function () {
        location.reload();
    });
});

