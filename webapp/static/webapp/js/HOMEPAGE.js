console.log('HOMEPAGE.js loaded');
document.addEventListener('DOMContentLoaded', function() {
    let element = document.querySelectorAll(".bait")
    element.forEach(function(element) {
        element.addEventListener("click", function() {
            console.log('bait clicked');
            let url = this.getAttribute("data-url")
            if (url) {
                window.location.href = url;
            }
        });
    });
})

