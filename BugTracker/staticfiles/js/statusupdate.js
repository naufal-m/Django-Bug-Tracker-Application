// statusupdate.js
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
                // Update the success message in the modal body
                var modal = form.closest('.modal');
                var successMessage = '<p class="text-success">' + data.message + '</p>';
                modal.find('.modal-body .success-message').html(successMessage);

                // Clear the command field
                form.find('input[name="command"]').val('');

//                // Update the history section
//                var bugHistoryString = document.getElementById('bugHistory').textContent;
//                var bugHistoryArray = bugHistoryString.split('\n'); // Split history string by line breaks
//
//                var history = $('.history');  // Select the correct history section
//
//                var historyEntry = $('<div>').text(data.history_entry);
//
//                for (var i = 0; i < bugHistoryArray.length; i++) {
//                    var historyEntryText = bugHistoryArray[i];
//                    if (historyEntryText.trim() !== '') {
//                        var historyEntry = $('<div>').addClass('history-entry').text(historyEntryText);
//                        history.append(historyEntry);
//                    }
//                }

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

