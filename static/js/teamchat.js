var socket = new io.Socket();
socket.connect();
var data = {
    'action':'start',
    'room':''
};
socket.on('connect', function () {
    socket.subscribe('team-chat');
    socket.send(data);
});

var addUser = function (data) {

    if (!$('.user-' + data.id).length > 0) {
        $('.user-list').append('<li class="user-' + data.id + '"><a href="#" data-user-id="' + data.id + '"><i class="icon-user"></i> ' + data.name + '</a></li>');
    }
};
var removeUser = function (data) {
    $('.user-' + data.id).remove();
};
socket.on('message', function (data) {
    console.log(data);
    switch (data.action) {
        case 'started':
            $.each(data.users, function (i, user) {
                addUser({name:user.name, id:user.id});
            });
            break;
        case 'join':
            addUser(data);
            break;
        case 'leave':
            removeUser(data);
            break;
        default:
            console.log(data);
            break;
    }
});
