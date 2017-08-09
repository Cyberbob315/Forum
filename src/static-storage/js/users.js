const USER_API_URL = '/api/account/';
const DEFAULT_STUDENT_ID = '20170000';
let tableHeader = `<tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Gender</th>
                        <th>Date of birth</th>
                        <th>Email</th>
                        <th>Mobile phone
                        <th>Status</th>
                    </tr>`;

$(document).ready(function () {
    initInputMask();
    initEvents();
});

function initEvents() {
    $('.infoRow').on('click', onRowClick);
    $('#btnSave').click(updateProfile);
    $('#btnDelete').click(deleteProfile);
    $('#btn-create-new').click(function (event) {
        event.preventDefault();
        $('#user-create-modal').modal({});
    });
    $('#btn-save-new').click(createNewUser);
}

function createNewUser(event) {
    event.preventDefault();
    $('#userCreateErr').hide();
    $('#userCreateErr').html('');
    let name = $('#user-name-create').val();
    let privateEmail = $('#user-private-email-create').val();
    let gender = $('#male-check-create').is(':checked');
    let birthDay = $('#user-date-birth-create').val();
    let mobileNumer = $('#user-phone-create').val();
    let address = $('#user-address-create').val();
    let csrfToken = $('#user-edit-form').attr('csrf-token');
    let image = $('#user-avatar-create')[0].files[0];
    let data = new FormData();
    data.append('student_id', DEFAULT_STUDENT_ID);
    data.append('name', name);
    data.append('gender', gender);
    data.append('date_of_birth', birthDay);
    data.append('private_email', privateEmail);
    data.append('mobile_phone', mobileNumer);
    data.append('home_address', address);
    if (image)
        data.append('profile_pic', image);

    $.ajax({
        url: USER_API_URL,
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            alert('Create successfully');
            location.reload();
        },
        error: function (data) {
            let msg = '';
            if (data.responseJSON.private_email)
                msg += ` Private Email : ${data.responseJSON.private_email[0]}<br/>`;
            if (data.responseJSON.mobile_phone)
                msg += ` Mobile phone number: ${data.responseJSON.mobile_phone[0]}<br/>`;
            $('#userCreateErr').show();
            $('#userCreateErr').html(msg);
        }
    });
}


function deleteProfile(event) {
    event.preventDefault();
    if (!confirm('Are you sure to delete this user?'))
        return;
    let studentId = $('#user-id').text();
    let url = `${USER_API_URL}${studentId}/`;
    let csrfToken = $('#user-edit-form').attr('csrf-token');
    $.ajax({
        url: url,
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        },
        dataType: 'json',
        data: {},
        success: function (data) {
            console.log('success');
            location.reload();
        },
        error: function (data) {
            console.log(data.result);
        }
    });
}

function updateProfile(event) {
    event.preventDefault();
    let studentId = $('#user-id').text();
    let updateUrl = `${USER_API_URL}${studentId}/`;
    let name = $('#user-name').text();
    let birthDay = $('#user-date-birth').val();
    let privateEmail = $('#user-private-email').val();
    let mobileNumer = $('#user-phone').val();
    let address = $('#user-address').val();
    let gender = $('#male-check').is(':checked');
    let csrfToken = $('#user-edit-form').attr('csrf-token');
    let image = $('#userAvatarUpload')[0].files[0];
    let data = new FormData();
    data.append('student_id', studentId);
    data.append('name', name);
    data.append('gender', gender);
    data.append('date_of_birth', birthDay);
    data.append('private_email', privateEmail);
    data.append('mobile_phone', mobileNumer);
    data.append('home_address', address);
    if (image)
        data.append('profile_pic', image);
    $.ajax({
        url: updateUrl,
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrfToken
        },
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            alert('Success!');
            location.reload();
        },

        error: function (data) {
            let msg = '';
            if (data.responseJSON.private_email)
                msg += ` Private email : ${data.responseJSON.private_email[0]}<br/>`;
            if (data.responseJSON.mobile_phone)
                msg += ` Mobile phone number: ${data.responseJSON.mobile_phone[0]}<br/>`;
            $('#userUpdateErr').show();
            $('#userUpdateErr').html(msg);

        }
    });
}

function onRowClick(event) {
    event.preventDefault();
    let this_ = $(this);
    let student_id = this_.attr('student-id');

    $.ajax({
        url: USER_API_URL + student_id,
        method: 'GET',
        dataType: 'json',
        data: {},
        success: function (data) {
            showUserModal(data);
        },
        error: function (data) {

        }
    })
}


function showUserModal(userInfo) {
    let userModal = $('#user-modal');
    userModal.on('show.bs.modal', function (event) {
        $('#user-name').text(userInfo.name);
        $('#userAvatar').attr('src', userInfo.profile_pic);
        $('#user-id').text(userInfo.student_id);
        $('#user-status').text(userInfo.status);
        $('#user-date-birth').val(userInfo.date_of_birth);
        $('#user-email').text(userInfo.email);
        $('#user-joined-date').text(userInfo.joined_time);
        $('#user-private-email').val(userInfo.private_email);
        $('#user-phone').val(userInfo.mobile_phone);
        $('#user-address').val(userInfo.home_address);
        $('#btnTranscript').attr('href', userInfo.transcript_link);
        if (userInfo.gender)
            $('#male-check').attr('checked', true);
        else
            $('#female-check').attr('checked', true);
        $(this).unbind();
    });
    userModal.modal({});
}

function initInputMask() {
    $('#user-date-birth').inputmask('yyyy-mm-dd', {'placeholder': 'yyyy-mm-dd'});
    $('#user-date-birth-create').inputmask('yyyy-mm-dd', {'placeholder': 'yyyy-mm-dd'});
}

function genUserItem(userValue) {
    return ` <tr student-id="${userValue.student_id}" class="infoRow">
                <td>${userValue.student_id}</td>
                <td><a href="${userValue.transcript_link}">${userValue.name}</a></td>
                <td>${userValue.gender}</td>
                <td>${userValue.date_of_birth}</td>
                <td>${userValue.private_email}</td>
                <td>${userValue.mobile_phone}</td>
                <td>${getStatusItem(userValue.status)}</td>
            </tr>`;
}

function getStatusItem(status) {
    let classes;
    switch (status) {
        case 'Administrator':
            classes = 'label label-success';
            break;
        case 'Studying':
            classes = 'label label-warning';
            break;
        case 'Graduated':
            classes = 'label label-info';
            break;
    }
    return `<span class="${classes}">${status}</span>`;
}