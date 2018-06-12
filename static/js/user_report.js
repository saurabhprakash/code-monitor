$(document).ready(function () {
    init();
});
function init() {
    $('#user-dropdown').select2();
    $('#user-dropdown').on('change',function(){
        if(!$('#user-dropdown').find('option:selected').prop('disabled')) {
            $('.user-data').html('').addClass('page-loader');
            showReleventData($('#user-dropdown').find('option:selected').val());
            }
    });
}   
function showReleventData(endPoint) {
    var baseUrl='/user/issues/';
    $.ajax({
            url: baseUrl+endPoint+'/',
            type: "GET"
            })
            .done(function( data ) {
                $('.user-data').removeClass('page-loader');  
                $('.user-data').html(data);
            })
            .fail(function( xhr, status, errorThrown ) {
                $('.user-data').removeClass('page-loader');      
                alert( "Sorry, there was a problem!" );
                console.log( "Status: " + status );
                console.dir( xhr );
            });
}