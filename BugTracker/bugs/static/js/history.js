$(document).ready(function() {
    // Assuming this function is called when the modal is opened
    function displayHistoryEntries() {
        var bugHistoryString = document.getElementById('bugHistory').textContent;
        var bugHistoryArray = bugHistoryString.split('\n');

        var historyList = document.getElementById('historyList');

//        var history = $('.history');

        for (var i = 0; i < bugHistoryArray.length; i++) {
            var historyEntryText = bugHistoryArray[i].trim();
            if (historyEntryText !== '') {
                var historyEntry = document.createElement('li');
                historyEntry.textContent = historyEntryText;
                historyList.appendChild(historyEntry);
            }
        }
    }

    // Call the function to display history entries when the modal is opened
    $('#yourModalId').on('shown.bs.modal', function() {
        displayHistoryEntries();
    });
});
