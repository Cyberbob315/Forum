const FORUM_LIST_API = '/api/subforum/list/';

$(document).ready(function () {
    let forumList = $('#forumListLink');
    $.ajax({
        url: FORUM_LIST_API,
        method: 'GET',
        dataType: 'json',
        data: {},
        success: function (data) {
            for (let forum of data) {
                forumList.append(genForumLink(forum));
            }
        },
        error: function (data) {

        }
    });
});

function genForumLink(forumValue) {
    title = forumValue.title;
    if (title.length > 10)
        title = `${title.substring(0, 10)}...`;
    return `<li><a href="${forumValue.draft_list_link}">${title}
                <span class="pull-right" style="margin-right: 15px">${forumValue.total_draft}</span>
            </a></li>`;
}
