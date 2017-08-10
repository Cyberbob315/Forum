/**
 * Created by nhannt on 25/07/2017.
 */
$('#user-edit-form').submit(function (event) {
    event.preventDefault();
    this_ = $(this);
    deleteUrl = this_.attr('data-href');
    redirectUrl = this_.attr('data');
    let address = $('#input-address').val();
    let phone = $('#input-phone').val();
    let email = $('#input-email').val();
    let csrfToken = $("[name=csrfmiddlewaretoken]").val();
    let image = $('#input-image')[0].files[0];
    let data = new FormData();
    data.append('profile_pic', image);
    data.append('address', address);
    data.append('phone', phone);
    data.append('email', email);
    $.ajax({
        url: deleteUrl,
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            if (data.success) {
                alert('Update successfully');
            } else {
                alert('Update failed')
            }
            window.location.href = redirectUrl;
        },
        error: function (data) {
            alert('Email is not valid,please enter right email')
        }
    })
});

