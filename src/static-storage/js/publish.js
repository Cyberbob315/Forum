let successText = `<span class="alert alert-success btn-sm"><strong>Published</strong></span>`;
let failText = `<span class="alert alert-warning btn-sm"><strong>Error Occured!</strong></span>`;
let deleteSuccess = `<span class="alert alert-success btn-sm"><strong>Deleted</strong></span>`;
let totalThread = 0;
$(document).ready(function () {
    totalThread = parseInt($('#thread_counter').attr('data-href'));
    for (i = 1; i <= totalThread; i++) {
        let publishId = `#btn-publish-${i}`;
        let deleteId = `#btn-delete-${i}`;
        $(publishId).click({'counter': i}, publish);
        $(deleteId).click({'counter': i}, showDeleteConfirm);
    }
});

function showDeleteConfirm(event) {
    event.preventDefault();
    let deleteModal = $('#deleteModal');
    deleteModal.modal({});
    let counter = event.data.counter;
    $('#btnDelete').click(function (event) {
        event.preventDefault();
        let deleteId = `#btn-delete-${counter}`;
        let deleteAreaId = `#delete-area-${counter}`;
        let deleteArea = $(deleteAreaId);
        let deleteUrl = $(deleteId).attr('delete-url');
        let csrfToken = $(deleteId).attr('csrf-token');
        console.log(deleteUrl);
        $.ajax({
            url: deleteUrl,
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: {},
            success: function (data) {
                if (data.success) {
                    deleteArea.html(deleteSuccess);
                    deleteModal.modal('hide');
                }
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
    let counter = event.data.counter;
    let publishAreaId = '#publish-area-' + counter;
    let publishArea = $(publishAreaId);
    let publishUrl = $(this).attr('publish-url');
    let csrfToken = $(this).attr('csrf-token');
    $.ajax({
        url: publishUrl,
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrfToken
        },
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
            if (data.success) {
                publishArea.html(successText);
            }
        },
        error: function (data) {
            publishArea.html(failText);
        }
    });
}


