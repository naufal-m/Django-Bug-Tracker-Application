$(document).ready(function () {
    // Filter table rows based on selected status
    $('#status-filter').on('change', function () {
        var selectedStatus = $(this).val();
        if (selectedStatus === 'all') {
            $('table.table tbody tr').show();
        } else {
            $('table.table tbody tr').hide();
            $('table.table tbody tr[data-status="' + selectedStatus + '"]').show();
        }
    });
});
