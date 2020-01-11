$(document).ready(function () {
    var url = window.location.href.split('/');
    var roomNumber = url[4];
    $('#session_start').click(function () {
        window.location.pathname = '/session_view/' + roomNumber + '/';
    });
    var chatSocket = new ReconnectingWebSocket(
        'ws://' + window.location.host + '/ws/session_view/' + roomNumber + '/');

    chatSocket.onopen = function (e) {
        fetchMessages();
    }

    chatSocket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        if (data['command'] === 'messages') {
            for (let i = 0; i < data['messages'].length; i++) {
                createMessage(data['messages'][i]);
            }
        } else if (data['command'] === 'new_message') {
            createMessage(data['message']);
        }
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
        var messageInputDom = document.getElementById('chat-message-input');
        var message = messageInputDom.value;
        if (message) {
            chatSocket.send(JSON.stringify({
                'command': 'new_message',
                'message': message,
                'from': username
            }));
        } else {
            return false;
        }
        messageInputDom.value = '';
    };

    function fetchMessages() {
        chatSocket.send(JSON.stringify({'command': 'fetch_messages'}));
    }

    function createMessage(data) {
        var author = data['author'];
        var msgListTag = document.createElement('li');
        var imgTag = document.createElement('img');
        var pTag = document.createElement('p');
        pTag.textContent = data.content;
        imgTag.src = 'http://emilcarlsson.se/assets/mikeross.png';

        if (author === username) {
            msgListTag.className = 'sent';
        } else {
            msgListTag.className = 'replies';
        }
        msgListTag.appendChild(imgTag);
        msgListTag.appendChild(pTag);
        document.querySelector('#chat-log').appendChild(msgListTag);
    }
});