$().ready(function () {
    var user_id = $('#js-data').data('user-id');
    var table = $('#bug-table');
    var data = {'window':false};


    $('#my-work').on('click', function () {
        var self = $(this);
        if(self.hasClass('active')){
            delete  data.owner;
            self.removeClass('active');
        } else {
            data.owner = user_id;
            self.addClass('active');
        }
        $.ajax({
            url:'',
            data:data,
            success:function(data){
                table.html(data);
            }
        })
    });
    $('#my-bugs').on('click', function () {
        var self = $(this);
        if(self.hasClass('active')){
            delete  data.requester;
            self.removeClass('active');
        } else {
            data.requester = user_id;
            self.addClass('active');
        }
        $.ajax({
            url:'',
            data:data,
            success:function(data){
                table.html(data);
            }
        })
    });
    $('#resolved').on('click', function () {
        var self = $(this);
        if(self.hasClass('active')){
            delete  data.status;
            self.removeClass('active');
        } else {
            data.status = user_id;
            self.addClass('active');
        }

        $.ajax({
            url:'',
            data:data,
            success:function(data){
                table.html(data);
            }
        })
    });
});