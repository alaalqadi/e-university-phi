var session;
$(document).ready(function (e) {
    var session_id = sessionId;
    // var session;
    var api_key = apiKey;
    var token = accessToken;
    var publisher;


    function initOpenTok() {
        if (OT.on) {
            OT.on("exception", exceptionHandler);
        } else {
            OT.addEventListener(OT.EXCEPTION, exceptionHandler);
        }

        session = OT.initSession(null, session_id, {});

        if (session.on) {
            session.addEventListener = session.on;
        } else {
            session.removeEventListener = session.off;
            session.off();
        }
        session.on('sessionConnected', sessionConnectedHandler);
        session.on('streamCreated', streamCreatedHandler);
        session.on('streamDestroyed', streamDestroyedHandler);

        session.connect(api_key, token);
    }

    $('.connection-info .publish').on('click', function (e) {
        var pub_properties = {
            width: '100%',
            height: '100%',
        };
        publisher = session.publish('video', pub_properties);

        if (publisher.on) {
            publisher.addEventListener = publisher.on;
        }

        publisher.addEventListener("streamCreated", streamCreatedHandler)
        publisher.addEventListener("streamDestroyed", streamDestroyedHandler)

        $('.connection-info').attr('data-status', "publishing");
    });

    function sessionConnectedHandler(event) {
        $(".connection-info .publish").removeClass("disabled").addClass('active')
    }

    function streamCreatedHandler(event) {
        var stream = event.stream;

        if (stream.connection.connectionId == session.connection.connectionId) {
            selfStreamCreated(stream);
        } else {
            otherStreamCreated(stream);
        }
    }


    function selfStreamCreated(stream) {
        $('.connection-info .unpublish').closest('li').removeClass('hidden');
        $('.connection-info .publish').closest('li').addClass('hidden');

        $('.connection-info .unpublish').removeClass('disabled').click(function () {
            $('.connection-info').attr('data-status', '');
            session.unpublish(publisher);
            $(this).addClass('disabled');
        }).addClass('active');

        $('.connection-info .video').removeClass('disabled').click(function () {
            if ($(this).hasClass('active')) {
                publisher.publishVideo(false);
                $(this).removeClass('active');
            } else {
                publisher.publishVideo(true);
                $(this).addClass('active');
            }
        }).addClass('active');


        $('.connection-info .audio').removeClass('disabled').click(function () {
            if ($(this).hasClass('active')) {
                publisher.publishAudio(false);
                var bdm = publisher.getStyle().buttonDisplayMode;
                publisher.setStyle({buttonDisplayMode: 'on'});
                setTimeout(function () {
                    publisher.setStyle({buttonDisplayMode: bdm})
                }, 2000);
                $(this).removeClass('active');
            } else {
                publisher.publishAudio(true);
                var bdm = publisher.getStyle().buttonDisplayMode;
                publisher.setStyle({buttonDisplayMode: 'on'});
                setTimeout(function () {
                    publisher.setStyle({buttonDisplayMode: bdm})
                }, 2000);
                $(this).addClass('active');
            }
        }).addClass('active');
    }


    function otherStreamCreated(stream) {
        var sub_properties = {
            width: '100%',
            height: '100%',
            fitMode: "contain",
        };
        var subscriber = session.subscribe(stream, 'video', sub_properties);
        $('.connection-info').attr('data-status', "publishing");
    }

    function streamDestroyedHandler(event) {
        var stream = event.stream;

        $('.connection-info').attr('data-status', '');
        $('.connection-info .video-container').append('<div id="video"></div>');
        $('.connection-info .unpublish').closest('li').addClass('hidden');
        $('.connection-info .publish').closest('li').removeClass('hidden');
        $('.connection-info .unpublish, .connection-info .video, .connection-info .audio').removeClass('active').addClass('disabled')
    }


    function exceptionHandler(event) {
        console.error(event);
    }

    initOpenTok();
});