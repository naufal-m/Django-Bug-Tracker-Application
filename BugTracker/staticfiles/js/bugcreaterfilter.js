<script>
    document.addEventListener('DOMContentLoaded', function () {
        const reporterFilter = document.getElementById('reporter-filter');

        reporterFilter.addEventListener('change', function () {
            const selectedReporter = reporterFilter.value;
            filterBugsByReporter(selectedReporter);
        });

        function filterBugsByReporter(reporter) {
            const bugElements = document.querySelectorAll('.bug');

            bugElements.forEach(function (bugElement) {
                const bugReporter = bugElement.getAttribute('data-reporter');

                if (reporter === 'all' || bugReporter === reporter) {
                    bugElement.style.display = 'block';
                } else {
                    bugElement.style.display = 'none';
                }
            });
        }
    });
</script>
