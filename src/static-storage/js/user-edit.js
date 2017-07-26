/**
 * Created by nhannt on 25/07/2017.
 */
$('#user-edit-form').submit(function (event) {
    event.preventDefault();
    this_ = $(this);
    url = this_.attr('data-href');
    redirectUrl = this_.attr('data');
    var address = $('#input-address').val();
    var phone = $('#input-phone').val();
    var email = $('#input-email').val();
    var csrfToken = $("[name=csrfmiddlewaretoken]").val();
    console.log(image);

    $.ajax({
        url: url,
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: {
            'address': address,
            'phone': phone,
            'email': email
        },
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

$('#form-image').submit(function (event) {
    event.preventDefault();
    this_ = $(this);
    url = this_.attr('data-href');
    redirectUrl = this_.attr('data');
    var image = $('#input-image')[0].files[0];
    var data = new FormData();
    data.append('profile_pic',image);
    var csrfToken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: url,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: data,
        processData: false,
        contentType: false,
        success: function (data) {
            if (data.success) {
                alert('Update successfully');
            } else {
                alert('Update failed')
            }
            window.location.href = redirectUrl;
        },
        error: function (data) {

        }
    });
});
