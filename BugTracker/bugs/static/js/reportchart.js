document.addEventListener("DOMContentLoaded", function () {
    console.log('DOMContentLoaded event fired.');

    var statusCountsData = document.getElementById('status-data').getAttribute('data-status-counts');
    var statusCounts = JSON.parse(statusCountsData);
    console.log('statusCounts:', statusCounts);

    var statusLabels = ["Open", "In Progress", "Re-open", "Done", "Closed"];
    console.log('statusLabels:', statusLabels);

    // Create a reference to the canvas element
    var ctx = document.getElementById('statusChart').getContext('2d');

    // Create the bar chart
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: statusLabels,
            datasets: [{
                label: 'Status Counts',
                data: statusCounts,
                backgroundColor: [
                    'rgb(255, 173, 153)', // Bar color for Open
                    'rgb(153, 204, 255)', // Bar color for In-progress
                    'rgb(255, 194, 153)', // Bar color for Re-open
                    'rgb(159, 223, 190)', // Bar color for Done
                    'rgb(217, 217, 217)', // Bar color for Close
                ],
                borderColor: [
                    'rgb(255, 173, 153)', // Bar color for Open
                    'rgb(153, 204, 255)', // Bar color for In-progress
                    'rgb(255, 194, 153)', // Bar color for Re-open
                    'rgb(159, 223, 190)', // Bar color for Done
                    'rgb(217, 217, 217)', // Bar color for Close
                ],
                borderWidth: 1,
                barPercentage: 0.05,
                categoryPercentage: 0.3,
            }]
        },
        options: {
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: 12,
                        },
                        maxRotation: 10,
                        autoSkip: false,
                        stepSize: 0.3,
                    },
                    beforeFit: function(scaleInstance) {
                        scaleInstance.width = 1; // sets the width to 100px
                    },
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 0.3, // Adjust as needed
                        suggestedMin: 0, // Set the minimum value to 0
                        suggestedMax: 10, // Set the maximum value to your desired
                    },
                    display: false,
                },
            },
        },
    });
});

