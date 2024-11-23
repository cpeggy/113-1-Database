$(document).ready(function() {
    $('.toggle-button').click(function() {
        $(this).next('.log-details').toggle();
    });
});