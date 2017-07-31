var successText = `<span class="alert alert-success btn-sm"><strong>Published</strong></span>`;
var failText = `<span class="alert alert-warning btn-sm"><strong>Error Occured!</strong></span>`;
var deleteSuccess = `<span class="alert alert-success btn-sm"><strong>Deleted</strong></span>`;
;
var totalThread = 0;
$(document).ready(function () {
    totalThread = parseInt($('#thread_counter').attr('data-href'));
    for (i = 1; i <= totalThread; i++) {
        var publishId = '#btn-publish-' + i;
        var deleteId = '#btn-delete-' + i;
        $(publishId).click({'counter': i}, publish);
        $(deleteId).click({'counter': i}, showDeleteConfirm);
    }
});

function showDeleteConfirm(event) {
    event.preventDefault();
    var deleteModal = $('#deleteModal');
    deleteModal.modal({});
    var counter = event.data.counter;
    $('#btnDelete').click(function (event) {
        event.preventDefault();
        var deleteId = '#btn-delete-' + counter;
        var deleteAreaId = '#delete-area-' + counter;
        var deleteArea = $(deleteAreaId);
        var deleteUrl = $(deleteId).attr('delete-url');
        console.log(deleteId);
        console.log(deleteUrl);
        $.ajax({
            url: deleteUrl,
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log('success');
                if (data.success) {
                    deleteArea.html(deleteSuccess);
                    deleteModal.modal('hide');
                }
            },
            error: function (data) {
                deleteArea.html(failText);
            }
        });
    });
    deleteModal.on('hide.bs.modal', function () {
        $('#btnDelete').unbind();
        console.log('hide');
    })
}

function deleteThread(event) {

}

function publish(event) {
    event.preventDefault();
    var counter = event.data.counter;
    var publishAreaId = '#publish-area-' + counter;
    var publishArea = $(publishAreaId);
    var publishUrl = $(this).attr('publish-deleteUrl');
    $.ajax({
        url: publishUrl,
        method: 'GET',
        data: {},
        success: function (data) {
            if (data.success) {
                publishArea.html(successText);
            }
        },
        error: function (data) {
            publishArea.html(failText);
        }
    });
}


