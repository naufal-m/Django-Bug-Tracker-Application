$(document).ready(function () {
    // Filter table rows based on selected status and user
    $('#status-filter, #user-filter').on('change', function () {
        var selectedStatus = $('#status-filter').val();
        var selectedUser = $('#user-filter').val();

        // Show all rows initially
        $('table.table tbody tr').show();

        // Filter by status if not 'all'
        if (selectedStatus !== 'all') {
            $('table.table tbody tr:not([data-status="' + selectedStatus + '"])').hide();
        }

        // Filter by user if not 'all'
        if (selectedUser !== 'all') {
            $('table.table tbody tr:not([data-user="' + selectedUser + '"])').hide();
        }
    });
});
