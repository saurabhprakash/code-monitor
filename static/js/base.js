$(document).ready(function () {
    var activeElement;
    $('.submenu').addClass('hidden-content'); //hiding submenu 
    var pageName = $('.page-selector').data('page-name');
    switch (pageName) {
        case 'dashboard': $('.menu-items.dashboard').addClass('active');
            activeElement = $('.menu-items.dashboard');
            break;
        case 'user-report': $('.menu-items.user-report').addClass('active');
            activeElement = $('.menu-items.user-report');
            break;
        case 'lead-reports': $('.submenu').removeClass('hidden-content'); //show submenu on lead report
            if($('#no-commit-data').length) activeElement = $('#no-commit-sub-menu');
            else if ($('#full-commit-data').length) activeElement = $('#full-commit-sub-menu');
            activeElement.addClass('active');
            break;
        default: break;
    }
    $('.menu-items').on('click', function () {
        if($(this).hasClass('lead-reports')){ //show & hide submenu
            if($(this).hasClass('submenu-opened')){
                $(this).removeClass('submenu-opened');
                $('.submenu').addClass('hidden-content');
            } 
            else {
                $(this).addClass('submenu-opened');
                $('.submenu').removeClass('hidden-content'); 
            }
            return;
        }
        if (activeElement) activeElement.removeClass('active');//active selected menu
        $(this).addClass('active');
        activeElement = $(this);
        addPageLoader('.rendered-page');
    });
});

function addPageLoader(loaderDivClass) {
    $(loaderDivClass).html('<div class="page-navigation-loader"><img src="/static/images/Ellipsis-1s-200px.gif"></img></div>');
}