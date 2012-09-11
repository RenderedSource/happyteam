var users = [];

$(function () {

    var refresh = function () {
        var onlineUsers = users.filter(function (e) {
            return e.online;
        });
        var message = '';
        var gambling = false;
        if (onlineUsers.length == 0) {
            message = 'Некому мусор выносить :(';
        } else if (onlineUsers.length == 1) {
            message = 'Без альтернатив :)'
        } else {
            message = 'Да свершится предначертанное!';
            gambling = true;
        }

        $('.step').hide();
        $('.step.step-online-list').show();
        var button = $('.step.step-online-list .btn-gambling');
        var button_test = $('.step.step-online-list .btn-gambling-test');
        button.html(message);

        if (gambling) {
            button.removeClass('disabled');
            button_test.removeClass('disabled');
        } else {
            button.addClass('disabled');
            button_test.addClass('disabled');
        }

        var online = $('.step.step-online-list .list-online');
        var offline = $('.step.step-online-list .list-offline');
        online.find('.item').remove();
        offline.find('.item').remove();
        for (var i in users) {
            var user = users[i];
            var container = user.online ? online : offline;
            var item = $('<div class="item">' + user.first_name + ' ' + user.last_name + '</div>');
            container.append(item);
            item.data('user_id', user.id);
        }
    }

    $('.btn-start').click(function () {
        $('.step').hide();
        $('.step.step-online-progress').show();

        $.getJSON('/gc/get-online',function (data) {
            users = data;
            refresh();

            $('.step.step-online-list .list .item').live('click', function () {
                var userId = $(this).data('user_id');
                var user = users.filter(function (element, index, array) {
                    return element.id == userId;
                })[0];
                user.online = !user.online;
                refresh();
            });
        }).error(function () {
                    alert("error");
                })
    });
    var looser_ajax = function (user_id) {
        $.ajax({
            url:'/gc/addlooser/',
            type:'post',
            dataType:'json',
            data:{
                'csrfmiddlewaretoken':$('input[name="csrfmiddlewaretoken"]').val(),
                'user':user_id
            },
            success:function (data) {
                // todo status.true / false
                console.log(data)
            }
        })
    };

    function checkLooser(test) {
        if (!$(this).hasClass('disabled')) {
            $('.step').hide();
            $('.step.step-gambling').show();

            var onlineUsers = users.filter(function (element, index, array) {
                return element.online;
            });

            if (onlineUsers.length == 0) {
                throw 'Users not found';
            }

            var userCount = onlineUsers.length;
            var rand = Math.random();
            var looser = Math.floor(rand / (1 / userCount));

            for (var i = 0; i < looser; i++) {
                onlineUsers.push(onlineUsers.shift());
            }

            var delta = 360 / userCount;
            for (var i in onlineUsers) {
                if (i == 0) {
                    if(!test){
                        looser_ajax(onlineUsers[i].id)
                    }
                }
                var user = onlineUsers[i];
                var item = $('<div class="item" data-user="' + user.id + '"><p>' + user.first_name + ' ' + user.last_name + '</p></div>');
                item.css('-webkit-transform', 'rotateY(' + i * delta + 'deg) translateZ(700px)');
                $('.step.step-gambling .roulette').append(item);
            }

        }
    }

    // todo add looser id in $('#looserId').val()
    $('.btn-gambling').click(function () {
        checkLooser(false)
    });
    $('.btn-gambling-test').click(function () {
        checkLooser(true)
    });
});