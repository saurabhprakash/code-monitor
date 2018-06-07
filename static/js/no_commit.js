$(document).ready(function () {
    $('.show-no-commit-users').on('click', function () {
        if ($('#no-commit-users').hasClass('hidden-content')) {
            $('#no-commit-users').removeClass('hidden-content');
            $('#no-commit-users').slideDown();
            $(this).find('img').attr('src', '../static/images/arrow_drop_up.png');
        }
        else {
            $('#no-commit-users').slideUp().addClass('hidden-content');
            $(this).find('img').attr('src', '../static/images/arrow_drop_down.png');
        }
    });
    $('.show-commit-report').on('click', function () {
        if ($('#commit-report').hasClass('hidden-content')) {
            $('#commit-report').removeClass('hidden-content').slideDown();
            $(this).find('img').attr('src', '../static/images/arrow_drop_up.png');
        }
        else {
            $('#commit-report').slideUp();
            $('#commit-report').addClass('hidden-content');
            $(this).find('img').attr('src', '../static/images/arrow_drop_down.png');
        }
    });
});