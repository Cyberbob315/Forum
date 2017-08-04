$(document).ready(function () {
    console.log('working');

    $('img').each(function () {
       $(this).addClass('img-responsive');
    });

    let totalComment = $('#commentSection').attr('total-comment');
    for (let i = 1; i <= totalComment; i++) {
        let btnId = '#btnDeleteComment-' + i;
        $(btnId).click({'btnId': btnId}, commentDelete)
    }
});

function commentDelete(event) {
    event.preventDefault();
    btnDeleteId = event.data.btnId;
    let deleteModal = $('#deleteModal');
    let deleteBtn = $('#btnDelete');
    deleteModal.modal({});
    deleteBtn.click(function (event) {
        event.preventDefault();
        deleteUrl1 = $(btnDeleteId).attr('delete-url');
        csrfToken = $(btnDeleteId).attr('csrf-token');
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
