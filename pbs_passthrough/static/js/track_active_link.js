document.addEventListener("DOMContentLoaded", function() {
    var currentPage = window.location.pathname;
    var links = document.querySelectorAll('.nav-links a');
    links.forEach(function(link) {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});