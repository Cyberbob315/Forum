/**
 * Created by nhannt on 26/07/2017.
 */
function updateText(btn, newCount, verb) {
    countText = $('#like-counter');
    countText.text(newCount);
    btn.text(verb)
}
$('#like-btn').click(function (event) {
    event.preventDefault();
    var this_ = $(this);
    var likeUrl = this_.attr('data-href');
    $.ajax({
        url: likeUrl,
        method: 'GET',
        data: {},
        success: function (data) {
            var likeCount = parseInt(data.likeCount);
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
        }
    });
})
