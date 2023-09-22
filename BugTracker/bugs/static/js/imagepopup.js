$(document).ready(function () {
        $('#imageModal').on('show.bs.modal', function (event) {
            var imageSource = $(event.relatedTarget).attr('href');
            $(this).find('#largeImage').attr('src', imageSource);
        });
    });

//lightbox.option({
//        'resizeDuration': 200,
//        'wrapAround': true
//    });

