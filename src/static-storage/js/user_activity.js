const THREAD_API_BASE_URL = $('#dataHolder').attr('thread-url');
const COMMENT_API_BASE_URL = $('#dataHolder').attr('comment-url');
const TYPE_THREAD = 1;
const TYPE_COMMENT = 2;
const RESULT_PER_PAGE = 5;
let studentId = $('#dataHolder').attr('student-id');
let threadPaginator = $('#threadPaginator');
let commentPaginator = $('#commentPaginator');
let btnNextThread = $('#btnNextThread');
let btnPrevThread = $('#btnPrevThread');
let btnNextComment = $('#btnNextComment');
let btnPrevComment = $('#btnPrevComment');
let nextThreadUrl;
let prevThreadUrl;
let nextCommentUrl;
let prevCommentUrl;
let currentThreadPage = 1;
let currentCommentPage = 1;
let totalThreadPage;
let totalCommentPage;

$(document).ready(function () {
    getUserThreads();
    getUserComments();
    document.getElementById("defaultOpen").click();

});

btnPrevThread.click({'type': TYPE_THREAD}, prevPage);
btnNextThread.click({'type': TYPE_THREAD}, nextPage);
btnNextComment.click({'type': TYPE_COMMENT}, nextPage);
btnPrevComment.click({'type': TYPE_COMMENT}, prevPage);

function nextPage(event) {
    type = event.data.type;
    switch (type) {
        case TYPE_THREAD:
            if (nextThreadUrl) {
                getUserThreads(false, nextThreadUrl);
                updatePageCount(TYPE_THREAD, ++currentThreadPage);
            }
            break;
        case TYPE_COMMENT:
            if (nextCommentUrl) {
                getUserComments(false, nextCommentUrl);
                updatePageCount(TYPE_COMMENT, ++currentCommentPage);
            }
            break;
    }
}

function prevPage(event, type) {
    type = event.data.type;
    switch (type) {
        case TYPE_THREAD:
            if (prevThreadUrl) {
                getUserThreads(false, prevThreadUrl);
                updatePageCount(TYPE_THREAD, --currentThreadPage);
            }
            break;
        case TYPE_COMMENT:
            if (prevCommentUrl) {
                getUserComments(false, prevCommentUrl);
                updatePageCount(TYPE_COMMENT, --currentCommentPage);
            }
            break;
    }
}

function getUserThreads(isInit = true, url = THREAD_API_BASE_URL) {
    let threadContainer = $('#userThreadsContainer');
    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        data: {
            'student_id': studentId
        },
        success: function (data) {
            nextThreadUrl = data.next;
            prevThreadUrl = data.previous;
            threadContainer.html('');
            totalThreadPage = Math.ceil(data.count / RESULT_PER_PAGE);

            if (data.count <= RESULT_PER_PAGE)
                threadPaginator.hide();
            else
                threadPaginator.show();

            if (data.next)
                btnNextThread.attr('class', '');
            else
                btnNextThread.attr('class', 'disabled');

            if (data.previous)
                btnPrevThread.attr('class', '');
            else
                btnPrevThread.attr('class', 'disabled');

            if (isInit)
                initPageCount();

            for (let key in data.results) {
                threadContainer.append(genThreadItem(data.results[key]));
            }
        },
        error: function (data) {
            console.log('thread error');
        }
    });
}

function getUserComments(isInit = true, url = COMMENT_API_BASE_URL) {
    let commentContainer = $('#userCommentsContainer');
    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        data: {
            'student_id': studentId
        },
        success: function (data) {
            nextCommentUrl = data.next;
            prevCommentUrl = data.previous;
            commentContainer.html('');
            totalCommentPage = Math.ceil(data.count / RESULT_PER_PAGE);
            if (data.count <= RESULT_PER_PAGE)
                commentPaginator.hide();
            else
                commentPaginator.show();

            if (data.next)
                btnNextComment.attr('class', '');
            else
                btnNextComment.attr('class', 'disabled');

            if (data.previous)
                btnPrevComment.attr('class', '');
            else
                btnPrevComment.attr('class', 'disabled');

            if (isInit)
                initPageCount();
            for (let key in data.results) {
                commentContainer.append(genCommentItem(data.results[key]));
            }
        },
        error: function (data) {
            console.log('comment error');
        }
    });
}

function updatePageCount(type, pageNum) {
    switch (type) {
        case TYPE_THREAD:
            $('#pageCounterThread').html(`${pageNum}/${totalThreadPage}`);
            break;
        case TYPE_COMMENT:
            $('#pageCounterComment').html(`${pageNum}/${totalCommentPage}`);
            break;
    }
}

function initPageCount() {
    currentCommentPage = 1;
    currentThreadPage = 1;
    $('#pageCounterComment').html(`${currentCommentPage}/${totalCommentPage}`);
    $('#pageCounterThread').html(`${currentThreadPage}/${totalThreadPage}`);
}

function genThreadItem(threadValue) {
    return ` <article class="card">
                                <div class="row">
                                    <div class="col-sm-4 col-md-2">
                                        <figure>
                                            <img
                                                class="img-rounded img-responsive "
                                                style="width: 80px;height: 80px"
                                                src="${threadValue.author_pic_url}">
                                        </figure>
                                    </div>
                                    <div class="col-sm-8 col-md-10">
                                        <span
                                            class="label label-default pull-right">
                                            <i class="glyphicon glyphicon-comment"></i>${threadValue.total_comment}
                                        </span>
                                        <h4>${threadValue.title}</h4>
                                        <p>${threadValue.content}</p>
                                        <section>
                                            <i class="glyphicon glyphicon-folder-open"></i>${threadValue.sub_forum}
                                            <i class="glyphicon glyphicon-user"></i>${threadValue.author_name}
                                            <i class="glyphicon glyphicon-calendar"></i>${threadValue.created_date}
                                            <i class="glyphicon glyphicon-eye-open"></i>${threadValue.total_view}
                                            <i class="glyphicon glyphicon-thumbs-up"></i>${threadValue.total_like}
                                            <span class="pull-right">
                                                <a href="${threadValue.detail_link}"
                                                   target="_blank"
                                                   class="btn btn-default btn-sm">More
                                                ... </a>
                                            </span>
                                        </section>
                                    </div>
                                </div>
                            </article>
                        <hr/>`;
}

function genCommentItem(commentValue) {
    return `<article class="card">
                <div class="row col-md-12 col-sm-12">
                    <strong>Reply to thread 
                        "<a target="_blank" 
                            href="${commentValue.thread_link}">
                            ${commentValue.thread_title}
                        </a>"
                    </strong>
                </div>
                <div class="row">
                    <div class="col-md-2 col-sm-2 hidden-xs">
                        <figure>
                            <img class="img-responsive"
                                 style="height: 100px;width: 100px;"
                                 src="${commentValue.author_pic_link}"/>
                            <figcaptionclass="text-center">
                                ${commentValue.author_name}
                            </figcaption>
                        </figure>
                    </div>
                    <div class="col-md-10 col-sm-10">
                        <div class="panel panel-default arrow left">
                            <div class="panel-body">
                                <header class="text-left">
                                    <time class="comment-date">
                                        ${commentValue.created_date}
                                    </time>
                                    <hr/>
                                </header>
                                <div class="comment-post">
                                    <p>${commentValue.content}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </article>`
}

function openCity(evt, tabName) {
    // Declare all letiables

    // Get all elements with class="tabcontent" and hide them
    let tabcontent = document.getElementsByClassName("tabcontent");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    let tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}
