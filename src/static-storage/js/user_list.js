const USER_LIST_API = '/api/account/';

$(document).ready(function () {
    let table = $('#userTable');
    $.ajax({
        url: USER_LIST_API,
        method: 'GET',
        dataType: 'json',
        data: {},
        success: function (data) {
            for (let user of data) {
                let userItem = $(genUserItem(user));
                table.append(userItem);
            }
            $('.infoRow').on('click', onRowClick);
        },
        error: function (data) {

        }
    })
});

function onRowClick(event) {
    event.preventDefault();
    let this_ = $(this);
    let student_id = this_.attr('student-id');
    let userModal = $('#user-modal');
    $.ajax({
        url: USER_LIST_API + student_id,
        method: 'GET',
        dataType: 'json',
        data:{},
        success: function (data) {
            console.log(data);
        },
        error: function (data) {

        }
    })
}

function showUserModal(userInfo) {
    userModal.on('show.bs.modal', function (event) {

    });
    userModal.modal({});
}

function genUserItem(userValue) {
    return ` <tr student-id="${userValue.student_id}" class="infoRow">
                <td>${userValue.student_id}</td>
                <td>${userValue.name}</td>
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
