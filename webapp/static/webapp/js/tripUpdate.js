document.addEventListener("DOMContentLoaded", function () {
    function setupGallery(toggleId, wrapperId, galleryId, inputId, showText, hideText) {
        const toggleBtn = document.getElementById(toggleId);
        const wrapper = document.getElementById(wrapperId);
        const gallery = document.getElementById(galleryId);
        const hiddenInput = document.getElementById(inputId);
        const selected = new Set();

        if (!toggleBtn || !wrapper) return;

        toggleBtn.textContent = showText;

        toggleBtn.addEventListener("click", () => {
            const isHidden = wrapper.style.display === "none" || wrapper.style.display === "";
            wrapper.style.display = isHidden ? "block" : "none";
            toggleBtn.textContent = isHidden ? hideText : showText;
        });

        if (gallery) {
            gallery.querySelectorAll(".gallery-image").forEach(div => {
                div.addEventListener("click", () => {
                    const filename = div.dataset.filename;
                    if (selected.has(filename)) {
                        selected.delete(filename);
                        div.classList.remove("border-primary");
                        div.classList.add("border-secondary");
                    } else {
                        selected.add(filename);
                        div.classList.add("border-primary");
                        div.classList.remove("border-secondary");
                    }
                    hiddenInput.value = Array.from(selected).join(",");
                });
            });
        }
    }

    setupGallery("toggle-gallery-available", "gallery-wrapper-available", "gallery-available", "selected-images-available", "Přidej obrázky", "Skrýt nabídku");
    setupGallery("toggle-gallery-attached", "gallery-wrapper-attached", "gallery-attached", "selected-images-attached", "Aktuální výběr", "Skrýt přiřazené obrázky");
});