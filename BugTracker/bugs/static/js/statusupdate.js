// statusupdate.js
$(document).ready(function () {
    $('form.update-status-form').on('submit', function (event) {
        event.preventDefault();

        var form = $(this);
        var formData = form.serialize();
        var url = form.attr('action');

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function (data) {
                // Update the success message in the modal body
                var modal = form.closest('.modal');
                var successMessage = '<p class="text-success">' + data.message + '</p>';
                modal.find('.modal-body .success-message').html(successMessage);

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
