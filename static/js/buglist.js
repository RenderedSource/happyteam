$().ready(function(){
    var user_id = 1;
    $('.nav-buttons').button('toggle');
    $('#my-work').on('click', function(){
        $.get('',{'requester':user_id});
    });
    $('#my-bugs').on('click', function(){
        $.get('',{'owner':user_id});
    });
    $('#resolved').on('click', function(){
        $.get('',{'status':true});
    });
});