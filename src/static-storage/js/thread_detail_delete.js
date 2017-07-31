$(document).ready(function () {
    console.log('working');
    var totalComment = $('#commentSection').attr('total-comment');
    console.log('totalComment:' + totalComment);
    for (i = 1; i <= totalComment; i++) {
        var btnId = '#btnDeleteComment-' + i;
        $(btnId).click({'btnId': btnId}, commentDelete)
    }
});

function commentDelete(event) {
    event.preventDefault();
    btnDeleteId = event.data.btnId;
    var deleteModal = $('#deleteModal');
    var deleteBtn = $('#btnDelete');
    deleteModal.modal({});
    deleteBtn.click(function (event) {
        event.preventDefault();
        deleteUrl1 = $(btnDeleteId).attr('delete-url');
        csrfToken = $(btnDeleteId).attr('csrf-token');
        console.log("DELETEURL 1", deleteUrl1);
        $.ajax({
            url: deleteUrl1,
            method: 'DELETE',
            dataType: 'json',
            headers:{
                'X-CSRFToken': csrfToken
            },
            data: {},
            success: function (data) {
                console.log('success');
                console.log(data);
                // location.href = location.href;
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
