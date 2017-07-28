var successText = `<span class="alert alert-success btn-sm"><strong>Published</strong></span>`;
var failText = `<span class="alert alert-warning btn-sm"><strong>Error Occured!</strong></span>`;
var deleteSuccess = `<span class="alert alert-success btn-sm"><strong>Deleted</strong></span>`;;
var totalThread = 0;
$(document).ready(function () {
    totalThread = parseInt($('#thread_counter').attr('data-href'));
    for (i = 1; i <= totalThread; i++) {
        var publishId = '#btn-publish-' + i;
        var deleteId = '#btn-delete-'+i;
        $(publishId).click({'counter': i}, publish);
        $(deleteId).click({'counter':i}, deleteThread);
    }
});

function deleteThread(event) {
    event.preventDefault();
    var counter = event.data.counter;
    var deleteAreaId = '#delete-area-' + counter;
    var deleteArea = $(deleteAreaId);
    var deleteUrl = $(this).attr('delete-url');
    $.ajax({
        url: deleteUrl,
        method: 'GET',
        data: {},
        success: function (data) {
            if (data.success) {
                deleteArea.html(deleteSuccess);
            }
        },
        error: function (data) {
            deleteArea.html(failText);
        }
    });
}

function publish(event) {
    event.preventDefault();
    var counter = event.data.counter;
    var publishAreaId = '#publish-area-' + counter;
    var publishArea = $(publishAreaId);
    var publishUrl = $(this).attr('publish-url');
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


