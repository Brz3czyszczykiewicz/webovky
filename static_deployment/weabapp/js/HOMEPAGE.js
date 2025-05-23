
let element = document.querySelectorAll(".bait")
element.forEach(function(element) {
    element.addEventListener("click", function() {
        let url = element.getAttribute("data-url")
        if (url) {
            window.location.href = url;
        }
    });
});
