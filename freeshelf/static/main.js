(function () {
    $(function () {
        $('.book-link').on('mousedown', function () {
            $(this).attr('href', $(this).data("link"));
        })
    })
})();