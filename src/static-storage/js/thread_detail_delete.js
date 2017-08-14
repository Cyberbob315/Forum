const COMMENT_API = '/api/comment';

$(document).ready(function () {
    console.log('working');
    let editor = new MediumEditor('.editable');
    $('img').each(function () {
        $(this).addClass('img-responsive');
    });
    $('#btnDeleteThread').click(deleteThread);
    let totalComment = $('#commentSection').attr('total-comment');
    for (let i = 1; i <= totalComment; i++) {
        let btnDeleteId = `#btnDeleteComment-${i}`;
        $(btnDeleteId).click({'btnId': btnDeleteId}, commentDelete);
    }
});

function deleteThread(event) {
    event.preventDefault();
    let deleteModal = $('#deleteModal');
    let threadId = $(this).attr('thread-id');
    let deleteBtn = $('#btnDelete');
    let csrfToken = $(this).attr('csrf-token');
    deleteModal.modal({});
    deleteBtn.click(function (event) {
        $.ajax({
            url: `/api/thread/${threadId}/delete/`,
            method: 'DELETE',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (data) {
                alert('Deleted successfully!');
                location.href = data.redirect_link;
            },
            statusCode: {
                403: function () {
                    location.href = '/403/';
                },
                404: function () {
                    location.href = '/404/'
                }
            },
            error: function (data) {

            }
        });
    })
};

function commentDelete(event) {
    event.preventDefault();
    let btnDeleteId = event.data.btnId;
    let deleteModal = $('#deleteModal');
    let deleteBtn = $('#btnDelete');
    let commentId = $(this).attr('comment-id');
    deleteModal.modal({});
    deleteBtn.click(function (event) {
        event.preventDefault();
        let deleteUrl1 = `${COMMENT_API}/${commentId}/`;
        let csrfToken = $(btnDeleteId).attr('csrf-token');
        $.ajax({
            url: deleteUrl1,
            method: 'DELETE',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (data) {
                console.log('success');
                console.log(data);
                location.href = location.href;
                deleteModal.modal('hide');
            },
            error: function (data) {
                console.log('error');
            }
        });
    });
    deleteModal.on('hide.bs.modal', function () {
        $('#btnDelete').unbind();
        console.log('hide');
    });
}
