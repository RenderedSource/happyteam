var connect = 0;

var connected = function () {
    console.log('connected');
    socket.subscribe('team-chat');
    socket.send({
        'action':'start',
        'room':''
    });
};
var messaged = function (data) {
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
            case 'message':
                addMessage(data);
                break;
            default:
                console.log(data);
                break;
        }
};

var disconnected = function () {
    setTimeout(start, 1000);
};

var addUser = function (data) {

    if (!$('.user-' + data.id).length > 0) {
        $('.user-list').append('<li class="user-' + data.id + '"><a href="#" data-user-id="' + data.id + '"><i class="icon-user"></i> ' + data.name + '</a></li>');
    }
};

var removeUser = function (data) {
    $('.user-' + data.id).remove();
};

var addMessage = function(data){
    $('#group-chat').append(data.message);
};

var start = function () {
    socket = new io.Socket();
    socket.connect();
    socket.on('connect', connected);
    socket.on('disconnect', disconnected);
    socket.on('message', messaged);
};
start();

