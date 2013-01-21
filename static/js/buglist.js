$().ready(function(){

    $('.nav-buttons').button('toggle');
    $('#my-work').on('click', function(){
        var user_id = $(this).data('user_id');
        $.get('',{'requester':user_id});
    });
    $('#my-bugs').on('click', function(){
        var user_id = $(this).data('user_id');
        $.get('',{'owner':user_id});
    });
    $('#resolved').on('click', function(){
        var user_id = $(this).data('user_id');
        $.get('',{'status':true});
    });
});