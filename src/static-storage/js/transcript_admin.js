const MARK_API_URL = '/api/subject-mark/mark/';

$(document).ready(function () {
    jQuery('.mark-row').click(onMarkRowClick);
    jQuery('#btnAddMark').click(function (event) {
        event.preventDefault();
        jQuery('#mark-create-modal').modal({});
    });
    jQuery('#btnCreateMark').click(addMark);
    jQuery('#btnSaveMark').click(updateMark);
    $('#mark-create-modal').on('hide.bs.modal', function (event) {
            $('#mid-term-mark-create').val('');
            $('#final-mark-create').val('');
            $('#markCreateErr').hide();
            $('#markCreateErr').empty();
        });
});

function updateMark(event) {
    let markForm = $('#mark-edit-form');
    let subjectId = markForm.attr('subject-id');
    let studentId = jQuery('#btnAddMark').attr('student-id');
    let markId = markForm.attr('mark-id');
    let midTermMark = $('#mid-term-mark-edit').val();
    let finalMark = $('#final-mark-edit').val();
    let url = `${MARK_API_URL}${markId}/`;
    let csrfToken = markForm.attr('csrf-token');
    $.ajax({
        url: url,
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrfToken
        },
        dataType: 'json',
        data: {
            'subject': subjectId,
            'student': studentId,
            'mid_term_mark': midTermMark,
            'final_mark': finalMark
        },
        success: function (data) {
            alert('Updated successfully!');
            location.reload();
        },
        error: function (data) {
            let msg = '';
            if (data.responseJSON.mid_term_mark)
                msg += ` Mid term mark : ${data.responseJSON.mid_term_mark[0]}<br/>`;
            if (data.responseJSON.final_mark)
                msg += ` Final mark: ${data.responseJSON.final_mark[0]}<br/>`;
            $('#markEditErr').show();
            $('#markEditErr').html(msg);
        }
    });
}

function onMarkRowClick(event) {
    let this_ = $(this);
    let subjectId = this_.attr('subject-id');
    let subjectTitle = $(this_.children()[2]).text();
    let midTermMark = $(this_.children()[4]).text();
    let finalMark = $(this_.children()[5]).text();
    let markID = this_.attr('mark-id');
    let markEditForm = $('#mark-edit-form');
    markEditForm.attr('mark-id', markID);
    markEditForm.attr('subject-id', subjectId);
    $('#mark-edit-modal').on('show.bs.modal', function (event) {
        $('#mark-subject-edit').text(subjectTitle);
        $('#mid-term-mark-edit').val(midTermMark);
        $('#final-mark-edit').val(finalMark);
        $('#markEditErr').hide();
    });
    $('#mark-edit-modal').modal({});
}

function addMark(event) {
    event.preventDefault();
    let subjectId = jQuery('#subject-select-create').val();
    let studentId = jQuery('#btnAddMark').attr('student-id');
    let midTermMark = jQuery('#mid-term-mark-create').val();
    let finalMark = jQuery('#final-mark-create').val();
    let csrfToken = jQuery('#mark-create-form').attr('csrf-token');
    $.ajax({
        url: MARK_API_URL,
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        dataType: 'json',
        data: {
            'subject': subjectId,
            'student': studentId,
            'mid_term_mark': midTermMark,
            'final_mark': finalMark
        },
        success: function (data) {
            alert('Created successfully!');
            location.reload();
        },
        error: function (data) {
            let msg = '';
            if (data.responseJSON.mid_term_mark)
                msg += ` Mid term mark : ${data.responseJSON.mid_term_mark[0]}<br/>`;
            if (data.responseJSON.final_mark)
                msg += ` Final mark: ${data.responseJSON.final_mark[0]}<br/>`
            $('#markCreateErr').show();
            $('#markCreateErr').html(msg);
        }
    });
}
