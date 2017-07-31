$('#btnQuickReply').click(function (event) {
    event.preventDefault();
    $('#replyModal').modal({});
    $('#replyModal').on('shown.bs.modal', function () {
        $('textarea').focus();
    });
});
