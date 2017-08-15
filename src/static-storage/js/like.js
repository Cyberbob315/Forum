/**
 * Created by nhannt on 26/07/2017.
 */
function updateText(btn, newCount, verb) {
    countText = $('#like-counter');
    countText.text(newCount);
    btn.text(verb)
}

$(document).ready(function () {
    let likeBtn = $('#like-btn');
    let checkLikeUrl = likeBtn.attr('check-like-url');
    $.ajax({
        url: checkLikeUrl,
        method: 'GET',
        data: {},
        statusCode: {
            403: function () {
                location.href = '/403/';
            },
            404: function () {
                location.href = '/404/'
            }
        },
        success: function (data) {
            let likeCount = parseInt(data.like_count);
            if (data.is_liked) {
                updateText(likeBtn, likeCount, 'Unlike');
                likeBtn.removeClass('glyphicon-thumbs-up').addClass('glyphicon-thumbs-down');
            } else {
                updateText(likeBtn, likeCount, 'Like');
                likeBtn.removeClass('glyphicon-thumbs-down').addClass('glyphicon-thumbs-up');
            }
        },
        error: function (error) {
            console.log('error');
        }
    });
});

$('#like-btn').click(function (event) {
    event.preventDefault();
    let this_ = $(this);
    let csrfToken = this_.attr('csrf-token');
    let likeUrl = this_.attr('like-url');
    let threadId = this_.attr('thread-id');
    $.ajax({
        url: likeUrl,
        method: 'PUT',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrfToken
        },
        statusCode: {
            403: function () {
                location.href = `/accounts/login-site/?next=/threads/show/${threadId}`;
            },
            404: function () {
                location.href = '/404/'
            }
        },
        data: {},
        success: function (data) {
            let likeCount = parseInt(data.like_count);
            if (data.liked) {
                updateText(this_, likeCount, 'Unlike');
                this_.removeClass('glyphicon-thumbs-up').addClass('glyphicon-thumbs-down');
            } else {
                updateText(this_, likeCount, 'Like');
                this_.removeClass('glyphicon-thumbs-down').addClass('glyphicon-thumbs-up');
            }
        },
        error: function (error) {
            console.log('error');
            window.location.href = '/accounts/login-site';
        }
    });
});
