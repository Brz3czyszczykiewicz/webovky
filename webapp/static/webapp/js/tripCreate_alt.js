console.log("tripCreate.js spuštěn");
document.addEventListener("DOMContentLoaded", function () {
    console.log("jebat js");

    const toggleBtn = document.getElementById("toggle-gallery");
    const galleryWrapper = document.getElementById("gallery-wrapper");

    if (toggleBtn && galleryWrapper) {
        toggleBtn.addEventListener("click", () => {
            console.log("už funguju")
            const isHidden = galleryWrapper.style.display === "none" || galleryWrapper.style.display === "";
            galleryWrapper.style.display = isHidden ? "block" : "none";
            toggleBtn.textContent = isHidden ? "Skrýt obrázky" : "Vyber obrázky";
        });
    }

    const selected = new Set();
    const gallery = document.getElementById("gallery");
    const hiddenInput = document.getElementById("selected-images");

    if (gallery) {
        gallery.querySelectorAll(".gallery-image").forEach(imgDiv => {
            imgDiv.addEventListener("click", () => {
                const filename = imgDiv.dataset.filename;
                if (selected.has(filename)) {
                    selected.delete(filename);
                    imgDiv.classList.remove("border-primary");
                    imgDiv.classList.add("border-secondary");
                } else {
                    selected.add(filename);
                    imgDiv.classList.add("border-primary");
                    imgDiv.classList.remove("border-secondary");
                }
                hiddenInput.value = Array.from(selected).join(",");
            });
        });
    }
});