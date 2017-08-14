const SUBJECT_API_URL = '/api/subject-mark/subject/';

$(document).ready(function () {
    initEvents();
});


function initEvents() {
    $('.subject-row').on('click', onSubjectRowClick);
    $('#btnSaveSubject').click(updateSubject);
    $('#btnDeleteSubject').click(deleteSubject);
    $('#btn-create-new-subject').click(function (event) {
        $('#subject-create-modal').modal({});
        $('#subject-create-modal').on('hide.bs.modal', function (event) {
            $('#subject-id-create').val('');
            $('#subject-name-create').val('');
            $('#subject-credit-create').val('');
            $('#createErr').hide();
            $('#createErr').empty();
        });
    });
    $('#btnCreateSubject').click(createSubject);
}

function createSubject(event) {
    event.preventDefault();
    let subjectId = $('#subject-id-create').val();
    let subjectTitle = $('#subject-name-create').val();
    let subjectCredit = $('#subject-credit-create').val();
    let csrfToken = $('#subject-create-form').attr('csrf-token');
    $.ajax({
        method: 'POST',
        url: SUBJECT_API_URL,
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: {
            'subject_id': subjectId,
            'title': subjectTitle,
            'credit': subjectCredit
        },
        statusCode: {
            403: function () {
                location.href = '/403/';
            },
            404: function () {
                location.href = '/404/'
            }
        },
        success: function (data, textstatus, xhr) {
            alert('Successfully Created!');
            $('#createErr').hide();
            location.reload()
        },
        error: function (data, textstatus, xhr) {
            let msg = '';
            if (data.responseJSON.subject_id)
                msg += `Subject ID : ${data.responseJSON.subject_id[0]}<br/>`;
            if (data.responseJSON.title)
                msg += ` Title : ${data.responseJSON.title[0]}<br/>`;
            if (data.responseJSON.credit)
                msg += `Credit : ${data.responseJSON.credit[0]}<br/>`;
            $('#createErr').show();
            $('#createErr').html(msg);
        }
    });

}

function updateSubject(event) {
    event.preventDefault();
    let subjectId = $('#subject-id-edit').text();
    let subjectTitle = $('#subject-name-edit').val();
    let subjectCredit = $('#subject-credit-edit').val();
    let csrfToken = $('#subject-edit-form').attr('csrf-token');
    let url = `${SUBJECT_API_URL}${subjectId}/`;
    $.ajax({
        method: 'PUT',
        url: url,
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: {
            'subject_id': subjectId,
            'title': subjectTitle,
            'credit': subjectCredit
        },
        success: function (data, textstatus, xhr) {
            location.reload();
        },
        error: function (data, textstatus, xhr) {
            let msg = '';
            if (data.responseJSON.title)
                msg += ` Title : ${data.responseJSON.title[0]}<br/>`;
            if (data.responseJSON.credit)
                msg += `Credit : ${data.responseJSON.credit[0]}<br/>`;
            $('#editErr').show();
            $('#editErr').html(msg);
        }
    });
}

function deleteSubject(event) {
    if (!confirm('Are you sure to delete this ? All marks and subforum of this subject will also be deleted!'))
        return;
    let subjectId = $('#subject-id-edit').text();
    let url = `${SUBJECT_API_URL}${subjectId}/`;
    let csrfToken = $('#subject-edit-form').attr('csrf-token');
    $.ajax({
        method: 'DELETE',
        url: url,
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: {},
        success: function (data, textstatus, xhr) {
            location.reload()
        },
        error: function (data, textstatus, xhr) {
            alert(xhr.status);
        }
    });
}

function onSubjectRowClick(event) {
    event.preventDefault();
    let this_ = $(this);
    let subjectModal = $('#subject-modal');
    console.log();
    let subjectId = $(this_.children()[0]).text();
    let subjectTitle = $(this_.children()[1]).text();
    let subjectCredit = $(this_.children()[2]).text();
    subjectModal.on('show.bs.modal', function (event) {
        $('#subject-id-edit').text(subjectId);
        $('#subject-name-edit').val(subjectTitle);
        $('#subject-credit-edit').val(subjectCredit);
        $('#editErr').hide();
    });
    subjectModal.modal({})
}
