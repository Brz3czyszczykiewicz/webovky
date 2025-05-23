
let element = document.querySelectorAll(".bait")
element.forEach(function(element) {
    element.addEventListener("click", function() {
        let url = this.getAttribute("data-url")
        if (url) {
            window.location.href = url;
        }
    });
});
