$(document).ready(function () {
    var url = window.location.href.split('/');
    var roomNumber = url[4];
    $('#session_start').click(function () {
        window.location.pathname = '/session_view/' + roomNumber + '/';
    });
    var chatSocket = new ReconnectingWebSocket(
        'ws://' + window.location.host + '/ws/session_view/' + roomNumber + '/');

    chatSocket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        document.querySelector('#chat-log').value += (message + '\n');
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function (e) {
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'command': 'fetch_messages'
        }));

        messageInputDom.value = '';
    };
});