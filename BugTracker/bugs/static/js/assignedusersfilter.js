$(document).ready(function () {
    // Filter table rows based on selected user
    $('#user-filter').on('change', function () {
        var selectedUser = $(this).val();
        if (selectedUser === 'all') {
            $('table.table tbody tr').show();
        } else {
            $('table.table tbody tr').hide();
            $('table.table tbody tr[data-assigned="' + selectedUser + '"]').show();
        }
    });
});
