$(document).ready(function () {
    var activeElement;
    var pageName = $('.page-selector').data('page-name');
    switch (pageName) {
        case 'dashboard': $('.menu-items.dashboard').addClass('active');
            activeElement = $('.menu-items.dashboard');
            break;
        case 'user-report': $('.menu-items.user-report').addClass('active');
            activeElement = $('.menu-items.user-report');
            break;
        case 'lead-reports': $('.menu-items.lead-reports').addClass('active');
            activeElement = $('.menu-items.lead-reports');
            break;
        default: break;
    }
    $('.menu-items').on('click', function () {
        if (activeElement) activeElement.removeClass('active');
        $(this).addClass('active');
        activeElement = $(this);
    });
});