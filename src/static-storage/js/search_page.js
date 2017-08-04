const PAGINATOR_ELEMENT = ``;
const SEARCH_URL = '/api/thread/search';
const RESULT_PER_PAGE = 7;
let totalPage;
let currentPage = 1;
let subformSeleted = 'All';
let filterselected = 'None';
let nextPageUrl = '#';
let prevPageUrl = '#';
let hasNext = false;
let hasPrev = false;
$(document).ready(function () {
// Get subforum data to show in combobox
    getSubforumList();
// Start search automatically when starting from other page
    queryInit = $('#queryHolder').attr('query-data');
    // When reset page the query-data will be None so we won't search with that value
    if (queryInit !== 'None') {
        $('#inputSearch').val(queryInit);
        searchThread(queryInit);
    }
// Hide Paginator firest
    $('#paginator').hide();

// Init data for 2 combobox
    $(".btn-select").each(function (e) {
        let value = $(this).find("ul li.selected").html();
        if (value !== undefined) {
            $(this).find(".btn-select-input").val(value);
            $(this).find(".btn-select-value").html(value);
        }
    });
// Submit event for search bar when user hit enter or click search button
    $('#searchBar').submit(function (event) {
        event.preventDefault();
        query = $('#inputSearch').val();
        searchThread(query);
    });
});

// Next Button in paginator
$('#btnNext').click(function (event) {
    event.preventDefault();
    if (hasNext) {
        query = $('#inputSearch').val();
        searchThread(query, nextPageUrl);
        updatePageCount(++currentPage);
    }
});

// Previous button in paginator
$('#btnPrev').click(function (event) {
    event.preventDefault();
    if (hasPrev) {
        query = $('#inputSearch').val();
        searchThread(query, prevPageUrl);
        updatePageCount(--currentPage);
    }
});


function getSubforumList() {
    let subForumUL = $('#subForumList');
    $.ajax({
        url: '/api/subforum/list',
        method: 'GET',
        success: function (data) {
            for (key in data) {
                subForumUL.append("<li>" + data[key].title + "<li/>");
            }
        },
        error: function (data) {
        }
    });
}

function searchThread(query, url = SEARCH_URL) {
    let threadSearchUrl = url;
    let paginator = $('#paginator');
    let resultsContainer = $('#resultContainer');
    resultsContainer.html('');
    let delay = 500;
    let loader = `<div id="loader" class="loader"></div>`;
    let resultCounter = $('#resultCounter');

    $.ajax({
        url: threadSearchUrl,
        method: 'GET',
        dataType: 'json',
        data: {
            'query': query,
            'subforum': subformSeleted,
            'filter': filterselected
        },
        beforeSend: function () {
            resultsContainer.append(loader);
        },
        success: function (data) {
            console.log('success');
            setTimeout(function () {
                resultCounter.html(`${data.count} threads found`);
                resultsContainer.html('');
                if (data.results.length === 0) {
                    resultCounter.html('');
                    resultsContainer.append(`<h1>No results</h1>`);
                }
                totalPage = Math.ceil(data.count / RESULT_PER_PAGE);
                if (data.count > 7) {
                    paginator.show();
                } else {
                    paginator.hide();
                    resultCounter.html('');
                }
                if (data.next) {
                    nextPageUrl = data.next;
                    $('#btnNext').attr('class', '');
                    hasNext = true;
                } else {
                    nextPageUrl = '#';
                    $('#btnNext').attr('class', 'disabled');
                    hasNext = false;
                }
                if (data.previous) {
                    prevPageUrl = data.previous;
                    $('#btnPrev').attr('class', '');
                    hasPrev = true;
                } else {
                    prevPageUrl = '#';
                    $('#btnPrev').attr('class', 'disabled');
                    hasPrev = false;
                }
                if (url === SEARCH_URL) {
                    console.log('here', data.count);
                    initPageCount();
                }
                for (let key in data.results) {
                    resultsContainer.append(genThreadItem(data.results[key])).hide().show(400);
                }
            }, delay);

        },
        error: function (data) {
            console.log('error');
            console.log(data);
        }
    });
}

$(document).on('click', '.btn-select', function (e) {
    e.preventDefault();
    let ul = $(this).find("ul");
    if ($(this).hasClass("active")) {
        if (ul.find("li").is(e.target)) {
            let target = $(e.target);
            let value = target.html();
            let id = $(this).attr('id');
            if (value !== '') {
                target.addClass("selected").siblings().removeClass("selected");
                $(this).find(".btn-select-input").val(value);
                $(this).find(".btn-select-value").html(value);
                switch (id) {
                    case 'subForumSelect':
                        subformSeleted = value;
                        break;
                    case 'filterSelect':
                        filterselected = value;
                        break;
                }
            }
            let query = $('#inputSearch').val();
            searchThread(query);
        }
        ul.hide();
        $(this).removeClass("active");
    }
    else {
        $('.btn-select').not(this).each(function () {
            $(this).removeClass("active").find("ul").hide();
        });
        ul.slideDown(300);
        $(this).addClass("active");
    }
});

$(document).on('click', function (e) {
    let target = $(e.target).closest(".btn-select");
    if (!target.length) {
        $(".btn-select").removeClass("active").find("ul").hide();
    }
});

function updatePageCount(pageNum) {
    $('#pageCounter').html(`${pageNum}/${totalPage}`);
}

function initPageCount() {
    currentPage = 1;
    $('#pageCounter').html(`${currentPage}/${totalPage}`);
}

function genThreadItem(threadValue) {
    let item = ` <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                            <article class="card">
                                <div class="row">
                                    <div class="col-sm-4 col-md-2">
                                        <figure>
                                            <img
                                                class="img-rounded img-responsive img-user"
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
                        </div><hr/>`;
    return item;
}
