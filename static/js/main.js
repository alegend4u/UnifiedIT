$(document).ready(function () {
    $(document).scroll(function () {
        var $nav = $("nav");
        var $links = $("nav a");
        $nav.toggleClass('scrollednav', $(this).scrollTop() > 0);
        $links.toggleClass('scrolleda', $(this).scrollTop() > 0);
    });
});