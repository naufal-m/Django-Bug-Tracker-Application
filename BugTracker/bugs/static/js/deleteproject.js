$(document).ready(function () {
    // Get the CSRF token from the page's cookie
    var csrftoken = getCookie('csrftoken');

    $('.delete-project-button').on('click', function (event) {
        event.preventDefault();

        var project_id = $(this).data('project-id');
        var delete_url = $(this).data('delete-url');

        // Display a confirmation dialog
        if (confirm('Are you sure you want to delete this project?')) {
            $.ajax({
                type: 'POST',
                url: delete_url,
                data: {
                    csrfmiddlewaretoken: csrftoken  // Include the CSRF token
                },
                success: function (data) {
                    if (data.success) {
                        // Reload the page or update the project list as needed
                        location.reload();
                    } else {
                        alert('Failed to delete the project.');
                    }
                },
                error: function () {
                    alert('An error occurred while trying to delete the project.');
                }
            });
        }
    });
});

// Function to get the CSRF token from the cookie
function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}
