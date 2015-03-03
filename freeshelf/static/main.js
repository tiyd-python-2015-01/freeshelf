$(document).on('ready', function () {
    $('.book-link').on('mousedown', function () {
        $(this).attr('href', $(this).data("link"));
    });

    $(".book").
        on('mouseenter', '.favorite', function () {
            $(this).addClass("fa-close").removeClass("fa-star");
            // add click event
        }).
        on('mouseleave', '.favorite', function () {
            $(this).removeClass("fa-close").addClass("fa-star");
            // remove click event
        });

    $(".add-favorite").on('click', function () {
        $.ajax({
            type: "POST",
            url: "/api/v1/books/" + $(this).data("book-id") + "/favorite",
            success: function (data) {
                $("#book-" + data['book_id']).
                    children(".book-link").
                    after(" <i class='fa fa-star favorite'></i>");
                $("#book-" + data['book_id']).
                    find('.add-favorite').
                    remove();
            },
            dataType: "json"
        });
    });

});