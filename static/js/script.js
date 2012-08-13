var users = [];

$(function() {

    var refresh = function() {
        var onlineUsers = users.filter(function(e) { return e.online; });
        var message = '';
        var gambling = false;
        if (onlineUsers.length == 0) {
            message = 'Некому мусор выносить :(';
        } else if (onlineUsers.length == 1) {
            message = 'Без альтернатив :)'
        } else {
            message = 'Да свершится предначертанное!'
            gambling = true;
        }

        $('.step').hide();
        $('.step.step-online-list').show();
        var button = $('.step.step-online-list .btn-gambling');
        button.html(message);

        if (gambling) {
            button.removeClass('disabled');
        } else {
            button.addClass('disabled');
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

    $('.btn-start').click(function() {  
        $('.step').hide();
        $('.step.step-online-progress').show();

        $.getJSON('/gc/get-online', function(data) {
            users = data;
            refresh();

            $('.step.step-online-list .list .item').live('click', function() {
                var userId = $(this).data('user_id');
                var user = users.filter(function(element, index, array) { return element.id == userId; })[0];
                user.online = !user.online;
                refresh();
            });
        }).error(function() {
            alert("error");
        })
    });

    $('.btn-gambling').click(function() {
        if (!$(this).hasClass('disabled')) {
            $('.step').hide();
            $('.step.step-gambling').show();

            var onlineUsers = users.filter(function(element, index, array) { return element.online; });

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
                var user = onlineUsers[i];
                var item = $('<div class="item"><p>' + user.first_name + ' ' + user.last_name + '</p></div>');
                item.css('-webkit-transform', 'rotateY(' + i * delta + 'deg) translateZ(700px)');
                $('.step.step-gambling .roulette').append(item);
            }
        }
    });
})