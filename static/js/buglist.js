$().ready(function () {
    var jsData = $('#js-data');
    var user_id = jsData.data('user-id');
    var csrf = jsData.data('csrf');
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
    $('#alert-message .close').on('click',function(){
        $('#alert-message').hide();
    });
    $('.owner').live('change', function(){
        var self = $(this);
        $.ajax({
            'type':'post',
            'url':'/buglist/action/',
            'data': {
                'bug': self.data('bug-id'),
                'user': self.val(),
                'csrfmiddlewaretoken':csrf,
                'action':'change-owner'
            },
            success: function(data){
                var alert = $('#alert-message');
                if (data == 'success'){
                    alert.addClass('alert-success').show();
                    alert.find('.content').html('Save success');
                } else {
                    alert.addClass('alert-error').show();
                    alert.find('.content').html(data);
                }
            }
        })
    });
    $('.fixed').live('click', function(){
        var self = $(this);
        self.html('Wait');
        self.attr('disabled','disabled');
        $.ajax({
            'type':'post',
            'url':'/buglist/action/',
            'data': {
                'bug': self.data('bug-id'),
                'csrfmiddlewaretoken':csrf,
                'action':'fixForm'
            },
            success: function(data){
                var alert = $('#alert-message');
                if (data == 'success'){
                    alert.addClass('alert-success').show();
                    alert.find('.content').html('Save success');
                    self.html('In progress');
                } else {
                    self.attr('disabled','');
                    alert.addClass('alert-error').show();
                    alert.find('.content').html(data);
                }
            }
        })
    });
    $('.approve').live('click', function(){
        var self = $(this);
        self.html('Wait');
        self.attr('disabled','disabled');
        $.ajax({
            'type':'post',
            'url':'/buglist/action/',
            'data': {
                'bug': self.data('bug-id'),
                'csrfmiddlewaretoken':csrf,
                'action':'approve'
            },
            success: function(data){
                var alert = $('#alert-message');
                if (data == 'success'){
                    alert.addClass('alert-success').show();
                    alert.find('.content').html('Fixed');
                    self.parent().append('<span class="label label-success">Close</span>');
                    self.remove();
                } else {
                    self.attr('disabled','');
                    alert.addClass('alert-error').show();
                    alert.find('.content').html(data);
                }
            }
        })
    })
});