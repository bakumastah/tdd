$(document).ready(function() {
    $('body').on('keypress click', 'input#test', function() {
        $('.has-error').hide();
    })
});
