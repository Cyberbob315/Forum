var subformSeleted = 'All';
$(document).ready(function () {

    getSubforumList();

    $(".btn-select").each(function (e) {
        let value = $(this).find("ul li.selected").html();
        if (value !== undefined) {
            $(this).find(".btn-select-input").val(value);
            $(this).find(".btn-select-value").html(value);
        }
    });

    $('#searchBar').submit(function (event) {
        event.preventDefault();
        query = $('#inputSearch').val();
        searchThread(query)
    })
});

function getSubforumList() {
    var subForumUL = $('#subForumList');
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

function searchThread(query) {
    let threadSearchUrl = '/api/thread/search';
    let resultsContainer = $('#resultContainer');
    resultsContainer.html('');
    $.ajax({
        url: threadSearchUrl,
        method: 'GET',
        dataType: 'json',
        data: {
            'query': query,
            'subforum': subformSeleted
        },
        success: function (data) {
            console.log('success');
            if (data.results.length === 0) {
                resultsContainer.append(`<h1>No results</h1>`);
            }
            for (let key in data.results) {
                resultsContainer.append(genThreadItem(data.results[key]));
            }
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
            if (value !== '') {
                target.addClass("selected").siblings().removeClass("selected");
                $(this).find(".btn-select-input").val(value);
                $(this).find(".btn-select-value").html(value);
                subformSeleted = value;
                query = $('#inputSearch').val();
                searchThread(query);
            }
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
    var target = $(e.target).closest(".btn-select");
    if (!target.length) {
        $(".btn-select").removeClass("active").find("ul").hide();
    }
});

function genThreadItem(threadValue) {
    var item = ` <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                            <article>
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
